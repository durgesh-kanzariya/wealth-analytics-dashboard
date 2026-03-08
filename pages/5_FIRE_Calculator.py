import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.set_page_config(page_title="FIRE Calculator | Wealth Pro", page_icon="🔥", layout="wide")

def load_css():
    if os.path.exists('style.css'):
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css()

st.title("🔥 Financial Independence (FIRE)")
st.markdown("Calculate your exact 'FIRE Number' using the 4% Rule and see when you can retire early.")

col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### 🎯 Your Lifestyle")
    annual_expenses = st.number_input("Est. Annual Expenses in Retirement (₹)", 500000, 10000000, 1200000, 100000, help="What do you plan to spend per year when you retire?")
    withdrawal_rate = st.slider("Safe Withdrawal Rate (%)", 2.5, 6.0, 4.0, 0.1, help="The 4% rule assumes you can safely withdraw 4% of your portfolio every year.")
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("### 💼 Current Progress")
    current_portfolio = st.number_input("Current Nest Egg / Savings (₹)", 0, 100000000, 500000, 100000)
    monthly_investment = st.number_input("Monthly Investments (₹)", 1000, 500000, 30000, 1000)
    expected_return = st.slider("Expected Annual Return (%)", 5.0, 20.0, 12.0, 0.5)

# Calculate FIRE Number
fire_number = annual_expenses / (withdrawal_rate / 100)

# Calculate Time to FIRE
def calculate_months_to_target(current, monthly_add, annual_return, target):
    if current >= target: return 0
    
    monthly_rate = annual_return / 100 / 12
    months = 0
    balance = current
    
    # Cap at 600 months (50 years) to prevent infinite loops if math fails
    while balance < target and months < 600:
        balance = balance * (1 + monthly_rate) + monthly_add
        months += 1
        
    return months

months_to_fire = calculate_months_to_target(current_portfolio, monthly_investment, expected_return, fire_number)
years_to_fire = months_to_fire / 12

with col2:
    m1, m2, m3 = st.columns(3)
    
    # Check if already reached
    if current_portfolio >= fire_number:
        m1.metric("Your FIRE Number", f"₹{fire_number/10000000:.2f} Cr", "Target Reached! 🎉")
        m2.metric("Time to Independence", "0 Years", "You can retire today.")
        m3.metric("Current Run Rate", f"{(current_portfolio * (withdrawal_rate/100)):,.0f} ₹/yr", "Safe Withdrawal Limit")
        st.success("Congratulations! Your current portfolio can sustain your lifestyle infinitely according to the Safe Withdrawal Rate rule.")
    else:
        progress_pct = (current_portfolio / fire_number) * 100
        m1.metric("Your FIRE Number", f"₹{fire_number/10000000:.2f} Cr", f"Needed for {annual_expenses/100000:.1f}L/yr lifestyle")
        m2.metric("Time to Independence", f"{years_to_fire:.1f} Years", f"Working {months_to_fire} more months", delta_color="inverse")
        m3.metric("Progress to FIRE", f"{progress_pct:.1f}%", f"Current Portfolio: ₹{current_portfolio/100000:.2f}L")

    # Generate Projection Data for Chart
    if months_to_fire > 0 and months_to_fire < 600:
        display_months = int(months_to_fire * 1.1) # Show slightly past the goal
        
        path_data = []
        bal = current_portfolio
        monthly_rate = expected_return / 100 / 12
        
        for m in range(display_months + 1):
            path_data.append({"Month": m, "Year": m/12, "Balance": bal})
            bal = bal * (1 + monthly_rate) + monthly_investment
            
        df_fire = pd.DataFrame(path_data)
        
        # Plotly Chart
        fig = go.Figure()
        
        # Target Line
        fig.add_hline(y=fire_number, line_dash="dash", line_color="#ef4444", annotation_text=" FIRE Target 🎯", annotation_position="top left", annotation_font_color="#ef4444")
        
        # Portfolio Growth
        fig.add_trace(go.Scatter(x=df_fire['Year'], y=df_fire['Balance'], fill='tozeroy', name='Projected Net Worth', line=dict(color='#10b981', width=3)))
        
        fig.update_layout(
            title="Road to Financial Independence",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#f8fafc", family="Outfit"),
            hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Years from Today"),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Portfolio Value (₹)"),
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Actionable Insight
        st.info(f"💡 **Pro Tip:** Increasing your monthly investments by just **₹10,000** would shave **{years_to_fire - (calculate_months_to_target(current_portfolio, monthly_investment + 10000, expected_return, fire_number) / 12):.1f} years** off your mandatory working timeline!")

