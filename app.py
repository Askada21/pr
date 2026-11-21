import pandas as pd
import streamlit as st

from analytics.sales_analytics import SalesAnalytics
from analytics.visualizations import (
    plot_revenue_by_store,
    plot_revenue_by_category,
    plot_monthly_sales_trends
)

# Page configuration
st.set_page_config(
    page_title="Smart Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

# Dashboard title
st.title("Smart Inventory Dashboard")
st.caption("Inventory Management & Sales Analytics")

# Load analytics data
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
    st.error(
        "Unable to load sales data. "
        "Please check the PostgreSQL connection."
    )
    st.stop()

# KPI section
st.subheader("Sales Overview")

total_revenue = store_df["estimated_revenue"].sum()
total_units = store_df["total_units_sold"].sum()
total_stores = store_df["store_id"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Estimated Revenue",
        f"{total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "Units Sold",
        f"{total_units:,}"
    )

with col3:
    st.metric(
        "Active Stores",
        total_stores
    )

# Monthly revenue trend
st.subheader("Monthly Sales Trends")

monthly_fig = plot_monthly_sales_trends(monthly_df)

st.plotly_chart(
    monthly_fig,
    width="stretch"
)

# Store and category comparisons
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by Store")

    store_fig = plot_revenue_by_store(store_df)

    st.plotly_chart(
        store_fig,
        width="stretch"
    )

with col_right:
    st.subheader("Revenue by Category")

    category_fig = plot_revenue_by_category(category_df)

    st.plotly_chart(
        category_fig,
        width="stretch"
    )

# Raw data section
with st.expander("View Sales Data"):
    st.write("Revenue by Store")
    st.dataframe(store_df, width="stretch")

    st.write("Revenue by Category")
    st.dataframe(category_df, width="stretch")

    st.write("Monthly Sales Trends")
    st.dataframe(monthly_df, width="stretch")

# Inventory Risk Dashboard
st.divider()
st.subheader("Inventory Risk Analysis")

st.write(
    "Identify products at risk of running out of stock "
    "and review replenishment recommendations."
)

store_id = st.selectbox(
    "Select Store",
    options=["S001", "S002", "S003", "S004", "S005"]
)

selected_date = st.date_input(
    "Select Date",
    value=pd.to_datetime("2022-01-01").date(),
    min_value=pd.to_datetime("2022-01-01").date(),
    max_value=pd.to_datetime("2023-12-31").date()
)

if st.button("Analyse Inventory"):
    from services.inventory_service import InventoryService

    inventory_service = InventoryService()

    try:
        recommendations = (
            inventory_service.get_replenishment_recommendations(
                date=str(selected_date),
                store_id=store_id
            )
        )

        if recommendations:
            risk_df = pd.DataFrame(recommendations)

            st.metric(
                "High-Risk Products",
                len(risk_df)
            )

            st.dataframe(
                risk_df,
                width="stretch"
            )

        else:
            st.success(
                "No high-risk products found "
                "for this store and date."
            )

    except Exception:
        st.error(
            "Unable to analyse inventory. "
            "Please check the database connection."
        )

