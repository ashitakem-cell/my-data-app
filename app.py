import streamlit as st
import pandas as pd
import requests
import os
from google import genai
from google.genai import types

st.set_page_config(page_title="Expert AI Data Analyst", layout="wide")
st.title("📊 Expert AI Data Analyst Hub")

# Sidebar Configuration
st.sidebar.header("🔑 API & Connection Configuration")
api_key = st.sidebar.text_input("Google AI Studio API Key", type="password")
webhook_url = st.sidebar.text_input("Automation Webhook URL (Optional)", type="password")

# File Uploader
file = st.file_uploader("Upload Dataset (Excel/CSV)", type=["csv", "xlsx"])

if file and api_key:
    try:
        # Initialize the modern Google GenAI Client
        client = genai.Client(api_key=api_key)
        
        # 1. Load and Clean Data
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
            
        # Display Data Preview Metrics
        st.subheader("📋 Dataset Preview & Context")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        if 'Sales Amount' in df.columns:
            col3.metric("Total Revenue", f"₹{df['Sales Amount'].sum():,}")
            
        st.dataframe(df.head(10), use_container_width=True)
        
        # 2. Expert Analysis Core
        if st.button("🚀 Run Expert AI Analysis", type="primary"):
            with st.spinner("Analyzing data vectors, calculating KPIs, and generating summary..."):
                
                data_string = df.to_string(index=False)
                
                # System instructions force Gemini to follow a strict analytical layout
                system_instruction = """
                You are a Senior Executive Data Analyst. Your analysis must be structured, 
                professional, and deeply insightful. Avoid generic descriptions. Always include:
                1. Executive Summary (High-level takeaways)
                2. Core Key Performance Indicators (KPIs) derived from the numbers
                3. Distinct Trends & Outliers discovered in categories or timelines
                4. Actionable Data-Driven Recommendations for leadership
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Analyze this sales performance dataset:\n\n{data_string}",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.3 # Lower temperature ensures focused, fact-based financial insights
                    )
                )
                
                # Store report in session state for later steps
                st.session_state['latest_report'] = response.text
                
                st.success("Analysis Complete!")
                st.markdown("---")
                st.subheader("📈 Executive Analysis Report")
                st.markdown(response.text)
                
        # 3. Integration Pipelines (Automations & Database Triggers)
        if 'latest_report' in st.session_state:
            st.markdown("---")
            st.subheader("🔗 Data Pipeline & Report Delivery")
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.info("💡 **Sync to Supabase Database**\nSimulating live database streaming. Ensure your backend handles row-by-row updates.")
                if st.button("Sync Raw Records to Supabase"):
                    # Here you can map your actual Supabase Client ingestion loop
                    st.success(f"Successfully processed and prepared {len(df)} records for table: 'sales_data'")
                    
            with c2:
                st.info("✉️ **Trigger Automation Workflow**\nSends the generated AI insights report directly through your active webhook integration.")
                if st.button("Send Report to Webhook/Email"):
                    if webhook_url:
                        payload = {
                            "status": "success",
                            "record_count": len(df),
                            "report_content": st.session_state['latest_report']
                        }
                        res = requests.post(webhook_url, json=payload)
                        if res.status_code == 200 or res.status_code == 201:
                            st.success("Pipeline executed! Report forwarded to Zapier / Mail workflow.")
                        else:
                            st.error(f"Failed to trigger endpoint. Status code: {res.status_code}")
                    else:
                        st.warning("Please provide a valid Webhook URL in the sidebar first.")
                        
    except Exception as e:
        st.error(f"Execution Error: {e}")
