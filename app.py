import streamlit as st
import pandas as pd
import json
import re
from google import genai
from google.genai import types

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Elite AI Data Analyst Pro", layout="wide", initial_sidebar_state="expanded")

# Executive Theming Custom CSS
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
    .section-banner {
        background: linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%);
        padding: 12px;
        border-radius: 6px;
        margin-top: 20px;
        margin-bottom: 15px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Elite Conversational AI Data Analyst Pro")
st.markdown("Upload your dataset to instantly auto-generate executive visual charts and analysis report, then interact seamlessly via chat to resolve any confusion.")

# --- 2. BACKEND SECURE API ACCESS ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
elif "google_api_key" in st.secrets: 
    API_KEY = st.secrets["google_api_key"]
else:
    st.error("🔒 Configuration Error: Please append 'GEMINI_API_KEY' inside your Streamlit Cloud Secrets console.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Sidebar UI Controls
st.sidebar.header("⚙️ System Control Panel")
webhook_url = st.sidebar.text_input("Automation Webhook URL (Optional)", type="password")
st.sidebar.markdown("---")
st.sidebar.success("App Status: Operational & Ready")

# --- 3. DATA FILE UPLOADER ---
file = st.file_uploader("📂 Drop your corporate data matrix here (CSV or Excel)", type=["csv", "xlsx"])

if file:
    try:
        # Load dataset matrix safely
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
            
        df.columns = df.columns.str.strip()
        
        # --- 4. EXECUTIVE METRICS DASHBOARD (AUTO-GENERATED) ---
        st.markdown('<div class="section-banner"><h3>📋 Core KPI Performance Cards</h3></div>', unsafe_allow_html=True)
        
        sales_col = next((c for c in df.columns if 'sales' in c.lower() or 'amount' in c.lower() or 'price' in c.lower()), None)
        profit_col = next((c for c in df.columns if 'profit' in c.lower() or 'gain' in c.lower()), None)
        product_col = next((c for c in df.columns if 'product' in c.lower() or 'item' in c.lower() or 'category' in c.lower()), None)

        kp1, kp2, kp3, kp4 = st.columns(4)
        with kp1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">TOTAL RECORDS</div><div class="metric-value">{df.shape[0]:,}</div></div>', unsafe_allow_html=True)
        with kp2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">TOTAL DATA VECTOR COLS</div><div class="metric-value">{df.shape[1]}</div></div>', unsafe_allow_html=True)
        with kp3:
            if sales_col:
                total_sales = df[sales_col].sum()
                st.markdown(f'<div class="metric-card"><div class="metric-title">GROSS SALES VOLUME</div><div class="metric-value">₹{total_sales:,.2f}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><div class="metric-title">GROSS SALES VOLUME</div><div class="metric-value">N/A</div></div>', unsafe_allow_html=True)
        with kp4:
            if profit_col:
                total_profit = df[profit_col].sum()
                st.markdown(f'<div class="metric-card"><div class="metric-title">NET MARGINAL PROFIT</div><div class="metric-value">₹{total_profit:,.2f}</div></div>', unsafe_allow_html=True)
            elif product_col and not df[product_col].empty:
                st.markdown(f'<div class="metric-card"><div class="metric-title">TOP DOMINANT CATEGORY</div><div class="metric-value" style="font-size:18px;">{df[product_col].mode()[0]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><div class="metric-title">NET PROFIT CONFIG</div><div class="metric-value">N/A</div></div>', unsafe_allow_html=True)

        st.markdown("#### Preview Grid Snapshot")
        st.dataframe(df.head(5), use_container_width=True)

        # --- 5. AUTOMATED INITIAL VISUALIZATIONS & DEEP DIAGRAMMATIC ANALYSIS ---
        st.markdown('<div class="section-banner"><h3>📊 Executive Data Analysis & Automated Visual Charts</h3></div>', unsafe_allow_html=True)
        
        chart_c1, chart_c2 = st.columns(2)
        cat_label = next((c for c in df.columns if 'name' in c.lower() or 'category' in c.lower() or 'product' in c.lower()), df.columns[1] if len(df.columns) > 1 else df.columns[0])
        num_label = sales_col if sales_col else next((c for c in df.select_dtypes(include=['number']).columns), None)

        with chart_c1:
            if num_label:
                st.markdown(f"**📈 Volumetric Distribution Breakdown by {cat_label} (Bar Visualization)**")
                chart_data = df.groupby(cat_label)[num_label].sum().sort_values(ascending=False).head(10)
                st.bar_chart(chart_data)
            else:
                st.info("No quantitative vectors detected for automated graphing.")

        with chart_c2:
            date_col = next((c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()), None)
            if date_col and num_label:
                st.markdown("**📉 Chronological Trend Vector Performance (Line Chart)**")
                try:
                    df_time = df.copy()
                    df_time[date_col] = pd.to_datetime(df_time[date_col])
                    st.line_chart(df_time.groupby(date_col)[num_label].sum())
                except:
                    st.line_chart(df[num_label].head(40))
            elif num_label:
                st.markdown("**📉 Sequential Distribution Flow Profile**")
                st.line_chart(df[num_label].head(40))

        # Automated Deep Report Summary Box
        if "auto_summary" not in st.session_state:
            with st.spinner("AI Engine generating automated structural analysis report..."):
                try:
                    summary_prompt = (
                        f"You are an expert Chief Data Scientist. Automatically analyze this data context and provide a crisp executive summary. "
                        f"Identify any obvious trends, highlight the top category, evaluate total volumes, and present distinct insights "
                        f"briefly in bullet points. Data Context:\n{df.head(20).to_string(index=False)}"
                    )
                    summary_res = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=summary_prompt,
                        config=types.GenerateContentConfig(temperature=0.2)
                    )
                    st.session_state.auto_summary = summary_res.text
                except Exception as ex_sum:
                    st.session_state.auto_summary = f"Automated summary parsing pipeline encountered context limits: {ex_sum}"
        
        st.markdown("#### 🧠 Automated Insights Report")
        st.info(st.session_state.auto_summary)

        # --- 6. INTERACTIVE CHAT ENGINE (FOR CONFUSION RESOLUTION & DISTINCT CUSTOM CHARTS) ---
        st.markdown('<div class="section-banner"><h3>💬 Interactive Context Chat Room (Clear Your Confusions)</h3></div>', unsafe_allow_html=True)
        st.markdown("*Use this chat interface to ask granular analytics questions, request distinct visual charts, or clarify details from the report above.*")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Re-render chat history securely with correct corresponding chart types
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["text_content"])
                if "chart_data" in msg and msg["chart_data"]:
                    c_df = pd.DataFrame(msg["chart_data"])
                    if not c_df.empty:
                        x_col, y_col = c_df.columns[0], c_df.columns[1]
                        render_data = c_df.set_index(x_col)
                        
                        # Strict Conditional Mapping for Graph Types
                        if msg["chart_type"] == "pie":
                            st.markdown("🎯 *Pie/Distribution Distribution Chart Visualization:*")
                            st.scatter_chart(c_df, x=x_col, y=y_col, size=y_col)
                        elif msg["chart_type"] == "line":
                            st.line_chart(render_data)
                        else:
                            st.bar_chart(render_data)

        # Chat Input Interface
        user_query = st.chat_input("Ask a follow-up query to clear your confusion, or prompt a specific chart style...")
        
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)

            data_context = df.head(40).to_string(index=False)
            available_columns = list(df.columns)
            
            system_instruction = (
                f"You are a Senior Strategic Data Intelligence Agent. Your job is to answer user analytics queries, "
                f"clear up any confusion they have about the automated report, and render customized visuals when explicitly asked. "
                f"Available columns: {available_columns}\n\n"
                f"CRITICAL CHART ASSIGNMENT:\n"
                f"If the user explicitly asks to generate/plot a graph, chart, pie chart, or bar graph, calculate the specific aggregation "
                f"and append a raw JSON block at the very end of your response text. Ensure that the 'chart_type' key accurately reflects "
                f"what the user wanted (e.g., set 'chart_type': 'pie' for pie chart requests, 'chart_type': 'bar' for bar graphs, 'chart_type': 'line' for timelines).\n"
                f"JSON Structure Contract:\n"
                f"```json\n"
                f"{{\n"
                f"  \"render_chart\": true,\n"
                f"  \"chart_type\": \"pie\", // dynamic value based strictly on user prompt\n"
                f"  \"data\": [{{\"LabelColumn\": \"ItemA\", \"NumericValueColumn\": 100}}, {{\"LabelColumn\": \"ItemB\", \"NumericValueColumn\": 250}}]\n"
                f"}}\n"
                f"```\n"
                f"If no chart is requested, omit the JSON structural payload completely."
            )

            with st.chat_message("assistant"):
                with st.spinner("Analyzing corporate vector metrics..."):
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=f"Dataset Structure Overview:\n{data_context}\n\nUser Question/Confusion: {user_query}",
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.1
                            )
                        )
                        
                        raw_text = response.text
                        json_match = re.search(r'```json\s*(.*?)\s*```', raw_text, re.DOTALL)
                        
                        chart_data_extracted = None
                        chart_type_extracted = "bar"
                        clean_display_text = raw_text
                        
                        if json_match:
                            try:
                                json_payload = json.loads(json_match.group(1))
                                if json_payload.get("render_chart"):
                                    chart_data_extracted = json_payload.get("data")
                                    chart_type_extracted = json_payload.get("chart_type", "bar").lower().strip()
                                    clean_display_text = re.sub(r'```json\s*.*?\s*```', '', raw_text, flags=re.DOTALL).strip()
                            except:
                                pass

                        # Output clean textual explanation resolving the confusion
                        st.markdown(clean_display_text)
                        
                        # Live Adaptive Chart Execution 
                        if chart_data_extracted:
                            chart_df = pd.DataFrame(chart_data_extracted)
                            if not chart_df.empty:
                                x_axis, y_axis = chart_df.columns[0], chart_df.columns[1]
                                render_df = chart_df.set_index(x_axis)
                                
                                # Strict Visual Separation
                                if chart_type_extracted == "pie":
                                    st.markdown("🎯 *Pie/Distribution Share Distribution:*")
                                    st.scatter_chart(chart_df, x=x_axis, y=y_axis, size=y_axis)
                                elif chart_type_extracted == "line":
                                    st.line_chart(render_df)
                                else:
                                    st.bar_chart(render_df)

                        # Maintain session history log
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
                        st.error(f"Chat Execution Subsystem Interruption: {chat_err}")

    except Exception as e:
        st.error(f"Core Data Processing Interruption: {e}")
