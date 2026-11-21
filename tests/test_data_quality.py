from unittest.mock import MagicMock, patch

from database.data_quality import check_data_quality

@patch("database.data_quality.get_connection")
def test_data_quality_valid_dataset(mock_get_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    # Simulate a database with no quality issues
    mock_cursor.fetchone.return_value = (
        73100, 0, 0, 0, 0
    )

    results = check_data_quality()

    assert results["total_records"] == 73100
    assert results["missing_critical_values"] == 0
    assert results["negative_inventory"] == 0
    assert results["negative_sales"] == 0
    assert results["invalid_prices"] == 0

    mock_connection.close.assert_called_once()

@patch("database.data_quality.get_connection")
def test_data_quality_detects_issues(mock_get_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    # Simulate a database containing invalid values
    mock_cursor.fetchone.return_value = (
        1000, 3, 2, 1, 4
    )

    results = check_data_quality()

    assert results["missing_critical_values"] == 3
    assert results["negative_inventory"] == 2
    assert results["negative_sales"] == 1
    assert results["invalid_prices"] == 4

    mock_connection.close.assert_called_once()

@patch("database.data_quality.get_connection")
def test_data_quality_connection_closed(mock_get_connection):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    mock_cursor.fetchone.return_value = (
        10, 0, 0, 0, 0
    )

    check_data_quality()

    mock_connection.close.assert_called_once()
