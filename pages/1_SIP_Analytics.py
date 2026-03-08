import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="SIP Analytics | Wealth Pro", page_icon="🚀", layout="wide")

def load_css():
    if os.path.exists('style.css'):
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css()

st.title("🚀 SIP & Tax Analytics")
st.markdown("Project compound growth. Adjust for Inflation & real-world Taxes.")

col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### ⚙️ Configuration")
    monthly_inv = st.slider("Monthly Investment (₹)", 1000, 200000, 25000, 500)
    step_up_rate = st.slider("Annual Step-Up (%)", 0, 20, 5, help="Increase SIP amount by this % every year")
    return_rate = st.slider("Expected Annual Return (%)", 5.0, 20.0, 12.0, 0.5)
    time_period = st.slider("Time Period (Years)", 1, 40, 15)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("### 🛡️ Reality Checks")
    inflation_adj = st.toggle("Adjust for Inflation (6%)", value=False)
    tax_adj = st.toggle("Apply LTCG Tax (12.5%)", value=False, help="Tax on gains > ₹1.25 Lakhs")
    
    inflation_rate = 6.0 if inflation_adj else 0.0

# Calculation Logic
data = []
total_invested = 0
current_value = 0
months = time_period * 12
monthly_rate = return_rate / 100 / 12

current_sip = monthly_inv

for m in range(1, months + 1):
    if m > 1 and (m - 1) % 12 == 0:
        current_sip = current_sip * (1 + (step_up_rate/100))
        
    total_invested += current_sip
    interest = current_value * monthly_rate
    current_value += current_sip + interest
    
    real_value = current_value / ((1 + (inflation_rate/100/12))**m)
    
    data.append({
        "Month": m,
        "Year": m / 12,
        "Monthly SIP": round(current_sip, 2),
        "Invested": round(total_invested, 2),
        "Portfolio Value": round(current_value, 2),
        "Real Value": round(real_value, 2)
    })

df = pd.DataFrame(data)
final_val = df.iloc[-1]["Portfolio Value"]
final_invested = df.iloc[-1]["Invested"]
total_gains = final_val - final_invested

# TAX LOGIC
tax_amount = 0
post_tax_value = final_val

if tax_adj:
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
        m3.metric("Tax Payable", f"₹{tax_amount/100000:.2f} L", "-12.5% LTCG", delta_color="inverse")
    else:
        m3.metric("Wealth Multiplier", f"{final_val/final_invested:.1f}x", "Money Multiplied")

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Invested'], fill='tozeroy', name='Invested', line=dict(color='#64748b', width=2)))
    fig.add_trace(go.Scatter(x=df['Year'], y=df['Portfolio Value'], fill='tonexty', name='Portfolio Value', line=dict(color='#3b82f6', width=3)))
    
    if inflation_adj:
         fig.add_trace(go.Scatter(x=df['Year'], y=df['Real Value'], name='Purchasing Power', line=dict(color='#ef4444', dash='dot', width=2)))
    
    fig.update_layout(
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#f8fafc", family="Outfit"),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Years"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Amount (₹)"),
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Export Data
    with st.expander("📊 View Detailed Data Table & Export"):
        st.dataframe(df.style.format({"Monthly SIP": "₹{:.0f}", "Invested": "₹{:.0f}", "Portfolio Value": "₹{:.0f}", "Real Value": "₹{:.0f}"}), use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Projection as CSV",
            data=csv,
            file_name='sip_tax_projection.csv',
            mime='text/csv',
            use_container_width=True
        )
