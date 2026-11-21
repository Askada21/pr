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

    def get_stockout_rate_by_store(self) -> pd.DataFrame:
        connection = get_connection()

        try:
            query = """
                select
                    store_id,
                    count(*) as total_records,
                    count(*) filter (
                        where inventory_level = 0
                    ) as zero_stock_records,
                    round(
                        100.0 * count(*) filter (
                            where inventory_level = 0
                        ) / nullif(count(*), 0),
                        2
                    ) as zero_stock_rate_pct
                from daily_inventory
                group by store_id
                order by zero_stock_rate_pct desc
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
                df["zero_stock_rate_pct"] = pd.to_numeric(
                    df["zero_stock_rate_pct"]
                )

            return df

        finally:
            connection.close()

    def get_low_stock_rate_by_store(
        self,
        threshold: int = 50
    ) -> pd.DataFrame:

        if threshold < 0:
            raise ValueError("Threshold cannot be negative")

        connection = get_connection()

        try:
            query = """
                select
                    store_id,
                    count(*) as total_records,
                    count(*) filter (
                        where inventory_level < %s
                    ) as low_stock_records,
                    round(
                        100.0 * count(*) filter (
                            where inventory_level < %s
                        ) / nullif(count(*), 0),
                        2
                    ) as low_stock_rate_pct
                from daily_inventory
                group by store_id
                order by low_stock_rate_pct desc
            """

            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (threshold, threshold)
                )

                rows = cursor.fetchall()

                columns = [
                    description[0]
                    for description in cursor.description
                ]

            df = pd.DataFrame(rows, columns=columns)

            if not df.empty:
                df["low_stock_rate_pct"] = pd.to_numeric(
                    df["low_stock_rate_pct"]
                )

            return df

        finally:
            connection.close()
 

