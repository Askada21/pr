from models.inventory import InventoryRecord

record = InventoryRecord(
    date="2026-01-01",
    product_id="P0001",
    store_id="S001",
    inventory_level=30,
    units_sold=10,
    demand_forecast=15.0
)

print(record)

print("Low stock:", record.is_low_stock())

print("Stock coverage:", record.stock_coverage_days())