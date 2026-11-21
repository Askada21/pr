import streamlit as st

from assets.theme import load_custom_css

st.set_page_config(
    page_title="Smart Inventory System",
    page_icon="📦",
    layout="wide"
)

load_custom_css()


st.title("Smart Inventory Management System")

st.markdown(
    """
    Welcome to the Smart Inventory & Supply Chain
    Management Dashboard.

    This application helps businesses monitor sales,
    identify inventory risks, and generate data-driven
    replenishment recommendations.
    """
)

st.subheader("System Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sales Analytics")
    st.write(
        "Explore estimated revenue by store and category, "
        "and analyse monthly sales trends."
    )

with col2:
    st.markdown("### Inventory Management")
    st.write(
        "Identify stockout risks and calculate "
        "recommended replenishment quantities."
    )

st.info(
    "Use the sidebar to navigate between dashboard pages."
)
