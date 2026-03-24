# 🚀 Retail Sales Intelligence & Business Analytics Dashboard

An advanced, interactive Streamlit-powered dashboard designed for deep-dive retail data analysis. This project transforms raw superstore sales data into actionable business intelligence using statistical analysis, machine learning forecasting, and market basket analysis.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

---

## 📊 Data Source

The analysis is based on the **Global Superstore Sales** dataset.
- **Dataset Link:** [Kaggle - Sales Forecasting Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)
- **Content:** Historical sales data including orders, returns, and customer information across various regions and categories.

---

## 🌟 Key Features

### 📈 Executive Business Intelligence
- **Pareto Analysis (80/20 Rule):** Automatically detects revenue concentration and identifies the vital few transactions driving most of the value.
- **Dynamic Sales Trends:** High-level temporal analysis of revenue streams.
- **Interactive Metrics:** Real-time calculation of AOV (Average Order Value), total revenue, and customer count.

### 🔍 Advanced Sales Analytics
- **Long-Tail Distribution:** Detailed histogram with marginal box plots to analyze transaction value skewness and identify high-value outliers.
- **Regional Performance:** Geographic breakdown of sales across different markets.
- **High-Value Order Tracking:** Dedicated focus on top-tier revenue transactions for retention strategy.

### 🧠 Algorithmic Insights
- **AI-Powered Forecasting:** Uses **ARIMA** (AutoRegressive Integrated Moving Average) to project future sales trends for the next 12 months.
- **Market Basket Analysis (Apriori):** Identifies hidden product associations using **Support, Confidence, and Lift** metrics to drive cross-selling strategies.
- **Shipping Performance:** Analyzes logistics delays across different delivery modes to optimize supply chain efficiency.

### 💡 Data-Driven Recommendations
- Each section provides **Automated Business Insights** derived from the underlying data, suggesting inventory strategies, VIP customer programs, and more.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (Interactive Dashboard)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualizations:** [Plotly Express](https://plotly.com/python/), [Seaborn](https://seaborn.pydata.org/)
- **Machine Learning/Stats:** [Statsmodels](https://www.statsmodels.org/) (ARIMA), [MLxtend](http://rasbt.github.io/mlxtend/) (Apriori)
- **Styling:** Custom CSS for a premium dark-mode aesthetic.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/krish1440/Retail-Sales-Intelligence.git
   cd Retail-Sales-Intelligence
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Structure

```text
├── app.py              # Main dashboard script
├── data/               # Raw and cleaned datasets
├── assets/             # Custom CSS and static assets
├── notebooks/          # Exploratory Data Analysis (Jupyter Notebooks)
└── .streamlit/         # Theme configurations (Custom CSS, Layout)
```

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for new features or analytics modules, feel free to:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

