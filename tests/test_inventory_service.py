from unittest.mock import MagicMock, patch
from datetime import date

from services.inventory_service import InventoryService


@patch("services.inventory_service.get_connection")
def test_get_high_risk_inventory(mock_get_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (date(2022, 1, 1), "P0001", "S001", 10, 5, 10.0),
        (date(2022, 1, 1), "P0002", "S001", 100, 5, 10.0),
        (date(2022, 1, 1), "P0003", "S001", 30, 5, 10.0),
    ]

    service = InventoryService()
    records = service.get_high_risk_inventory("2022-01-01", "S001")

    assert len(records) == 1
    assert records[0].product_id == "P0001"
    assert records[0].stockout_risk() == "High"

    mock_connection.close.assert_called_once()
