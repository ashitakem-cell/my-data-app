import streamlit as st
import pandas as pd
import requests
from google import genai
from google.genai import types

st.set_page_config(page_title="Expert AI Data Analyst", layout="wide")
st.title("📊 Public AI Data Analyst Hub")
st.markdown("Upload any Excel or CSV file to immediately get key metric summaries, performance charts, and expert AI analysis.")

# --- SECURE BACKGROUND API KEY CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
elif "google_api_key" in st.secrets: 
    API_KEY = st.secrets["google_api_key"]
else:
    st.error("🔒 API Configuration Needed: Please set up 'GEMINI_API_KEY' in your Streamlit Cloud Secrets dashboard.")
    st.stop()

webhook_url = st.sidebar.text_input("Automation Webhook URL (Optional)", type="password")

file = st.file_uploader("Upload Data Sheet", type=["csv", "xlsx"])

if file:
    try:
        client = genai.Client(api_key=API_KEY)
        
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
            
        df.columns = df.columns.str.strip()

        # ---- 1. CORE DATASET METRICS ----
        st.subheader("📋 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        
        sales_col = next((c for c in df.columns if 'sales' in c.lower() or 'amount' in c.lower() or 'price' in c.lower()), None)
        if sales_col:
            col3.metric("Total Volume Gross", f"₹{df[sales_col].sum():,}")
        else:
            col3.metric("Numeric Features", len(df.select_dtypes(include=['int64', 'float64']).columns))
            
        # Updated to fix the warning notice in logs
        st.dataframe(df.head(10), width='stretch')

        # ---- 2. DYNAMIC AUTOMATIC CHARTS ----
        st.markdown("---")
        st.subheader("📊 Interactive Performance Visualizations")
        
        cat_col = next((c for c in df.columns if 'name' in c.lower() or 'category' in c.lower() or 'product' in c.lower() or 'item' in c.lower()), None)
        num_col = sales_col if sales_col else next((c for c in df.columns if df[c].dtype in ['int64', 'float64']), None)
        date_col = next((c for c in df.columns if 'date' in c.lower() or 'time' in c.lower() or 'year' in c.lower()), None)

        chart_c1, chart_c2 = st.columns(2)

        with chart_c1:
            st.markdown("### 📈 Distribution / Category Breakdown")
            if cat_col and num_col:
                breakdown_data = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False).head(10)
                st.bar_chart(breakdown_data)
            else:
                st.info("Provide categorical label columns to render item breakdowns.")

        with chart_c2:
            st.markdown("### ⏱️ Sequential Timeline View")
            if date_col and num_col:
                try:
                    df_time = df.copy()
                    df_time[date_col] = pd.to_datetime(df_time[date_col])
                    timeline_data = df_time.groupby(date_col)[num_col].sum()
                    st.line_chart(timeline_data)
                except:
                    st.line_chart(df[num_col].head(100))
            elif num_col:
                st.line_chart(df[num_col].head(100))
            else:
                st.info("Provide numerical values to map distribution paths.")

        # ---- 3. SENIOR EXECUTIVE AI ANALYST ----
        st.markdown("---")
        if st.button("🚀 Run Expert AI Analysis", type="primary"):
            with st.spinner("Calculating matrices, assessing anomalies, and preparing final report..."):
                
                data_snapshot = df.to_string(index=False)
                
                system_instruction = """
                You are an Elite Senior Data Analyst and Business Strategy Consultant. 
                Your task is to draft a comprehensive executive business report.
                Structure the output beautifully with markdown formatting, bold points, and lists:
                1. Executive Summary
                2. Derived Key Performance Indicators
                3. Identified Trends & Outliers
                4. Actionable Strategy & Next-Step Recommendations
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Perform a complete strategic audit on this dataset table:\n\n{data_snapshot}",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2
                    )
                )
                
                st.session_state['saved_public_report'] = response.text
                st.success("Executive Analysis Generated!")
                st.markdown(response.text)

    except Exception as e:
        st.error(f"Application Execution Error: {e}")
