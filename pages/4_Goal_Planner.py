import streamlit as st
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Goal Planner | Wealth Pro", page_icon="🚗", layout="wide")

def load_css():
    if os.path.exists('style.css'):
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css()

st.title("🚗 Dream Purchase Planner")
st.markdown("Reverse-engineer the exact monthly savings required to hit major life goals.")

gcol1, gcol2 = st.columns([1, 2.5])

with gcol1:
    st.markdown("### 🎯 Goal Details")
    item_name = st.text_input("Name of Goal", "Tesla Model 3")
    current_cost = st.number_input("Current Cost (₹)", value=4000000, step=100000)
    years_to_buy = st.slider("Time horizon (Years)", 1, 15, 5)
    item_inflation = st.slider("Specific Item Inflation (%)", 0, 15, 5)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("### 💰 Funding")
    monthly_savings_goal = st.number_input("Currently Allocated (₹/mo)", value=50000, step=1000)
    goal_return = st.slider("Exp. Return on Savings (%)", 5.0, 15.0, 10.0)

# Calculations
future_cost = current_cost * ((1 + (item_inflation/100)) ** years_to_buy)
months = years_to_buy * 12
monthly_rate = goal_return / 100 / 12
future_savings = monthly_savings_goal * ((((1 + monthly_rate)**months) - 1) / monthly_rate) * (1 + monthly_rate)
gap = future_savings - future_cost

with gcol2:
    m1, m2 = st.columns(2)
    m1.metric("Inflated Target Cost", f"₹{future_cost/100000:.2f} L", f"{item_inflation}% YoY Inflation", delta_color="inverse")
    m2.metric("Projected Savings", f"₹{future_savings/100000:.2f} L", delta=f"{gap/100000:.2f} L Surplus" if gap >=0 else f"{gap/100000:.2f} L Shortfall", delta_color="normal")
    
    if gap >= 0:
        st.success(f"✅ **On Track!** You will easily be able to afford the **{item_name}** in {years_to_buy} years.")
    else:
        st.error(f"❌ **Shortfall Detected:** You will be short by **₹{abs(gap)/100000:.2f} L**")
        
        # Action Suggestion
        req_monthly = future_cost / (((((1 + monthly_rate)**months) - 1) / monthly_rate) * (1 + monthly_rate))
        diff_monthly = req_monthly - monthly_savings_goal
        
        st.warning(f"💡 **Action Required:** To reach your target on time, increase your monthly savings by **₹{diff_monthly:,.0f}** (New Total: ₹{req_monthly:,.0f}/mo).")
        
    fig_goal = go.Figure(data=[
        go.Bar(name='Projected Savings', x=['Amount'], y=[future_savings], marker_color='#3b82f6'),
        go.Bar(name='Required (Cost)', x=['Amount'], y=[future_cost], marker_color='#ef4444' if gap < 0 else '#10b981')
    ])
    fig_goal.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#f8fafc", family="Outfit"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_goal, use_container_width=True)
