import streamlit as st
import plotly.express as px

df = st.session_state["filtered_df"]

st.header("Executive Overview")

total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer Name"].nunique()
avg_order = df["Sales"].mean()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Sales",f"${total_sales:,.0f}")
col2.metric("Total Orders",total_orders)
col3.metric("Customers",total_customers)
col4.metric("Avg Order Value",f"${avg_order:,.2f}")

st.markdown("---")

sales_trend = df.groupby("Order Date")["Sales"].sum().reset_index()

fig = px.line(
    sales_trend,
    x="Order Date",
    y="Sales",
    title="Sales Trend"
)

st.plotly_chart(fig,use_container_width=True)