import pandas as pd
import streamlit as st

from assets.theme import load_custom_css
from analytics.sales_analytics import SalesAnalytics
from analytics.visualizations import (
    plot_revenue_by_store,
    plot_revenue_by_category,
    plot_monthly_sales_trends
)

load_custom_css()

st.title("Sales Analytics")
st.caption("Revenue Performance & Sales Trends")

@st.cache_data(ttl=300)
def load_sales_data():
    analytics = SalesAnalytics()

    store_df = analytics.get_revenue_by_store()
    category_df = analytics.get_revenue_by_category()
    monthly_df = analytics.get_monthly_sales_trends()

    for df in [store_df, category_df, monthly_df]:
        df["estimated_revenue"] = pd.to_numeric(
            df["estimated_revenue"]
        )

    return store_df, category_df, monthly_df

try:
    store_df, category_df, monthly_df = load_sales_data()

except Exception:
    st.error("Unable to load sales data.")
    st.stop()

# KPI cards
total_revenue = store_df["estimated_revenue"].sum()
total_units = store_df["total_units_sold"].sum()
total_stores = store_df["store_id"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Estimated Revenue",
        f"{total_revenue / 1_000_000:,.2f}M"
    )

with col2:
    st.metric(
        "Units Sold",
        f"{total_units:,}"
    )

with col3:
    st.metric(
        "Stores",
        total_stores
    )

# Monthly sales
st.subheader("Monthly Revenue Trend")

st.plotly_chart(
    plot_monthly_sales_trends(monthly_df),
    width="stretch"
)

# Comparison charts
col_left, col_right = st.columns(2)

with col_left:
    st.plotly_chart(
        plot_revenue_by_store(store_df),
        width="stretch"
    )

with col_right:
    st.plotly_chart(
        plot_revenue_by_category(category_df),
        width="stretch"
    )

# Data tables
with st.expander("View Sales Data"):
    st.dataframe(store_df, width="stretch")
    st.dataframe(category_df, width="stretch")
    st.dataframe(monthly_df, width="stretch")
