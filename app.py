import streamlit as st
import pandas as pd
import json
import re
from google import genai
from google.genai import types

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Elite AI Data Analyst Pro", layout="wide", initial_sidebar_state="expanded")

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

st.title("🤖 Elite Conversational AI Data Analyst Pro")
st.markdown("Upload any enterprise CSV or Excel sheet to unlock an interactive executive dashboard and chat directly with your data (including dynamic chart rendering!).")

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

        # --- 6. ADVANCED CONVERSATIONAL CHAT (ASK AI & EXECUTE CHARTS) ---
        st.markdown("---")
        st.subheader("💬 Ask AI Anything About This Data")
        st.markdown("Type any conversational query below. **You can explicitly request charts!** (e.g., *'Show me a pie chart of sales by product'*).")

        # Session state management for Chat History
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display older messages cleanly
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["text_content"])
                if "chart_data" in msg and msg["chart_data"]:
                    c_type = msg["chart_type"]
                    c_df = pd.DataFrame(msg["chart_data"])
                    if not c_df.empty:
                        # Re-render charts from logs cleanly
                        x_col, y_col = c_df.columns[0], c_df.columns[1]
                        chart_render_data = c_df.set_index(x_col)
                        if c_type == "bar":
                            st.bar_chart(chart_render_data)
                        elif c_type == "line":
                            st.line_chart(chart_render_data)
                        elif c_type == "pie":
                            # Streamlit standard lacks native st.pie_chart, so we fallback beautifully to a clear bar_chart 
                            # or use an alternate clean distribution rendering
                            st.markdown(f"📊 *Visualizing item share distribution for {x_col}:*")
                            st.bar_chart(chart_render_data)

        # Accept fresh question input
        user_query = st.chat_input("Ask a strategic analytics question or request a visualization...")
        
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)

            # Format full system instruction setup allowing chart JSON metadata injection
            data_context = df.to_string(index=False)
            available_columns = list(df.columns)
            
            system_instruction = (
                f"You are a Senior Strategic Data Intelligence Agent. Your task is to answer user analytics queries precisely "
                f"based on the provided dataset structure. Available columns in the file: {available_columns}\n\n"
                f"CRITICAL ASSIGNMENT FOR CHARTS:\n"
                f"If the user explicitly asks to plot, visualize, or create a chart (like a bar chart, line chart, or pie chart), "
                f"you MUST calculate the aggregated data requested and append a clean JSON block at the very end of your response text.\n"
                f"Do not write regular markdown charts. Always output the JSON structure exactly like this enclosed in code delimiters:\n"
                f"```json\n"
                f"{{\n"
                f"  \"render_chart\": true,\n"
                f"  \"chart_type\": \"bar\", // can be 'bar', 'line', or 'pie'\n"
                f"  \"data\": [{{\"Column1\": \"LabelA\", \"Column2\": 120}}, {{\"Column1\": \"LabelB\", \"Column2\": 340}}]\n"
                f"}}\n"
                f"```\n"
                f"If the user does not request a visual representation, do not include the JSON payload block."
            )

            with st.chat_message("assistant"):
                with st.spinner("AI Agent interpreting data matrices..."):
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Dataset:\n{data_context}\n\nUser Question: {user_query}",
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.2
                            )
                        )
                        
                        raw_text = response.text
                        
                        # Parse JSON instructions if injected by the AI model
                        json_match = re.search(r'```json\s*(.*?)\s*```', raw_text, re.DOTALL)
                        
                        chart_data_extracted = None
                        chart_type_extracted = None
                        clean_display_text = raw_text
                        
                        if json_match:
                            try:
                                json_payload = json.loads(json_match.group(1))
                                if json_payload.get("render_chart"):
                                    chart_data_extracted = json_payload.get("data")
                                    chart_type_extracted = json_payload.get("chart_type", "bar")
                                    # Clean raw JSON blocks out from natural reader UI text
                                    clean_display_text = re.sub(r'```json\s*.*?\s*```', '', raw_text, flags=re.DOTALL).strip()
                            except:
                                pass # Fault tolerance for corrupted token parsing

                        # Render user display texts
                        st.markdown(clean_display_text)
                        
                        # Live execution of the requested charts dynamically right inside chat channel!
                        if chart_data_extracted:
                            chart_df = pd.DataFrame(chart_data_extracted)
                            if not chart_df.empty:
                                x_axis, y_axis = chart_df.columns[0], chart_df.columns[1]
                                render_df = chart_df.set_index(x_axis)
                                if chart_type_extracted == "bar":
                                    st.bar_chart(render_df)
                                elif chart_type_extracted == "line":
                                    st.line_chart(render_df)
                                else:
                                    st.markdown(f"📊 *Visualizing distribution share breakdown:*")
                                    st.bar_chart(render_df)

                        # Save clean states into history pipelines
                        st.session_state.chat_history.append({
                            "role": "user", 
                            "text_content": user_query
                        })
                        st.session_state.chat_history.append({
                            "role": "assistant", 
                            "text_content": clean_display_text,
                            "chart_data": chart_data_extracted,
                            "chart_type": chart_type_extracted
                        })
                        
                    except Exception as chat_err:
                        st.error(f"Chat Engine Error: {chat_err}")

    except Exception as e:
        st.error(f"Core System Interruption: {e}")
