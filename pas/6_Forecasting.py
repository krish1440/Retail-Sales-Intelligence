import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA

df = st.session_state["filtered_df"]

st.header("Sales Forecast")

ts = df.groupby("Order Date")["Sales"].sum()

model = ARIMA(ts,order=(1,1,1))

fit = model.fit()

forecast = fit.forecast(steps=12)

forecast_df = forecast.reset_index()

forecast_df.columns=["Date","Forecast"]

fig = px.line(forecast_df,x="Date",y="Forecast")

st.plotly_chart(fig,use_container_width=True)