import streamlit as st
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Cost of Delay | Wealth Pro", page_icon="📉", layout="wide")

def load_css():
    if os.path.exists('style.css'):
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css()

st.title("📉 The Cost of Waiting")
st.markdown("Discover exactly how much wealth is destroyed by delaying investments.")

cd_col1, cd_col2 = st.columns([1, 2.5])
with cd_col1:
    st.markdown("### ⚙️ Time Machine")
    delay_inv = st.number_input("Monthly Investment (₹)", value=25000, step=1000)
    delay_ret = st.number_input("Return Rate (%)", value=12.0, step=0.5)
    delay_duration = st.slider("Total Investment Window (Years)", 5, 40, 20)
    delay_years = st.slider("Delay Start By (Years)", 1, 15, 5)

with cd_col2:
    # Scenario A: Start Today
    months_a = delay_duration * 12
    rate = delay_ret / 100 / 12
    corpus_a = delay_inv * ((((1 + rate)**months_a) - 1) / rate) * (1 + rate)
    
    # Scenario B: Start Late
    months_b = (delay_duration - delay_years) * 12
    corpus_b = delay_inv * ((((1 + rate)**months_b) - 1) / rate) * (1 + rate)
    
    loss = corpus_a - corpus_b
    if delay_years > 0:
        loss_per_day = loss / (delay_years * 365)
    else:
        loss_per_day = 0
    
    # Metrics display
    st.markdown(f"## 🚨 Total Lost Wealth: <span style='color:#ef4444;'>₹{loss/100000:.2f} Lakhs</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.2rem; color: #cbd5e1;'>By waiting <b>{delay_years} years</b> to start investing, every single day of inaction is costing your future self <b><span style='color:#ef4444;'>₹{loss_per_day:,.0f}</span></b>.</p>", unsafe_allow_html=True)
    
    # Chart
    fig_delay = go.Figure(data=[
        go.Bar(name='Start Today', x=['Final Corpus'], y=[corpus_a], marker_color='#3b82f6', text=f"₹{corpus_a/100000:.1f}L", textposition='auto'),
        go.Bar(name=f'Start {delay_years} Years Late', x=['Final Corpus'], y=[corpus_b], marker_color='#475569', text=f"₹{corpus_b/100000:.1f}L", textposition='auto')
    ])
    fig_delay.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#f8fafc", family="Outfit"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_delay, use_container_width=True)
