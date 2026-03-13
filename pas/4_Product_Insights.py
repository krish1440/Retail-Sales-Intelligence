import streamlit as st
import plotly.express as px

df = st.session_state["filtered_df"]

st.header("Product Insights")

sub_sales = df.groupby("Sub-Category")["Sales"].sum().reset_index()

sub_sales = sub_sales.sort_values("Sales",ascending=False)

fig = px.bar(
    sub_sales,
    x="Sub-Category",
    y="Sales",
    title="Product Demand"
)

st.plotly_chart(fig,use_container_width=True)