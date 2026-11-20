
import pytest
from models.inventory import InventoryRecord


@pytest.fixture
def sample_inventory():
    return InventoryRecord(
        date="2022-01-01",
        product_id="P0001",
        store_id="S001",
        inventory_level=30,
        units_sold=10,
        demand_forecast=15.0
    )


def test_low_stock(sample_inventory):
    assert sample_inventory.is_low_stock() is True


def test_stock_coverage(sample_inventory):
    assert sample_inventory.stock_coverage_days() == 2.0


def test_not_low_stock():
    record = InventoryRecord(
        date="2022-01-01",
        product_id="P0002",
        store_id="S001",
        inventory_level=100,
        units_sold=10,
        demand_forecast=20.0
    )

    assert record.is_low_stock() is False


def test_zero_demand():
    record = InventoryRecord(
        date="2022-01-01",
        product_id="P0003",
        store_id="S001",
        inventory_level=100,
        units_sold=0,
        demand_forecast=0.0
    )

    assert record.stock_coverage_days() is None


@pytest.mark.parametrize(
    "inventory_level, demand_forecast, expected_risk",
    [
        (10, 10.0, "High"),
        (30, 10.0, "Medium"),
        (100, 10.0, "Low"),
        (100, 0.0, "Unknown"),
    ]
)
def test_stockout_risk(
    inventory_level,
    demand_forecast,
    expected_risk
):
    record = InventoryRecord(
        date="2022-01-01",
        product_id="P0001",
        store_id="S001",
        inventory_level=inventory_level,
        units_sold=5,
        demand_forecast=demand_forecast
    )

    assert record.stockout_risk() == expected_risk


@pytest.mark.parametrize(
    "inventory_level, demand_forecast, expected",
    [
        (150, 100.0, 350),
        (600, 100.0, 0),
        (0, 10.0, 50),
        (100, 0.0, 0),
        (100, 10.1, 0),
    ]
)
def test_recommended_order_quantity(
    inventory_level,
    demand_forecast,
    expected
):
    record = InventoryRecord(
        date="2022-01-01",
        product_id="P0001",
        store_id="S001",
        inventory_level=inventory_level,
        units_sold=5,
        demand_forecast=demand_forecast
    )

    assert record.recommended_order_quantity() == expected


def test_negative_lead_time():
    record = InventoryRecord(
        date="2022-01-01",
        product_id="P0001",
        store_id="S001",
        inventory_level=100,
        units_sold=5,
        demand_forecast=10.0
    )

    with pytest.raises(ValueError):
        record.recommended_order_quantity(lead_time_days=-1)
