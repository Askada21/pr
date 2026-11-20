from database.connection import get_connection
from models.inventory import InventoryRecord

class InventoryService:

    def get_inventory_record(
        self,
        date: str,
        product_id: str,
        store_id: str
    ) -> InventoryRecord | None:

        connection = get_connection()

        try:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    select
                        date,
                        product_id,
                        store_id,
                        inventory_level,
                        units_sold,
                        demand_forecast
                    from daily_inventory
                    where date = %s
                      and product_id = %s
                      and store_id = %s
                    """,
                    (date, product_id, store_id)
                )

                row = cursor.fetchone()

                if row is None:
                    return None

                return InventoryRecord(
                    date=row[0].isoformat(),
                    product_id=row[1],
                    store_id=row[2],
                    inventory_level=row[3],
                    units_sold=row[4],
                    demand_forecast=float(row[5])
                )

        finally:
            connection.close()

    def get_high_risk_inventory(
        self,
        date: str,
        store_id: str
    ) -> list[InventoryRecord]:

        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    select
                        date,
                        product_id,
                        store_id,
                        inventory_level,
                        units_sold,
                        demand_forecast
                    from daily_inventory
                    where date = %s
                      and store_id = %s
                    order by product_id
                    """,
                    (date, store_id)
                )

                rows = cursor.fetchall()

                records = []

                for row in rows:
                    record = InventoryRecord(
                        date=row[0].isoformat(),
                        product_id=row[1],
                        store_id=row[2],
                        inventory_level=row[3],
                        units_sold=row[4],
                        demand_forecast=float(row[5])
                    )

                    if record.stockout_risk() == "High":
                        records.append(record)

                return sorted(
                    records,
                    key=lambda record: record.stock_coverage_days()
                )

        finally:
            connection.close()

    def get_replenishment_recommendations(
        self,
        date: str,
        store_id: str,
        lead_time_days: int = 3,
        safety_stock_days: int = 2
    ) -> list[dict]:

        if lead_time_days < 0 or safety_stock_days < 0:
            raise ValueError("Days cannot be negative")

        records = self.get_high_risk_inventory(
            date=date,
            store_id=store_id
        )

        recommendations = []

        for record in records:
            order_quantity = record.recommended_order_quantity(
                lead_time_days=lead_time_days,
                safety_stock_days=safety_stock_days
            )

            recommendations.append({
                "product_id": record.product_id,
                "store_id": record.store_id,
                "date": record.date,
                "inventory_level": record.inventory_level,
                "stock_coverage_days": record.stock_coverage_days(),
                "stockout_risk": record.stockout_risk(),
                "recommended_order": order_quantity
            })

        return recommendations