# 📈 Wealth Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

A comprehensive financial planning engine built with **Python** and **Streamlit**. 

Unlike standard SIP calculators, this dashboard integrates **Statistical Probability (Monte Carlo Simulations)**, **Taxation Logic (Indian LTCG)**, and **Inflationary Economics** to provide realistic, data-driven financial projections.

**[🚀 View Live Demo](https://durgesh-wealth-analytics-dashboard.streamlit.app/)**

---

## 📊 Key Features

### 1. Advanced SIP & Tax Analytics
* **Real-World Returns:** Calculates returns adjusted for **Inflation (6%)** to show true purchasing power.
* **Tax Compliance:** Integrated logic for India's **Long Term Capital Gains (LTCG)** tax (12.5% on gains > ₹1.25L), providing a realistic "Net-In-Hand" corpus.

### 2. 🔮 Monte Carlo Simulation (Stochastic Modeling)
* **Risk Analysis:** Moves beyond fixed-return assumptions.
* **The Math:** Runs **50 synchronized market simulations** using Gaussian distributions (`numpy.random.normal`) to model market volatility.
* **Outcome:** Provides a probabilistic range of outcomes (Worst Case vs. Best Case scenarios) rather than a single static number.

### 3. 📉 Cost of Delay Visualizer
* **Opportunity Cost:** Quantifies the financial loss incurred by delaying investments.
* **Visualization:** Comparative bar charts demonstrating the power of compounding over different time horizons.

### 4. 🚗 Goal-Based Reverse Engineering
* **Dynamic Pricing:** Calculates the future cost of aspirations (e.g., a car or house) by applying specific asset inflation rates.
* **Gap Analysis:** Automatically calculates the shortfall/surplus between projected savings and future costs.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Web Framework)
* **Data Manipulation:** Pandas (Time-series data generation)
* **Statistical Computing:** NumPy (Monte Carlo/Randomized simulations)
* **Visualization:** Plotly (Interactive financial charts)

---

## ⚙️ How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YourUsername/wealth-analytics-dashboard.git](https://github.com/YourUsername/wealth-analytics-dashboard.git)
    cd wealth-analytics-dashboard
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app**
    ```bash
    streamlit run app.py
    ```

---

## 🧠 The "Data Science" Behind the App

### The Monte Carlo Logic
Markets are non-deterministic. To model this, the app uses the following approach:
1.  **Volatility Parameter ($\sigma$):** User-defined standard deviation (e.g., 15%).
2.  **Drift ($\mu$):** Expected annual return converted to a monthly mean.
3.  **Simulation:** We generate random monthly returns for $N$ months:
    $$R_t \sim \mathcal{N}(\mu, \sigma^2)$$
4.  **Iteration:** This process is repeated 50 times to generate a confidence interval for the portfolio's future value.

---

## 🚀 Future Scope
* **Portfolio Optimization:** Implementing "Efficient Frontier" logic to suggest the best split between Equity and Debt.
* **Live Market Data:** Fetching real-time NIFTY 50 P/E ratios to suggest "Buy/Sell" zones.

---

## 👨‍💻 Author

**Durgesh Kanzariya** *Aspiring Data Scientist | B.Tech IT Student*

* [LinkedIn Profile](https://linkedin.com/in/durgesh-kanzariya)
* [GitHub Profile](https://github.com/durgesh-kanzariya)

Built with ❤️ using Python.
