import pandas as pd

from analytics.sales_analytics import SalesAnalytics
from analytics.visualizations import (
    plot_revenue_by_store,
    plot_revenue_by_category,
    plot_monthly_sales_trends
)

# 1. Create analytics object
analytics = SalesAnalytics()

# 2. Retrieve data from PostgreSQL
store_df = analytics.get_revenue_by_store()
category_df = analytics.get_revenue_by_category()
monthly_df = analytics.get_monthly_sales_trends()

# 3. Convert revenue columns to numeric values
store_df["estimated_revenue"] = pd.to_numeric(
    store_df["estimated_revenue"]
)

category_df["estimated_revenue"] = pd.to_numeric(
    category_df["estimated_revenue"]
)

monthly_df["estimated_revenue"] = pd.to_numeric(
    monthly_df["estimated_revenue"]
)

# 4. Display data in terminal
print("\nRevenue by Store:")
print(store_df)

print("\nRevenue by Category:")
print(category_df)

print("\nMonthly Sales Trends:")
print(monthly_df.head(12))

# 5. Create Plotly figures
store_fig = plot_revenue_by_store(store_df)

category_fig = plot_revenue_by_category(category_df)

monthly_fig = plot_monthly_sales_trends(monthly_df)

# 6. Open interactive charts in browser
store_fig.show(renderer="browser")

category_fig.show(renderer="browser")

monthly_fig.show(renderer="browser")

print("\nAll visualizations generated successfully!")
