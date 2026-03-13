import streamlit as st
import plotly.express as px

df = st.session_state["filtered_df"]

st.header("Sales Analytics")

col1,col2 = st.columns(2)

category_sales = df.groupby("Category")["Sales"].sum().reset_index()

fig1 = px.bar(category_sales,x="Category",y="Sales",color="Category")

col1.plotly_chart(fig1,use_container_width=True)

region_sales = df.groupby("Region")["Sales"].sum().reset_index()

fig2 = px.bar(region_sales,x="Region",y="Sales",color="Region")

col2.plotly_chart(fig2,use_container_width=True)

city_sales = df.groupby("City")["Sales"].sum().reset_index()

city_sales = city_sales.sort_values("Sales",ascending=False).head(10)

fig3 = px.bar(city_sales,x="City",y="Sales",title="Top Cities")

st.plotly_chart(fig3,use_container_width=True)