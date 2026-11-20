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

print("\nMonthly Sales Trends:")

monthly_df = analytics.get_monthly_sales_trends()

print(monthly_df.head(12))

print("\nTotal months:", len(monthly_df))

assert monthly_df["month"].is_monotonic_increasing
print("Monthly dates are correctly sorted!")

if not monthly_df.empty:
    print(
        "Highest revenue month:",
        monthly_df.loc[
            monthly_df["estimated_revenue"].idxmax(),
            "month"
        ]
    )