from services.inventory_service import InventoryService

service = InventoryService()

records = service.get_high_risk_inventory(
    date="2022-01-01",
    store_id="S001"
)

print("High-risk products:", len(records))

for record in records:
    print(
        record.product_id,
        "Inventory:", record.inventory_level,
        "Coverage:", round(record.stock_coverage_days(), 2),
        "Risk:", record.stockout_risk()
    )