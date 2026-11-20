from unittest.mock import patch

import pytest

from models.inventory import InventoryRecord
from services.inventory_service import InventoryService


@pytest.fixture
def sample_record():
    return InventoryRecord(
        date="2022-01-01",
        product_id="P0001",
        store_id="S001",
        inventory_level=150,
        units_sold=80,
        demand_forecast=100.0
    )


@patch.object(InventoryService, "get_high_risk_inventory")
def test_replenishment_recommendations(
    mock_get_high_risk_inventory,
    sample_record
):
    mock_get_high_risk_inventory.return_value = [sample_record]

    service = InventoryService()

    recommendations = service.get_replenishment_recommendations(
        date="2022-01-01",
        store_id="S001",
        lead_time_days=3,
        safety_stock_days=2
    )

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation["product_id"] == "P0001"
    assert recommendation["inventory_level"] == 150
    assert recommendation["stockout_risk"] == "High"
    assert recommendation["recommended_order"] == 350

    mock_get_high_risk_inventory.assert_called_once_with(
        date="2022-01-01",
        store_id="S001"
    )


@patch.object(InventoryService, "get_high_risk_inventory")
def test_empty_replenishment_recommendations(
    mock_get_high_risk_inventory
):
    mock_get_high_risk_inventory.return_value = []

    service = InventoryService()

    recommendations = service.get_replenishment_recommendations(
        date="2022-01-01",
        store_id="S001"
    )

    assert recommendations == []


@patch.object(InventoryService, "get_high_risk_inventory")
def test_negative_lead_time_replenishment(
    mock_get_high_risk_inventory
):
    service = InventoryService()

    with pytest.raises(ValueError):
        service.get_replenishment_recommendations(
            date="2022-01-01",
            store_id="S001",
            lead_time_days=-1
        )

    mock_get_high_risk_inventory.assert_not_called()
