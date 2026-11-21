from analytics.inventory_analytics import InventoryAnalytics

def main():
    analytics = InventoryAnalytics()

    df = analytics.get_stockout_rate_by_store()

    print("\nZero-Stock Rate by Store:")
    print(df.to_string(index=False))

    assert len(df) == 5
    assert df["zero_stock_rate_pct"].between(0, 100).all()

    print("\nStockout analytics check passed!")


if __name__ == "__main__":
    main()
