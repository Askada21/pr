from analytics.sales_analytics import SalesAnalytics

analytics = SalesAnalytics()

df = analytics.get_revenue_by_store()

print("Revenue by Store:")
print(df)

print("\nNumber of stores:", len(df))

if not df.empty:
    print(
        "\nTop-performing store:",
        df.iloc[0]["store_id"]
    )
