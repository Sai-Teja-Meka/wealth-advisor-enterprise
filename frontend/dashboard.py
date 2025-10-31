# ============================================================
# STREAMLIT DASHBOARD (Web UI)
# ============================================================

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Configure page
st.set_page_config(
    page_title="Wealth Advisor Enterprise",
    page_icon="💼",
    layout="wide"
)

# API URL
API_URL = "http://localhost:8000/api/v1"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.title("⚙️ Settings")
    
    selected_tickers = st.multiselect(
        "Select Companies to Monitor",
        ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "SHOP", "UPST", "NET", "PLTR", "CRWD"],
        default=["AAPL", "MSFT", "GOOGL"]
    )
    
    update_frequency = st.radio(
        "Update Frequency",
        ["Manual", "Every Hour", "Daily"]
    )
    
    if st.button("🔄 Generate Recommendations"):
        st.session_state.generate = True

# ============================================================
# MAIN CONTENT
# ============================================================

st.title("💰 Wealth Advisor - Enterprise Dashboard")
st.markdown("AI-powered investment advisory system for small companies")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analysis",
    "💼 Recommendations",
    "📈 Portfolio",
    "ℹ️ About"
])

# TAB 1: ANALYSIS
with tab1:
    st.header("Company Analysis")
    
    if selected_tickers:
        # Make API request
        try:
            with st.spinner("Analyzing companies..."):
                response = requests.post(
                    f"{API_URL}/analyze",
                    json=selected_tickers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    analysis = data["analysis"]
                    
                    # Display results
                    for i, company in enumerate(analysis[:5], 1):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                f"{company['ticker']} - {company['name']}",
                                f"${company['price']:.2f}",
                                f"{company['score']:.1f}/100"
                            )
                        
                        with col2:
                            recommendation_color = {
                                "STRONG BUY": "🟢",
                                "BUY": "🟢",
                                "HOLD": "🟡",
                                "WEAK SELL": "🔴",
                                "SELL": "🔴"
                            }
                            st.write(f"**Recommendation:** {recommendation_color.get(company['recommendation'])} {company['recommendation']}")
                            st.write(f"**Risk Level:** {company['risk']}")
                        
                        with col3:
                            metrics_df = pd.DataFrame([company['metrics']])
                            st.dataframe(metrics_df)
                    
                    # DataFrame
                    df = pd.DataFrame(analysis)
                    st.dataframe(df[["ticker", "name", "price", "score", "recommendation", "risk"]], use_container_width=True)
        
        except Exception as e:
            st.error(f"Error: {e}")

# TAB 2: RECOMMENDATIONS
with tab2:
    st.header("Investment Recommendations")
    
    if selected_tickers:
        try:
            with st.spinner("Generating recommendations..."):
                response = requests.post(
                    f"{API_URL}/advise",
                    json=selected_tickers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    advice = data["advice"]
                    
                    st.info(advice)
        
        except Exception as e:
            st.error(f"Error: {e}")

# TAB 3: PORTFOLIO
with tab3:
    st.header("Portfolio Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔴 Aggressive")
        st.write("""
        - 70% High Potential
        - 25% Medium Potential
        - 5% Low Potential
        """)
    
    with col2:
        st.subheader("🟡 Balanced")
        st.write("""
        - 50% High Potential
        - 40% Medium Potential
        - 10% Low Potential
        """)
    
    with col3:
        st.subheader("🟢 Conservative")
        st.write("""
        - 30% High Potential
        - 50% Medium Potential
        - 20% Low Potential
        """)

# TAB 4: ABOUT
with tab4:
    st.header("About This Application")
    
    st.markdown("""
    ### Wealth Advisor Enterprise
    
    **Version:** 1.0.0
    
    **Architecture:**
    - **Frontend:** Streamlit (this dashboard)
    - **Backend:** FastAPI (REST API)
    - **Database:** Supabase PostgreSQL
    - **AI:** Groq (Investment advice)
    
    **Features:**
    - Real-time company analysis
    - AI-powered investment recommendations
    - Multi-user dashboard
    - Automated hourly updates
    - Scalable microservices
    
    **Data Sources:**
    - Finnhub (Stock prices, fundamentals)
    - Financial Modeling Prep (Financial ratios)
    - Groq API (AI recommendations)
    
    **Contact:** admin@wealthadvisor.app
    """)
