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