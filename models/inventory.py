class InventoryRecord:
    def __init__(
        self,
        date: str,
        product_id: str,
        store_id: str,
        inventory_level: int,
        units_sold: int,
        demand_forecast: float
    ):
        self.date = date
        self.product_id = product_id
        self.store_id = store_id
        self.inventory_level = inventory_level
        self.units_sold = units_sold
        self.demand_forecast = demand_forecast

    def is_low_stock(self, threshold: int = 50) -> bool:
        return self.inventory_level < threshold

    def stock_coverage_days(self) -> float | None:
        if self.demand_forecast <= 0:
            return None

        return self.inventory_level / self.demand_forecast

    def __repr__(self):
        return (
            f"InventoryRecord("
            f"product_id={self.product_id!r}, "
            f"store_id={self.store_id!r}, "
            f"inventory_level={self.inventory_level})"
        )