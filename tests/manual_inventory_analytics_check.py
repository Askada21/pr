from analytics.inventory_analytics import InventoryAnalytics

analytics = InventoryAnalytics()

df = analytics.get_stock_coverage_by_store()

print("\nAverage Stock Coverage by Store:")
print(df)

assert len(df) == 5
assert df["avg_stock_coverage_days"].notna().all()

print("\nInventory analytics check passed!")
