import streamlit as st
import numpy as np
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Monte Carlo | Wealth Pro", page_icon="🔮", layout="wide")

def load_css():
    if os.path.exists('style.css'):
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css()

st.title("🔮 Probability Analysis (Monte Carlo)")
st.markdown("Markets are volatile. Simulates 100 different market futures to show the range of possible outcomes.")

mc_col1, mc_col2 = st.columns([1, 2.5])

with mc_col1:
    st.markdown("### ⚙️ Parameters")
    mc_years = st.number_input("Years", 5, 40, 15)
    mc_inv = st.number_input("Monthly Investment (₹)", 5000, 200000, 25000)
    mc_avg_return = st.number_input("Average Return (%)", 8.0, 15.0, 12.0)
    mc_volatility = st.slider("Market Volatility (%)", 5.0, 30.0, 15.0, help="Standard Deviation. Higher % means wilder market swings.")

with mc_col2:
    # Monte Carlo Logic
    simulations = 100
    months = mc_years * 12
    
    fig_mc = go.Figure()
    final_values = []
    all_paths = []
    
    # Set a fixed seed so the 100 random paths remain consistent across reruns 
    # (prevents chart from changing wildly when interacting with unrelated widgets)
    np.random.seed(42)
    
    for i in range(simulations):
        monthly_mean = mc_avg_return / 100 / 12
        monthly_std = mc_volatility / 100 / (12**0.5)
        
        monthly_returns = np.random.normal(monthly_mean, monthly_std, months)
        
        portfolio_path = [0]
        curr = 0
        for ret in monthly_returns:
            curr = (curr + mc_inv) * (1 + ret)
            portfolio_path.append(curr)
        
        final_values.append(curr)
        all_paths.append(portfolio_path)
        
        # Add trace (faint lines)
        fig_mc.add_trace(go.Scatter(y=portfolio_path, mode='lines', line=dict(width=1, color='rgba(59, 130, 246, 0.05)'), showlegend=False, hoverinfo='skip'))

    # Calculate Percentiles
    all_paths_arr = np.array(all_paths)
    p10_path = np.percentile(all_paths_arr, 10, axis=0) # Bottom 10%
    p50_path = np.percentile(all_paths_arr, 50, axis=0) # Median
    p90_path = np.percentile(all_paths_arr, 90, axis=0) # Top 10%
    
    x_axis = list(range(months+1))
    fig_mc.add_trace(go.Scatter(x=x_axis, y=p90_path, mode='lines', line=dict(width=2, color='#10b981', dash='dash'), name='Top 10% (P90)'))
    fig_mc.add_trace(go.Scatter(x=x_axis, y=p50_path, mode='lines', line=dict(width=3, color='#3b82f6'), name='Median (P50)'))
    fig_mc.add_trace(go.Scatter(x=x_axis, y=p10_path, mode='lines', line=dict(width=2, color='#ef4444', dash='dash'), name='Bottom 10% (P10)'))
    
    fig_mc.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#f8fafc", family="Outfit"),
        hovermode="x unified",
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Months"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Portfolio Value (₹)"),
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_mc, use_container_width=True)
    
    # Summary Stats
    st.markdown("### 📊 End of Period Outcomes")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Bottom 10% (Poor Luck)", f"₹{np.percentile(final_values, 10)/100000:.2f} L")
    col_b.metric("Median (Expected)", f"₹{np.percentile(final_values, 50)/100000:.2f} L")
    col_c.metric("Top 10% (Great Luck)", f"₹{np.percentile(final_values, 90)/100000:.2f} L")
