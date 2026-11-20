from services.inventory_service import InventoryService


service = InventoryService()

record = service.get_inventory_record(
    date="2022-01-01",
    product_id="P0001",
    store_id="S001"
)

if record is not None:
    print("Record found!")
    print(record)
    print("Low stock:", record.is_low_stock())
    print("Stock coverage:", record.stock_coverage_days())
else:
    print("Record not found.")