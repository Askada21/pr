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

# Inventory Risk & Replenishment Dashboard
from services.inventory_service import InventoryService

st.divider()
st.subheader("Inventory Risk & Replenishment")

st.write(
    "Identify high-risk products and calculate "
    "recommended replenishment quantities."
)

# Store and date filters
col1, col2 = st.columns(2)

with col1:
    store_id = st.selectbox(
        "Select Store",
        options=["S001", "S002", "S003", "S004", "S005"]
    )

with col2:
    selected_date = st.date_input(
        "Select Date",
        value=pd.to_datetime("2022-01-01").date(),
        min_value=pd.to_datetime("2022-01-01").date(),
        max_value=pd.to_datetime("2023-12-31").date()
    )

# Replenishment settings
st.markdown("#### Replenishment Settings")

col3, col4 = st.columns(2)

with col3:
    lead_time_days = st.number_input(
        "Lead Time (days)",
        min_value=0,
        max_value=30,
        value=3,
        step=1
    )

with col4:
    safety_stock_days = st.number_input(
        "Safety Stock (days)",
        min_value=0,
        max_value=30,
        value=2,
        step=1
    )

# Run analysis
if st.button("Generate Replenishment Plan"):
    inventory_service = InventoryService()

    try:
        recommendations = (
            inventory_service.get_replenishment_recommendations(
                date=str(selected_date),
                store_id=store_id,
                lead_time_days=int(lead_time_days),
                safety_stock_days=int(safety_stock_days)
            )
        )

        if recommendations:
            risk_df = pd.DataFrame(recommendations)

            # Summary metrics
            high_risk_count = len(risk_df)

            total_order_quantity = int(
                risk_df["recommended_order"].sum()
            )

            avg_coverage = risk_df[
                "stock_coverage_days"
            ].mean()

            metric1, metric2, metric3 = st.columns(3)

            with metric1:
                st.metric(
                    "High-Risk Products",
                    high_risk_count
                )

            with metric2:
                st.metric(
                    "Recommended Units to Order",
                    f"{total_order_quantity:,}"
                )

            with metric3:
                st.metric(
                    "Average Stock Coverage",
                    f"{avg_coverage:.2f} days"
                )

            # Replenishment table
            st.markdown("#### Replenishment Recommendations")

            st.dataframe(
                risk_df,
                width="stretch",
                hide_index=True
            )

            # CSV export
            csv_data = risk_df.to_csv(index=False)

            st.download_button(
                label="Download Replenishment Plan (CSV)",
                data=csv_data,
                file_name=(
                    f"replenishment_{store_id}_"
                    f"{selected_date}.csv"
                ),
                mime="text/csv"
            )

        else:
            st.success(
                "No high-risk products found "
                "for the selected store and date."
            )

    except Exception:
        st.error(
            "Unable to generate replenishment plan. "
            "Please check the database connection."
        )
