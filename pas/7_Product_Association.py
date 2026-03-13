import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px

df = st.session_state["filtered_df"]

st.header("Product Association Analysis")

st.markdown("""
This analysis identifies products that are frequently purchased together.
Retailers use this insight to improve product recommendations and cross-selling strategies.
""")

# Create basket table
basket = (
    df.groupby(["Order ID", "Sub-Category"])["Sales"]
    .sum()
    .unstack()
    .fillna(0)
)

basket = basket.applymap(lambda x: True if x > 0 else False)

# Run Apriori
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

st.subheader("Top Product Associations")

# SEC FIX: Clean frozenset for display
rules_display = rules.copy()
rules_display["antecedents"] = rules_display["antecedents"].apply(lambda x: ', '.join(list(x)))
rules_display["consequents"] = rules_display["consequents"].apply(lambda x: ', '.join(list(x)))

st.dataframe(
    rules_display[["antecedents","consequents","support","confidence","lift"]].head(10),
    use_container_width=True
)

st.markdown("### 💡 Association Insights")
st.info("""
- **Lift Value**: Measures the strength of association. A lift > 1 means products are positively correlated.
- **Support**: Shows how frequently the product combination appears in total orders.
- **Actionable Insight**: Target the top rules for bundle deals or recommendation engine improvements.
""")

# Convert for visualization
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
    title="Product Association Strength",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)