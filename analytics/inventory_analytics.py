import pandas as pd

from database.connection import get_connection

class InventoryAnalytics:

    def get_stock_coverage_by_store(self) -> pd.DataFrame:
        connection = get_connection()

        try:
            query = """
                select
                    store_id,
                    round(
                        avg(
                            inventory_level::numeric
                            / nullif(demand_forecast, 0)
                        ),
                        2
                    ) as avg_stock_coverage_days,
                    count(*) filter (
                        where demand_forecast > 0
                    ) as valid_forecast_records
                from daily_inventory
                group by store_id
                order by avg_stock_coverage_days asc
            """

            with connection.cursor() as cursor:
                cursor.execute(query)

                rows = cursor.fetchall()

                columns = [
                    description[0]
                    for description in cursor.description
                ]

            df = pd.DataFrame(rows, columns=columns)

            if not df.empty:
                df["avg_stock_coverage_days"] = pd.to_numeric(
                    df["avg_stock_coverage_days"]
                )

            return df

        finally:
            connection.close()
