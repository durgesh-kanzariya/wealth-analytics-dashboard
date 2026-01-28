import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(
    page_title="Wealth Analytics Pro",
    page_icon="📈",
    layout="wide"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .metric-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Wealth Analytics Dashboard")
st.markdown("Advanced Financial Projections, Risk Analysis (Monte Carlo), and Goal Planning.")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 SIP & Tax Analytics", 
    "🔮 Monte Carlo Simulation", 
    "📉 Cost of Delay", 
    "🚗 Goal Planner"
])

# ================= TAB 1: SIP + TAX ANALYTICS =================
with tab1:
    st.subheader("SIP Calculator with Tax & Inflation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Inputs")
        monthly_inv = st.slider("Monthly Investment (₹)", 1000, 100000, 25000, 500)
        return_rate = st.slider("Annual Return (%)", 5.0, 20.0, 12.0, 0.5)
        time_period = st.slider("Time Period (Years)", 1, 30, 15)
        
        st.divider()
        st.markdown("### Reality Checks")
        inflation_adj = st.toggle("Adjust for Inflation (6%)", value=False)
        tax_adj = st.toggle("Apply LTCG Tax (12.5%)", value=False, help="Tax on gains > ₹1.25 Lakhs")
        
        inflation_rate = 6.0 if inflation_adj else 0.0

    # Calculation Logic
    data = []
    total_invested = 0
    current_value = 0
    months = time_period * 12
    monthly_rate = return_rate / 100 / 12
    
    for m in range(1, months + 1):
        total_invested += monthly_inv
        interest = current_value * monthly_rate
        current_value += monthly_inv + interest
        
        # Inflation Adjustment
        real_value = current_value / ((1 + (inflation_rate/100/12))**m)
        
        data.append({
            "Month": m,
            "Year": m / 12,
            "Invested": total_invested,
            "Portfolio Value": current_value,
            "Real Value": real_value
        })

    df = pd.DataFrame(data)
    final_val = df.iloc[-1]["Portfolio Value"]
    final_invested = df.iloc[-1]["Invested"]
    total_gains = final_val - final_invested
    
    # TAX LOGIC (Indian LTCG Rules 2024-25)
    tax_amount = 0
    post_tax_value = final_val
    
    if tax_adj:
        # 12.5% tax on gains exceeding 1.25 Lakhs
        taxable_gains = max(0, total_gains - 125000)
        tax_amount = taxable_gains * 0.125
        post_tax_value = final_val - tax_amount

    with col2:
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Invested", f"₹{final_invested/100000:.2f} L")
        
        display_val = post_tax_value if tax_adj else final_val
        delta_label = "Post-Tax Gains" if tax_adj else "Total Gains"
        
        m2.metric("Final Corpus", f"₹{display_val/10000000:.2f} Cr", delta=f"{((display_val-final_invested)/final_invested)*100:.0f}% Growth")
        
        if tax_adj:
            m3.metric("Tax Payable", f"₹{tax_amount/100000:.2f} L", "LTCG @ 12.5%")
        else:
            m3.metric("Wealth Multiplier", f"{final_val/final_invested:.1f}x", "Money Multiplied")

        # Plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Year'], y=df['Invested'], fill='tozeroy', name='Invested', line=dict(color='#bdc3c7')))
        fig.add_trace(go.Scatter(x=df['Year'], y=df['Portfolio Value'], fill='tonexty', name='Portfolio Value', line=dict(color='#2ecc71')))
        
        if inflation_adj:
             fig.add_trace(go.Scatter(x=df['Year'], y=df['Real Value'], name='Purchasing Power', line=dict(color='#e74c3c', dash='dot')))
        
        st.plotly_chart(fig, use_container_width=True)


# ================= TAB 2: MONTE CARLO SIMULATION =================
with tab2:
    st.subheader("🔮 Probability Analysis (Monte Carlo)")
    st.info("Markets are volatile. This simulates 50 different market futures to show the range of possible outcomes.")
    
    mc_col1, mc_col2 = st.columns([1, 3])
    
    with mc_col1:
        mc_years = st.number_input("Years", 5, 30, 15)
        mc_inv = st.number_input("Monthly Inv", 5000, 100000, 25000)
        mc_avg_return = st.number_input("Avg Return (%)", 8.0, 15.0, 12.0)
        mc_volatility = st.slider("Market Volatility (%)", 5.0, 25.0, 15.0, help="Higher % means wilder market swings")
        
    with mc_col2:
        # Monte Carlo Logic
        simulations = 50
        months = mc_years * 12
        results = []
        
        fig_mc = go.Figure()
        
        final_values = []
        
        for i in range(simulations):
            # Generate random monthly returns based on normal distribution
            # Mean monthly return and monthly std dev
            monthly_mean = mc_avg_return / 100 / 12
            monthly_std = mc_volatility / 100 / (12**0.5)
            
            # Vectorized calculation for speed
            monthly_returns = np.random.normal(monthly_mean, monthly_std, months)
            
            # Calculate cumulative path
            portfolio_path = [0]
            curr = 0
            for ret in monthly_returns:
                curr = (curr + mc_inv) * (1 + ret)
                portfolio_path.append(curr)
            
            final_values.append(curr)
            
            # Add trace (make lines thin and transparent)
            fig_mc.add_trace(go.Scatter(y=portfolio_path, mode='lines', line=dict(width=1, color='rgba(0,100,255,0.2)'), showlegend=False))

        # Add Average Line
        avg_path = [mc_inv * m * (1 + monthly_mean)**m for m in range(months+1)] # Simplified approx for visual
        
        fig_mc.update_layout(title=f"50 Simulated Market Scenarios", xaxis_title="Months", yaxis_title="Portfolio Value")
        st.plotly_chart(fig_mc, use_container_width=True)
        
        # Summary Stats
        st.write("### Analysis of 50 Simulations")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Worst Case (Luck)", f"₹{min(final_values)/100000:.2f} L")
        col_b.metric("Median Case (Likely)", f"₹{np.median(final_values)/100000:.2f} L")
        col_c.metric("Best Case (Lucky)", f"₹{max(final_values)/100000:.2f} L")


# ================= TAB 3: COST OF DELAY =================
with tab3:
    st.subheader("📉 The Cost of Waiting")
    st.write("See how much money you lose by delaying your investment by just a few years.")
    
    cd_col1, cd_col2 = st.columns([1, 2])
    with cd_col1:
        delay_inv = st.number_input("Monthly Investment", value=25000)
        delay_ret = st.number_input("Return Rate (%)", value=12.0)
        delay_duration = st.slider("Total Investment Duration (Years)", 10, 40, 20)
        delay_years = st.slider("Delay Start By (Years)", 1, 10, 5)

    with cd_col2:
        # Scenario A: Start Today
        months_a = delay_duration * 12
        rate = delay_ret / 100 / 12
        corpus_a = delay_inv * ((((1 + rate)**months_a) - 1) / rate) * (1 + rate)
        
        # Scenario B: Start Late
        # Investment duration decreases by delay_years
        months_b = (delay_duration - delay_years) * 12
        corpus_b = delay_inv * ((((1 + rate)**months_b) - 1) / rate) * (1 + rate)
        
        loss = corpus_a - corpus_b
        
        st.error(f"💸 **Cost of Delay:** You lose **₹{loss/100000:.2f} Lakhs** by waiting {delay_years} years!")
        
        # Chart
        fig_delay = go.Figure(data=[
            go.Bar(name='Start Today', x=['Final Corpus'], y=[corpus_a], marker_color='#2ecc71'),
            go.Bar(name=f'Start {delay_years} Years Late', x=['Final Corpus'], y=[corpus_b], marker_color='#e74c3c')
        ])
        fig_delay.update_layout(title="Wealth Comparison")
        st.plotly_chart(fig_delay, use_container_width=True)


# ================= TAB 4: GOAL PLANNER =================
with tab4:
    st.subheader("🚗 Dream Purchase Planner")
    
    gcol1, gcol2 = st.columns([1, 2])
    
    with gcol1:
        item_name = st.text_input("Item Name", "Tesla Model 3")
        current_cost = st.number_input("Current Cost (₹)", value=4000000, step=100000)
        years_to_buy = st.slider("Years to Purchase", 1, 15, 5)
        item_inflation = st.slider("Item Inflation (%)", 0, 10, 5)
        monthly_savings_goal = st.number_input("Allocated Savings (₹)", value=50000, step=1000)
        goal_return = st.slider("Exp. Return (%)", 5.0, 15.0, 10.0)

    # Goal Calculations
    future_cost = current_cost * ((1 + (item_inflation/100)) ** years_to_buy)
    months = years_to_buy * 12
    monthly_rate = goal_return / 100 / 12
    future_savings = monthly_savings_goal * ((((1 + monthly_rate)**months) - 1) / monthly_rate) * (1 + monthly_rate)
    gap = future_savings - future_cost

    with gcol2:
        m1, m2 = st.columns(2)
        m1.metric("Future Cost", f"₹{future_cost/100000:.2f} L")
        m2.metric("Projected Savings", f"₹{future_savings/100000:.2f} L", delta=f"{gap/100000:.2f} L")
        
        if gap >= 0:
            st.success(f"✅ You can buy the **{item_name}**!")
        else:
            st.error(f"❌ Shortfall of ₹{abs(gap)/100000:.2f} L")
            
        fig_goal = go.Figure(data=[
            go.Bar(name='Savings', x=['Amount'], y=[future_savings], marker_color='#2ecc71'),
            go.Bar(name='Cost', x=['Amount'], y=[future_cost], marker_color='#e74c3c')
        ])
        st.plotly_chart(fig_goal, use_container_width=True)

st.divider()
st.caption("Developed by Durgesh Kanzariya | Financial Analytics Dashboard")