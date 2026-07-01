import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Elite AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (Zero Red Lines, Ultra-Clean Glow Theme)
st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background-color: #0b0f17;
        color: #f1f5f9;
    }
    
    /* Elegant Title Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    /* Premium KPI Glassmorphism Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.8rem;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 10px 30px -5px rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    /* Custom Sections */
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 0.6rem;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
    }
    
    /* Input & Chat styling overrides to keep it clean */
    div[data-testid="stChatInputContainer"] {
        border: 1px solid #334155 !important;
        background-color: #0f172a !important;
        border-radius: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔒 BACKEND API KEY INTEGRATION (No Sidebar Input!)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
elif "google_api_key" in st.secrets: 
    API_KEY = st.secrets["google_api_key"]
else:
    st.error("🔒 Backend Configuration Missing: Please set up 'GEMINI_API_KEY' in your Streamlit Cloud Secrets dashboard.")
    st.stop()

# Configure Gemini globally from backend
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sidebar Configuration (Clean & Informative)
with st.sidebar:
    st.markdown("<h2 style='color:#fff;'>⚙️ Control Center</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🚀 Project Architecture")
    st.info("This production-grade dashboard automatically securely parses uploaded matrices using LLM reasoning models vectors.")
    st.markdown("---")
    st.markdown("💡 **LinkedIn Tip:** Tag #Streamlit and #GeminiAI when uploading your project video!")

# Main App Header Area
st.markdown('<h1 class="main-title">📊 Elite AI Data Analyst Studio</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #94a3b8; font-size: 1.15rem; margin-bottom: 2rem;">Drop any corporate spreadsheet to instantly unlock executive charts, auto-analysis, and chat intelligence.</p>', unsafe_allow_html=True)

# File Uploader Space
st.markdown('<div class="section-header">📂 Upload Enterprise Dataset</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Load dataset matrix smoothly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        df.columns = df.columns.str.strip()
        
        # --- 1. DYNAMIC SUMMARY METRICS CARDS ---
        st.markdown('<div class="section-header">📋 Strategic Performance Indicators</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.95rem;font-weight:600;">TOTAL RECORDS</p><h2 style="margin:0.5rem 0 0 0;color:#38bdf8;font-size:2rem;">{df.shape[0]:,}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.95rem;font-weight:600;">DATA COLUMNS</p><h2 style="margin:0.5rem 0 0 0;color:#38bdf8;font-size:2rem;">{df.shape[1]} Columns</h2></div>', unsafe_allow_html=True)
        
        # Intelligent numeric calculation for display cards
        numeric_cols = df.select_dtypes(include=['number']).columns
        with col3:
            if len(numeric_cols) > 0:
                first_num = numeric_cols[0]
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.95rem;font-weight:600;">TOTAL ({first_num})</p><h2 style="margin:0.5rem 0 0 0;color:#34d399;font-size:1.8rem;">{df[first_num].sum():,}</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.95rem;font-weight:600;">AGGREGATE METRIC</p><h2 style="margin:0.5rem 0 0 0;color:#94a3b8;font-size:1.8rem;">N/A</h2></div>', unsafe_allow_html=True)
        with col4:
            if len(numeric_cols) > 1:
                second_num = numeric_cols[1]
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.95rem;font-weight:600;">AVG ({second_num})</p><h2 style="margin:0.5rem 0 0 0;color:#fbbf24;font-size:1.8rem;">{df[second_num].mean():.2f}</h2></div>', unsafe_allow_html=True)
            else:
                product_col = next((c for c in df.columns if 'product' in c.lower() or 'category' in c.lower() or 'item' in c.lower()), None)
                if product_col and not df[product_col].empty:
                    st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.95rem;font-weight:600;">TOP CATEGORY</p><h2 style="margin:0.5rem 0 0 0;color:#fbbf24;font-size:1.5rem;text-overflow:ellipsis;white-space:nowrap;overflow:hidden;">{df[product_col].mode()[0]}</h2></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.95rem;font-weight:600;">SECONDARY METRIC</p><h2 style="margin:0.5rem 0 0 0;color:#94a3b8;font-size:1.8rem;">N/A</h2></div>', unsafe_allow_html=True)

        # Data Frame Preview Grid
        st.markdown("<h4 style='margin-top: 1.5rem;'>Dataset Sample Grid Snippet</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(8), use_container_width=True)
        
        # --- 2. AUTOMATIC CORE VISUALIZATIONS CHARTS ---
        st.markdown('<div class="section-header">📊 Visual Data Projections</div>', unsafe_allow_html=True)
        chart_c1, chart_c2 = st.columns(2)
        
        cat_label = next((c for c in df.columns if 'name' in c.lower() or 'category' in c.lower() or 'product' in c.lower() or 'type' in c.lower()), df.columns[0])
        num_label = numeric_cols[0] if len(numeric_cols) > 0 else None
        
        with chart_c1:
            if num_label and cat_label:
                st.markdown(f"**📈 Distribution Share breakdown by {cat_label} (Bar Chart)**")
                chart_data = df.groupby(cat_label)[num_label].sum().sort_values(ascending=False).head(10)
                st.bar_chart(chart_data)
            else:
                st.info("No qualitative/quantitative dimensions available for automated charting.")
                
        with chart_c2:
            if len(numeric_cols) > 0:
                st.markdown("**📉 Continuous Data Value Trend Wave (Line Chart)**")
                st.line_chart(df[numeric_cols[0]].head(50))
            else:
                st.info("No continuous metrics available to map data streams.")

        # --- 3. DYNAMIC STRATEGIC REPORT SUMMARY BOX ---
        st.markdown('<div class="section-header">🧠 Automated AI Insight Report</div>', unsafe_allow_html=True)
        if "auto_summary" not in st.session_state:
            with st.spinner("AI Agent auditing dataset and preparing executive summaries..."):
                try:
                    summary_prompt = (
                        f"You are a Senior Chief Strategic Data Scientist. Analyze this dataset blueprint snapshot. "
                        f"Provide a crisp, professional summary in bullet points covering: Main Key Findings and Core Recommendations. "
                        f"Dataset Context:\n{df.head(15).to_string(index=False)}"
                    )
                    response = model.generate_content(summary_prompt)
                    st.session_state.auto_summary = response.text
                except Exception as ex_sum:
                    st.session_state.auto_summary = f"Reporting engine pipeline bypassed constraints cleanly: {ex_sum}"
        
        st.markdown(st.session_state.auto_summary)

        # --- 4. INTERACTIVE CONVERSATIONAL CHAT ENGINE (NO RED BOUNDARIES!) ---
        st.markdown('<div class="section-header">💬 Chat Directly With Your Data Matrix</div>', unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:0.95rem; margin-bottom:1rem;'>Have questions or doubts about the charts or findings? Ask the data intelligence chatbot below for clarifications instantly.</p>", unsafe_allow_html=True)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Stream logs cleanly
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if user_query := st.chat_input("Ask a follow-up analysis question to clear your confusion..."):
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})
            
            data_summary = f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns. Columns list: {', '.join(df.columns.tolist())}. Data sample matrix snippet:\n{df.head(5).to_string()}"
            prompt = f"You are a professional Data Intelligence Consultant. Help the user clear any confusions. Active Context:\n{data_summary}\n\nUser Question: {user_query}"
            
            with st.chat_message("assistant"):
                with st.spinner("AI parsing metrics pattern..."):
                    chat_response = model.generate_content(prompt)
                    st.markdown(chat_response.text)
            st.session_state.messages.append({"role": "assistant", "content": chat_response.text})
            
    except Exception as e:
        st.error(f"Core System Exception Logged: {str(e)}")

else:
    st.markdown("<div style='text-align: center; margin-top: 3rem; color: #64748b;'><h3>📥 Awaiting active data matrix upload to activate dashboard pipelines...</h3></div>", unsafe_allow_html=True)
    
