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
