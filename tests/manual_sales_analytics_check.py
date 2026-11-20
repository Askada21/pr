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

print("\nRevenue by Category:")

category_df = analytics.get_revenue_by_category()

print(category_df)
print("\nNumber of categories:", len(category_df))

if not category_df.empty:
    print(
        "Top-performing category:",
        category_df.iloc[0]["category_name"]
    )