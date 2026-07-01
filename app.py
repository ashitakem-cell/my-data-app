import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Elite AI Data Analyst", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Executive Look
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 14px;
        color: #94a3b8;
        font-weight: bold;
    }
    .metric-value {
        font-size: 24px;
        color: #f8fafc;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Elite Conversational AI Data Analyst")
st.markdown("Upload any enterprise CSV or Excel sheet to unlock an interactive executive dashboard and chat directly with your data.")

# --- 2. SECURE BACKGROUND API KEY CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
elif "google_api_key" in st.secrets: 
    API_KEY = st.secrets["google_api_key"]
else:
    st.error("🔒 API Configuration Needed: Please set up 'GEMINI_API_KEY' in your Streamlit Cloud Secrets dashboard.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

# Sidebar Configuration
st.sidebar.header("⚙️ Automation Settings")
webhook_url = st.sidebar.text_input("Automation Webhook URL (Optional)", type="password")
st.sidebar.markdown("---")
st.sidebar.info("Tip: Post this on LinkedIn and tag #Streamlit and #GeminiAI for maximum reach!")

# --- 3. FILE UPLOADER & PROCESSING ---
file = st.file_uploader("📂 Drop your data matrix here", type=["csv", "xlsx"])

if file:
    try:
        # Load dataset smoothly
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
            
        df.columns = df.columns.str.strip()
        
        # --- 4. EXECUTIVE KPI DASHBOARD SECTION ---
        st.subheader("📋 Executive KPI Metrics Dashboard")
        
        # Smart column discovery
        sales_col = next((c for c in df.columns if 'sales' in c.lower() or 'amount' in c.lower() or 'price' in c.lower()), None)
        profit_col = next((c for c in df.columns if 'profit' in c.lower() or 'gain' in c.lower()), None)
        product_col = next((c for c in df.columns if 'product' in c.lower() or 'item' in c.lower() or 'category' in c.lower()), None)

        kp1, kp2, kp3, kp4 = st.columns(4)
        
        with kp1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">TOTAL RECORDS</div><div class="metric-value">{df.shape[0]:,}</div></div>', unsafe_allow_html=True)
        with kp2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">TOTAL COLUMNS</div><div class="metric-value">{df.shape[1]}</div></div>', unsafe_allow_html=True)
        with kp3:
            if sales_col:
                total_sales = df[sales_col].sum()
                st.markdown(f'<div class="metric-card"><div class="metric-title">GROSS REVENUE</div><div class="metric-value">₹{total_sales:,.2f}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><div class="metric-title">GROSS REVENUE</div><div class="metric-value">N/A</div></div>', unsafe_allow_html=True)
        with kp4:
            if profit_col:
                total_profit = df[profit_col].sum()
                st.markdown(f'<div class="metric-card"><div class="metric-title">NET PROFIT</div><div class="metric-value">₹{total_profit:,.2f}</div></div>', unsafe_allow_html=True)
            elif product_col:
                top_item = df[product_col].mode()[0] if not df[product_col].empty else "N/A"
                st.markdown(f'<div class="metric-card"><div class="metric-title">TOP CATEGORY</div><div class="metric-value" style="font-size:18px;">{top_item}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><div class="metric-title">NET PROFIT</div><div class="metric-value">N/A</div></div>', unsafe_allow_html=True)

        # Data preview snippet using modern responsive sizing
        st.markdown("### Data Preview Snapshot")
        st.dataframe(df.head(5), width='stretch')

        # --- 5. DYNAMIC GRAPHICAL VISUALIZATIONS ---
        st.markdown("---")
        st.subheader("📊 Visual Analytics Trends")
        chart_c1, chart_c2 = st.columns(2)

        cat_label = next((c for c in df.columns if 'name' in c.lower() or 'category' in c.lower() or 'product' in c.lower()), df.columns[1] if len(df.columns) > 1 else df.columns[0])
        num_label = sales_col if sales_col else next((c for c in df.select_dtypes(include=['number']).columns), None)

        with chart_c1:
            if num_label:
                st.markdown(f"**Top Volumetric Share by {cat_label}**")
                chart_data = df.groupby(cat_label)[num_label].sum().sort_values(ascending=False).head(10)
                st.bar_chart(chart_data)
            else:
                st.info("No categorical columns available for charting.")

        with chart_c2:
            date_col = next((c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()), None)
            if date_col and num_label:
                st.markdown("**Performance Timeline Vector**")
                try:
                    df_time = df.copy()
                    df_time[date_col] = pd.to_datetime(df_time[date_col])
                    st.line_chart(df_time.groupby(date_col)[num_label].sum())
                except:
                    st.line_chart(df[num_label].head(50))
            elif num_label:
                st.markdown("**Data Distribution Flow**")
                st.line_chart(df[num_label].head(50))

        # --- 6. ADVANCED CONVERSATIONAL CHAT (ASK AI) ---
        st.markdown("---")
        st.subheader("💬 Ask AI Anything About This Data")
        st.markdown("Type any conversational query below (e.g., *'Which client brought in the highest margins?'* or *'Summarize our core risk factors'*).")

        # Session state management for Chat History
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display older messages cleanly
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Accept fresh question input
        user_query = st.chat_input("Ask a strategic analytics question...")
        
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.chat_history.append({"role": "user", "content": user_query})

            # Format full context payload for Gemini
            data_context = df.to_string(index=False)
            full_prompt = (
                f"You are a Senior Strategic Data Intelligence Agent. "
                f"Answer the user query precisely based on this active dataset file context:\n\n"
                f"{data_context}\n\nUser Question: {user_query}"
            )

            with st.chat_message("assistant"):
                with st.spinner("AI Agent interpreting data matrices..."):
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=full_prompt,
                            config=types.GenerateContentConfig(temperature=0.2)
                        )
                        st.markdown(response.text)
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    except Exception as chat_err:
                        st.error(f"Chat Engine Error: {chat_err}")

    except Exception as e:
        st.error(f"Core System Interruption: {e}")
