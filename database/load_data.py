# Uploads prepared data to database
import pandas as pd
from psycopg2.extras import execute_values
from pathlib import Path
from database.connection import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "inventory_cleaned.csv"


def extract_data():
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully!")
    print("Total records:", len(df))
    print("Total columns:", len(df.columns))

    return df

def transform_data(df):

    # Dimension tables
    products = df[["product_id"]].drop_duplicates()
    stores = df[["store_id"]].drop_duplicates()

    categories = pd.DataFrame({
        "category_name": sorted(df["category"].unique())
    })

    categories["category_id"] = range(1, len(categories) + 1)

    regions = pd.DataFrame({
        "region_name": sorted(df["region"].unique())
    })

    regions["region_id"] = range(1, len(regions) + 1)

    # Fact table
    daily_inventory = df.merge(
        categories,
        left_on="category",
        right_on="category_name",
        validate="many_to_one"
    )

    daily_inventory = daily_inventory.merge(
        regions,
        left_on="region",
        right_on="region_name",
        validate="many_to_one"
    )

    daily_inventory = daily_inventory[[
        "date",
        "product_id",
        "store_id",
        "inventory_level",
        "units_sold",
        "units_ordered",
        "demand_forecast",
        "price",
        "discount",
        "weather_condition",
        "holiday_promotion",
        "competitor_pricing",
        "seasonality",
        "category_id",
        "region_id"
    ]]

    return products, stores, categories, regions, daily_inventory

def load_data(products, stores, categories, regions, daily_inventory):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Load products
            execute_values(
                cursor,
                "insert into products (product_id) values %s",
                list(products.itertuples(index=False, name=None))
            )

            # Load stores
            execute_values(
                cursor,
                "insert into stores (store_id) values %s",
                list(stores.itertuples(index=False, name=None))
            )

            # Load categories
            execute_values(
                cursor,
                """
                insert into categories
                (category_id, category_name)
                values %s
                """,
                list(categories[
                    ["category_id", "category_name"]
                ].itertuples(index=False, name=None))
            )

            # Load regions
            execute_values(
                cursor,
                """
                insert into regions
                (region_id, region_name)
                values %s
                """,
                list(regions[
                    ["region_id", "region_name"]
                ].itertuples(index=False, name=None))
            )

            # Prepare boolean values
            daily_inventory = daily_inventory.copy()

            if not daily_inventory["holiday_promotion"].isin([0, 1]).all():
                raise ValueError("Invalid holiday_promotion values")

            daily_inventory["holiday_promotion"] = (
                daily_inventory["holiday_promotion"].astype(bool)
            )

            # Load fact table
            execute_values(
                cursor,
                """
                insert into daily_inventory (
                    date,
                    product_id,
                    store_id,
                    inventory_level,
                    units_sold,
                    units_ordered,
                    demand_forecast,
                    price,
                    discount,
                    weather_condition,
                    holiday_promotion,
                    competitor_pricing,
                    seasonality,
                    category_id,
                    region_id
                )
                values %s
                """,
                list(daily_inventory.itertuples(
                    index=False, name=None
                )),
                page_size=1000
            )

        connection.commit()

        print("All records inserted successfully!")

    except Exception as error:
        connection.rollback()
        print("Database loading failed:", error)
        raise

    finally:
        connection.close()

if __name__ == "__main__":

    df = extract_data()

    products, stores, categories, regions, daily_inventory = transform_data(df)

    assert len(daily_inventory) == len(df)

    assert not daily_inventory.duplicated(
        subset=["date", "product_id", "store_id"]
    ).any()

    assert not daily_inventory.isnull().any().any()

    print("Data validation passed!")

    load_data(
        products,
        stores,
        categories,
        regions,
        daily_inventory
    )

    print("ETL pipeline completed successfully!")