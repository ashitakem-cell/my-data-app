import streamlit as st
import pandas as pd
import requests
from google import genai
from google.genai import types

st.set_page_config(page_title="Public AI Data Analyst", layout="wide")
st.title("📊 Smart Data Analyst Hub")
st.markdown("Upload your CSV or Excel file below to instantly generate charts and AI-powered executive insights.")

# Retrieve the API key securely from Streamlit Secrets backend
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please configure 'GEMINI_API_KEY' in your Streamlit Secrets.")
    st.stop()

# Optional automation webhook config can remain in the sidebar for admin use
webhook_url = st.sidebar.text_input("Automation Webhook URL (Optional)", type="password")

# File Uploader - Simple for any regular user
file = st.file_uploader("Choose an Excel or CSV file", type=["csv", "xlsx"])

if file:
    try:
        # Initialize GenAI Client
        client = genai.Client(api_key=API_KEY)
        
        # Load Data
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
            
        # Clean up column names to prevent mapping errors
        df.columns = df.columns.str.strip()

        # ---- SECTION 1: QUICK METRICS ----
        st.subheader("📋 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records Listed", df.shape[0])
        col2.metric("Total Columns Detected", df.shape[1])
        
        # Check if financial columns exist to display a revenue metric
        sales_col = next((c for c in df.columns if 'sales' in c.lower() or 'amount' in c.lower()), None)
        if sales_col:
            col3.metric("Total Volume / Revenue", f"₹{df[sales_col].sum():,}")

        st.dataframe(df.head(5), use_container_width=True)

        # ---- SECTION 2: AUTOMATIC CHARTS ----
        st.markdown("---")
        st.subheader("📊 Visual Performance Charts")
        
        # Identify categorical vs numerical columns dynamically
        date_col = next((c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()), None)
        cat_col = next((c for c in df.columns if 'name' in c.lower() or 'category' in c.lower() or 'product' in c.lower()), None)
        num_col = sales_col if sales_col else next((c for c in df.columns if df[c].dtype in ['int64', 'float64']), None)

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Breakdown Breakdown Chart**")
            if cat_col and num_col:
                # Group data to clean up layout
                chart_data = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False).head(10)
                st.bar_chart(chart_data)
            else:
                st.info("Upload a dataset with clear categories to render bar breakdowns.")

        with chart_col2:
            st.markdown("**Timeline Cumulative View**")
            if date_col and num_col:
                try:
                    df_time = df.copy()
                    df_time[date_col] = pd.to_datetime(df_time[date_col])
                    time_data = df_time.groupby(date_col)[num_col].sum()
                    st.line_chart(time_data)
                except:
                    st.info("Could not convert date column automatically for timeline graph.")
            elif num_col:
                st.line_chart(df[num_col].head(50))
            else:
                st.info("Provide sequential numerical parameters to render distribution lines.")

        # ---- SECTION 3: EXPERT AI ANALYSIS ----
        st.markdown("---")
        if st.button("🚀 Run AI Analysis Report", type="primary"):
            with st.spinner("Analyzing data parameters and generating executive insights..."):
                
                data_snapshot = df.to_string(index=False)
                
                system_instruction = """
                You are an elite Senior Data Analyst. Write a beautifully structured executive report.
                Use bullet points, bold headers, and structured lists. Provide:
                1. Executive Summary
                2. Key Performance Indicators calculated from the data table
                3. Clear trends, peaks, or drops observed
                4. Strategic, actionable advice for improvement
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Analyze this dataset performance tables:\n\n{data_snapshot}",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2
                    )
                )
                
                st.session_state['public_report'] = response.text
                st.success("Report Compiled Successfully!")
                st.markdown(response.text)

        # ---- SECTION 4: DOWNSTREAM PIPELINE ----
        if 'public_report' in st.session_state and webhook_url:
            st.markdown("---")
            if st.button("📨 Dispatch Report to Automation Pipeline"):
                payload = {
                    "status": "completed",
                    "rows": len(df),
                    "summary": st.session_state['public_report']
                }
                res = requests.post(webhook_url, json=payload)
                if res.status_code in [200, 201]:
                    st.success("Sent! Your integrated workflow has picked up the document.")
                else:
                    st.error("Workflow link returned an error code.")

    except Exception as e:
        st.error(f"Analysis Engine Error: {e}")
