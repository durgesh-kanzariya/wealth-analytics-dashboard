import streamlit as st
import os

st.set_page_config(
    page_title="Wealth Analytics Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS securely
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
load_css('style.css')

# Landing Page Content
st.markdown("<h1 style='text-align: center; color: #f8fafc; font-size: 3.5rem; margin-bottom: 0;'>Wealth Analytics <span style='color: #3b82f6;'>Pro</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem; margin-bottom: 3rem;'>Professional financial modeling and projection tools.</p>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div data-testid="stMetric" style="min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
        <h3 style="color: #60a5fa; margin-top: 0;">🚀 SIP & Tax Analytics</h3>
        <p style="color: #cbd5e1;">Project your mutual fund growth with advanced options like automated Step-Up SIPs, Inflation adjustment, and Long Term Capital Gains (LTCG) tax calculations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div data-testid="stMetric" style="min-height: 200px; display: flex; flex-direction: column; justify-content: center; margin-top: 20px;">
        <h3 style="color: #34d399; margin-top: 0;">🔮 Monte Carlo Simulation</h3>
        <p style="color: #cbd5e1;">Stop relying on flat returns. Run 100 simulated market scenarios to calculate your 10th, 50th, and 90th percentile wealth probabilities.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div data-testid="stMetric" style="min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
        <h3 style="color: #f87171; margin-top: 0;">📉 Cost of Delay</h3>
        <p style="color: #cbd5e1;">Visualize exactly how much money you lose per day by waiting to start your investment journey. The math will shock you.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div data-testid="stMetric" style="min-height: 200px; display: flex; flex-direction: column; justify-content: center; margin-top: 20px;">
        <h3 style="color: #fbbf24; margin-top: 0;">🚗 Goal Planner</h3>
        <p style="color: #cbd5e1;">Plan for massive purchases (Cars, Homes, Weddings). The engine automatically calculates shortfalls and suggests exact monthly savings increases to hit targets.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin-top: 4rem;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>👈 Please select a tool from the sidebar to begin.</p>", unsafe_allow_html=True)