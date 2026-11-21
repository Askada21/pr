import pandas as pd

from database.connection import get_connection


class SalesAnalytics:

    def get_revenue_by_store(self) -> pd.DataFrame:
        connection = get_connection()

        try:
            query = """
                select
                    store_id,
                    sum(units_sold) as total_units_sold,
                    round(
                        sum(units_sold * price),
                        2
                    ) as estimated_revenue
                from daily_inventory
                group by store_id
                order by estimated_revenue desc
            """

            with connection.cursor() as cursor:
                cursor.execute(query)

                rows = cursor.fetchall()

                columns = [description[0] for description in cursor.description]

            return pd.DataFrame(rows, columns=columns)

        finally:
            connection.close()

    def get_revenue_by_category(self) -> pd.DataFrame:
        connection = get_connection()

        try:
            query = """
                select
                    c.category_name,
                    sum(d.units_sold) as total_units_sold,
                    round(
                        sum(d.units_sold * d.price),
                        2
                    ) as estimated_revenue
                from daily_inventory as d
                join categories as c
                    on d.category_id = c.category_id
                group by c.category_name
                order by estimated_revenue desc
            """

            with connection.cursor() as cursor:
                cursor.execute(query)

                rows = cursor.fetchall()

                columns = [description[0] for description in cursor.description]

            return pd.DataFrame(rows, columns=columns)

        finally:
            connection.close()

    def get_monthly_sales_trends(self) -> pd.DataFrame:
        connection = get_connection()

        try:
            query = """
                select
                    date_trunc('month', date)::date as month,
                    sum(units_sold) as total_units_sold,
                    round(sum(units_sold * price), 2) as estimated_revenue
                from daily_inventory
                group by date_trunc('month', date)
                having count(distinct date) = extract(
                    day from (
                        date_trunc('month', date) + interval '1 month - 1 day'
                    )
                )
                order by month;
            """

            with connection.cursor() as cursor:
                cursor.execute(query)

                rows = cursor.fetchall()

                columns = [description[0] for description in cursor.description]

            df = pd.DataFrame(rows, columns=columns)

            if not df.empty:
                df["month"] = pd.to_datetime(df["month"])
                df["estimated_revenue"] = pd.to_numeric(df["estimated_revenue"])

            return df

        finally:
            connection.close()
