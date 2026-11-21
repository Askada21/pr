import pandas as pd
import streamlit as st

from services.inventory_service import InventoryService
from assets.theme import load_custom_css
from analytics.inventory_analytics import InventoryAnalytics
from analytics.visualizations import plot_stock_coverage_by_store

load_custom_css()

st.title("Inventory Management")
st.caption("Stockout Risk & Replenishment Planning")

st.write(
    "Monitor high-risk inventory and generate "
    "data-driven replenishment recommendations."
)

# Inventory filters
col1, col2 = st.columns(2)

with col1:
    store_id = st.selectbox(
        "Select Store",
        ["S001", "S002", "S003", "S004", "S005"]
    )

with col2:
    selected_date = st.date_input(
        "Select Date",
        value=pd.Timestamp("2022-01-01").date(),
        min_value=pd.Timestamp("2022-01-01").date(),
        max_value=pd.Timestamp("2023-12-31").date()
    )

# Replenishment parameters
st.subheader("Replenishment Settings")

col3, col4 = st.columns(2)

with col3:
    lead_time_days = st.number_input(
        "Lead Time (days)",
        min_value=0,
        max_value=30,
        value=3
    )

with col4:
    safety_stock_days = st.number_input(
        "Safety Stock (days)",
        min_value=0,
        max_value=30,
        value=2
    )

if st.button("Generate Replenishment Plan"):
    service = InventoryService()

    try:
        recommendations = (
            service.get_replenishment_recommendations(
                date=str(selected_date),
                store_id=store_id,
                lead_time_days=int(lead_time_days),
                safety_stock_days=int(safety_stock_days)
            )
        )

        if recommendations:
            risk_df = pd.DataFrame(recommendations)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "High-Risk Products",
                    len(risk_df)
                )

            with col2:
                st.metric(
                    "Recommended Units",
                    int(risk_df["recommended_order"].sum())
                )

            with col3:
                st.metric(
                    "Average Coverage",
                    f"{risk_df['stock_coverage_days'].mean():.2f} days"
                )

            st.subheader("Replenishment Recommendations")

            st.dataframe(
                risk_df,
                width="stretch",
                hide_index=True
            )

            st.download_button(
                "Download CSV",
                data=risk_df.to_csv(index=False),
                file_name=f"replenishment_{store_id}_{selected_date}.csv",
                mime="text/csv"
            )

        else:
            st.success("No high-risk products found.")

    except Exception:
        st.error("Unable to generate replenishment plan.")

# Inventory Performance Analytics
st.divider()
st.subheader("Inventory Performance")

st.caption(
    "Historical average stock coverage across all "
    "available dates and products."
)


@st.cache_data(ttl=300)
def load_inventory_analytics():
    analytics = InventoryAnalytics()
    return analytics.get_stock_coverage_by_store()


try:
    coverage_df = load_inventory_analytics()

    if not coverage_df.empty:
        # KPI calculations
        stores_analysed = coverage_df["store_id"].nunique()

        avg_coverage = coverage_df[
            "avg_stock_coverage_days"
        ].mean()

        lowest_coverage_store = coverage_df.iloc[0]["store_id"]

        # KPI cards
        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:
            st.metric("Stores Analysed", stores_analysed)

        with kpi2:
            st.metric(
                "Average Coverage",
                f"{avg_coverage:.2f} days"
            )

        with kpi3:
            st.metric(
                "Lowest Coverage Store",
                lowest_coverage_store
            )

        # Plotly chart
        coverage_fig = plot_stock_coverage_by_store(
            coverage_df
        )

        st.plotly_chart(
            coverage_fig,
            width="stretch"
        )

        # Data table
        with st.expander("View Coverage Data"):
            st.dataframe(
                coverage_df,
                width="stretch",
                hide_index=True
            )

    else:
        st.info("No inventory coverage data available.")

except Exception:
    st.error(
        "Unable to load inventory performance data."
    )
