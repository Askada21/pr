from services.inventory_service import InventoryService

service = InventoryService()

recommendations = service.get_replenishment_recommendations(
    date="2022-01-01",
    store_id="S001",
    lead_time_days=3,
    safety_stock_days=2
)

print("Total recommendations:", len(recommendations))

for item in recommendations:
    print(
        "Product:", item["product_id"],
        "| Current stock:", item["inventory_level"],
        "| Coverage:", round(item["stock_coverage_days"], 2),
        "| Risk:", item["stockout_risk"],
        "| Recommended order:", item["recommended_order"]
    )