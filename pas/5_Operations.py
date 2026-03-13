import streamlit as st
import plotly.express as px

df = st.session_state["filtered_df"]

st.header("Shipping Performance")

ship_delay = df.groupby("Ship Mode")["Shipping Delay"].mean().reset_index()

fig = px.bar(
    ship_delay,
    x="Ship Mode",
    y="Shipping Delay",
    title="Average Shipping Delay"
)

st.plotly_chart(fig,use_container_width=True)