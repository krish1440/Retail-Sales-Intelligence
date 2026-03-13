import streamlit as st
import plotly.express as px

df = st.session_state["filtered_df"]

st.header("Customer Analytics")

rfm = df.groupby("Customer Name").agg({
    "Order Date":"max",
    "Order ID":"count",
    "Sales":"sum"
})

rfm.columns=["Recency","Frequency","Monetary"]

top_customers = rfm.sort_values("Monetary",ascending=False).head(10)

fig = px.bar(
    top_customers,
    y=top_customers.index,
    x="Monetary",
    orientation="h",
    title="Top Customers"
)

st.plotly_chart(fig,use_container_width=True)