import plotly.express as px
import pandas as pd

def plot_revenue_by_store(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="store_id",
        y="estimated_revenue",
        title="Estimated Revenue by Store",
        labels={
            "store_id": "Store",
            "estimated_revenue": "Estimated Revenue"
        },
        text="estimated_revenue"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Store",
        yaxis_title="Estimated Revenue",
        template="plotly_white"
    )

    return fig


def plot_revenue_by_category(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="category_name",
        y="estimated_revenue",
        title="Estimated Revenue by Category",
        labels={
            "category_name": "Category",
            "estimated_revenue": "Estimated Revenue"
        },
        text="estimated_revenue"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Estimated Revenue",
        template="plotly_white"
    )

    return fig


def plot_monthly_sales_trends(df: pd.DataFrame):
    fig = px.line(
        df,
        x="month",
        y="estimated_revenue",
        title="Monthly Estimated Revenue",
        markers=True,
        labels={
            "month": "Month",
            "estimated_revenue": "Estimated Revenue"
        }
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Estimated Revenue",
        template="plotly_white"
    )

    return fig

def plot_stock_coverage_by_store(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="store_id",
        y="avg_stock_coverage_days",
        title="Average Stock Coverage by Store",
        labels={
            "store_id": "Store",
            "avg_stock_coverage_days": "Coverage (days)"
        },
        text="avg_stock_coverage_days"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Store",
        yaxis_title="Average Stock Coverage (days)"
    )

    return fig

def plot_low_stock_rate_by_store(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="store_id",
        y="low_stock_rate_pct",
        title="Low Stock Rate by Store",
        labels={
            "store_id": "Store",
            "low_stock_rate_pct": "Low Stock Rate (%)"
        },
        text="low_stock_rate_pct"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Low Stock Rate (%)",
        yaxis_range=[0, 100]
    )

    return fig