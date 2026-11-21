import pandas as pd
import pytest

from analytics.inventory_analytics import InventoryAnalytics
from database.connection import get_connection

@pytest.mark.integration
def test_low_stock_rate_matches_database():
    analytics = InventoryAnalytics()

    # Result from our Python analytics method
    df = analytics.get_low_stock_rate_by_store(
        threshold=50
    )

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5

    # Independently calculate results using PostgreSQL
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                select
                    store_id,
                    count(*) as total_records,
                    count(*) filter (
                        where inventory_level < 50
                    ) as low_stock_records
                from daily_inventory
                group by store_id
            """)

            rows = cursor.fetchall()

    finally:
        connection.close()

    # Compare Python results with direct SQL results
    expected = {
        store_id: (total, low_stock)
        for store_id, total, low_stock in rows
    }

    for _, row in df.iterrows():
        store_id = row["store_id"]

        total, low_stock = expected[store_id]

        expected_rate = (
            100 * low_stock / total
            if total > 0 else 0
        )

        assert row["total_records"] == total
        assert row["low_stock_records"] == low_stock
        assert float(row["low_stock_rate_pct"]) == pytest.approx(
            expected_rate,
            abs=0.01
        )
