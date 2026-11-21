from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from analytics.inventory_analytics import InventoryAnalytics

@patch("analytics.inventory_analytics.get_connection")
def test_low_stock_rate_calculation(mock_get_connection):
    # Arrange
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    mock_cursor.description = [
        ("store_id",),
        ("total_records",),
        ("low_stock_records",),
        ("low_stock_rate_pct",)
    ]

    mock_cursor.fetchall.return_value = [
        ("S001", 100, 20, 20.0),
        ("S002", 100, 10, 10.0)
    ]

    analytics = InventoryAnalytics()

    # Act
    df = analytics.get_low_stock_rate_by_store(threshold=50)

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2

    assert df.iloc[0]["store_id"] == "S001"
    assert df.iloc[0]["low_stock_rate_pct"] == 20.0

    assert df.iloc[1]["store_id"] == "S002"
    assert df.iloc[1]["low_stock_rate_pct"] == 10.0

    mock_cursor.execute.assert_called_once()
    args = mock_cursor.execute.call_args.args

    assert args[1] == (50, 50)

    mock_connection.close.assert_called_once()

@pytest.mark.parametrize("threshold", [-1, -10, -100])
def test_negative_low_stock_threshold(threshold):
    analytics = InventoryAnalytics()

    with pytest.raises(ValueError):
        analytics.get_low_stock_rate_by_store(threshold=threshold)

@patch("analytics.inventory_analytics.get_connection")
def test_empty_low_stock_results(mock_get_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    mock_cursor.description = [
        ("store_id",),
        ("total_records",),
        ("low_stock_records",),
        ("low_stock_rate_pct",)
    ]

    mock_cursor.fetchall.return_value = []

    analytics = InventoryAnalytics()

    df = analytics.get_low_stock_rate_by_store(threshold=50)

    assert df.empty
    mock_connection.close.assert_called_once()
