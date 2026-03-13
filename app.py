import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from mlxtend.frequent_patterns import apriori, association_rules

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Intelligence Dashboard",
    layout="wide"
)

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/retail_sales_cleaned.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df

df = load_data()

# -------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------

st.sidebar.title("Dashboard Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

year = st.sidebar.multiselect(
    "Year",
    df["Order Year"].unique(),
    default=df["Order Year"].unique()
)

df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Order Year"].isin(year))
]

# -------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Executive Overview",
        "Sales Analytics",
        "Customer Analytics",
        "Product Insights",
        "Operations",
        "Forecasting",
        "Product Associations"
    ]
)

# -------------------------------------------------------
# TITLE
# -------------------------------------------------------

st.title("Retail Sales Intelligence Dashboard")

# -------------------------------------------------------
# EXECUTIVE OVERVIEW
# -------------------------------------------------------

if page == "Executive Overview":

    st.header("Executive Overview")

    total_sales = df["Sales"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer Name"].nunique()
    avg_order = df["Sales"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Customers", total_customers)
    col4.metric("Avg Order Value", f"${avg_order:,.2f}")

    st.markdown("### 📊 Executive Insights")
    
    # Pareto Analysis Calculation
    sales_sorted = df.sort_values(by='Sales', ascending=False)
    sales_sorted['Cumulative Sales'] = sales_sorted['Sales'].cumsum()
    total_sales_sum = sales_sorted['Sales'].sum()
    sales_sorted['Cumulative %'] = 100 * sales_sorted['Cumulative Sales'] / total_sales_sum
    
    orders_80 = sales_sorted[sales_sorted['Cumulative %'] <= 80].shape[0]
    perc_80 = (orders_80 / total_orders) * 100 if total_orders > 0 else 0
    
    ins_col1, ins_col2 = st.columns([1, 1])
    
    with ins_col1:
        st.info(f"""
        **The 80/20 Rule (Pareto Principle):**
        Approximately **{perc_80:.1f}%** of your orders contribute to **80%** of your total revenue. 
        This suggests a high concentration of value in a small segment of transactions.
        """)
        
    with ins_col2:
        st.success(f"""
        **Business Performance:**
        Total revenue is currently **${total_sales:,.0f}** across **{total_orders}** orders. 
        Average transaction value stands at **${avg_order:,.2f}**.
        """)

    st.markdown("---")

    col_trend, col_pareto = st.columns(2)

    with col_trend:
        sales_trend = df.groupby("Order Date")["Sales"].sum().reset_index()
        fig = px.line(
            sales_trend,
            x="Order Date",
            y="Sales",
            title="Sales Trend Over Time",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_pareto:
        fig_pareto = px.area(
            sales_sorted.reset_index(),
            y="Cumulative %",
            title="Revenue Concentration (Pareto Chart)",
            labels={"index": "Orders (Sorted by Value)", "Cumulative %": "Cumulative Revenue %"},
            template="plotly_dark"
        )
        fig_pareto.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Revenue Threshold")
        st.plotly_chart(fig_pareto, use_container_width=True)

# -------------------------------------------------------
# SALES ANALYTICS
# -------------------------------------------------------

elif page == "Sales Analytics":

    st.header("Sales Analytics")

    col1, col2 = st.columns(2)

    category_sales = df.groupby("Category")["Sales"].sum().reset_index()

    fig1 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    col1.plotly_chart(fig1, use_container_width=True)

    region_sales = df.groupby("Region")["Sales"].sum().reset_index()

    fig2 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region",
        template="plotly_dark"
    )

    col2.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📈 Deep Dive: Sales Distribution & High Value Orders")
    
    div_col1, div_col2 = st.columns([2, 1])
    
    with div_col1:
        fig_dist = px.histogram(
            df, 
            x="Sales", 
            nbins=50, 
            marginal="box",
            title="Transaction Value Distribution (Long Tail Analysis)",
            template="plotly_dark",
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        st.write("""
        **Analysis:** The distribution exhibits a heavy 'Long Tail'. Most transactions are low-value, 
        but the business is significantly impacted by rare, high-value transactions that drive the bulk of revenue.
        """)

    with div_col2:
        st.subheader("Top 10 High Value Orders")
        high_val = df.sort_values(by="Sales", ascending=False).head(10)[["Order ID", "Customer Name", "Sales"]]
        st.dataframe(high_val, use_container_width=True)
        st.write("""
        **Insight:** These specific orders are critical revenue drivers. Retaining these customers is vital for bottom-line stability.
        """)

# -------------------------------------------------------
# CUSTOMER ANALYTICS
# -------------------------------------------------------

elif page == "Customer Analytics":

    st.header("Customer Analytics")

    top_customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_customers,
        x="Customer Name",
        y="Sales",
        title="Top Customers"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 👥 Customer Behavior Insight")
    st.write(f"""
    **Value Concentration:** The top customers like **{top_customers.iloc[0]['Customer Name']}** are primary revenue contributors. 
    Focusing on VIP loyalty programs for high-value clients can significantly reduce customer acquisition costs (CAC).
    """)

# -------------------------------------------------------
# PRODUCT INSIGHTS
# -------------------------------------------------------

elif page == "Product Insights":

    st.header("Product Insights")

    sub_sales = df.groupby("Sub-Category")["Sales"].sum().reset_index()
    sub_sales = sub_sales.sort_values("Sales", ascending=False)

    fig = px.bar(
        sub_sales,
        x="Sub-Category",
        y="Sales",
        title="Product Demand",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📦 Inventory & Demand Strategy")
    st.info(f"""
    **Performance analysis:** {sub_sales.iloc[0]['Sub-Category']} is the highest demand sub-category. 
    **Recommendation:** Align purchasing cycles with these volume trends to minimize holding costs and optimize warehouse space.
    """)

# -------------------------------------------------------
# OPERATIONS
# -------------------------------------------------------

elif page == "Operations":

    st.header("Shipping Performance")

    ship_delay = df.groupby("Ship Mode")["Shipping Delay"].mean().reset_index()

    fig = px.bar(
        ship_delay,
        x="Ship Mode",
        y="Shipping Delay",
        title="Average Shipping Delay",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🚚 Logisitics Insight")
    mean_delay = df['Shipping Delay'].mean()
    st.success(f"""
    **Efficiency Check:** The overall average shipping delay is **{mean_delay:.1f} days**. 
    Optimizing {ship_delay.iloc[0]['Ship Mode']} and identifying bottlenecks in slower modes could improve 
    customer satisfaction and lower logistics overhead.
    """)

# -------------------------------------------------------
# FORECASTING
# -------------------------------------------------------

elif page == "Forecasting":

    st.header("Sales Forecast")

    ts = df.groupby("Order Date")["Sales"].sum()

    model = ARIMA(ts, order=(1,1,1))
    fit = model.fit()

    forecast = fit.forecast(steps=12)

    forecast_df = forecast.reset_index()
    forecast_df.columns = ["Date","Forecast"]

    fig = px.line(
        forecast_df,
        x="Date",
        y="Forecast",
        title="Next 12 Months Forecast",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔮 Predictive Commentary")
    st.warning("""
    **Forecasting Note:** This model uses the ARIMA algorithm. The projected trend helps in capacity planning. 
    Sudden external market changes or supply chain disruptions may require model re-calibration for better accuracy.
    """)

# -------------------------------------------------------
# PRODUCT ASSOCIATIONS
# -------------------------------------------------------

elif page == "Product Associations":

    st.header("Product Association Analysis")

    basket = (
        df.groupby(["Order ID","Sub-Category"])["Sales"]
        .sum()
        .unstack()
        .fillna(0)
    )

    basket = basket.applymap(lambda x: True if x > 0 else False)

    frequent_itemsets = apriori(
        basket,
        min_support=0.02,
        use_colnames=True
    )

    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1
    )

    rules = rules.sort_values("lift", ascending=False)

    # SEC FIX: Clean frozenset for display
    rules_display = rules.copy()
    rules_display["antecedents"] = rules_display["antecedents"].apply(lambda x: ', '.join(list(x)))
    rules_display["consequents"] = rules_display["consequents"].apply(lambda x: ', '.join(list(x)))

    st.dataframe(
        rules_display[["antecedents","consequents","support","confidence","lift"]].head(10),
        use_container_width=True
    )

    st.markdown("### 💡 Association Insights")
    st.write("""
    - **Lift > 1.0**: Indicates that the items are more likely to be bought together than independently. The higher the lift, the stronger the association.
    - **Confidence**: The probability that the second item is bought when the first one is.
    - **Strategy**: Use these associations for cross-selling (e.g., placing frequently bought items near each other or recommending them during checkout).
    """)

    # Conversion for visualization
    rules_viz = rules.head(10).copy()
    rules_viz["antecedents"] = rules_viz["antecedents"].apply(lambda x: ', '.join(list(x)))
    rules_viz["consequents"] = rules_viz["consequents"].apply(lambda x: ', '.join(list(x)))

    fig = px.scatter(
        rules_viz,
        x="support",
        y="confidence",
        size="lift",
        color="lift",
        hover_data=["antecedents","consequents"],
        title="Product Association Strength (Lift Analysis)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)