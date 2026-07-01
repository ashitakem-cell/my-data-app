import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page configuration for production feel
st.set_page_config(
    page_title="Enterprise AI Insights Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Ultra-Clean Glow Layout & Zero-Red-Line Styling
st.markdown("""
    <style>
    /* Main Theme Matrix */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    /* Sleek Title Design */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #58a6ff 0%, #f2ea79 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    /* Symmetric Executive KPI Cards */
    .metric-card {
        background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
        padding: 1.6rem;
        border-radius: 14px;
        border: 1px solid #30363d;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .metric-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 10px 30px rgba(88, 166, 255, 0.15);
        transform: translateY(-3px);
    }
    
    /* Custom Responsive Layout Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
    }
    
    /* Input & Focus Overrides (No more bizarre red halos) */
    div[data-testid="stChatInputContainer"], div[data-testid="stTextInput"] > div {
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }
    div[data-testid="stChatInputContainer"]:focus-within, div[data-testid="stTextInput"] > div:focus-within {
        border-color: #58a6ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔒 ROBUST CLOUD CREDENTIALS MANAGEMENT
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
elif "google_api_key" in st.secrets: 
    API_KEY = st.secrets["google_api_key"]
else:
    st.error("🔒 Configuration Error: 'GEMINI_API_KEY' not discovered inside Streamlit Secrets infrastructure.")
    st.stop()

# Initialize Gemini engine smoothly
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sleek and minimal managed sidebar
with st.sidebar:
    st.markdown("<h2 style='color:#fff; font-size: 1.6rem;'>⚙️ Studio Settings</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Engine Status")
    st.success("Core Engine: Active & Protected")
    st.markdown("---")
    st.markdown("💡 **LinkedIn Hook:** Copy your deployed application URL and share a clean screen recording to show the world how seamless your interface handles multi-format tables.")

# Core App Title Layout
st.markdown('<h1 class="main-title">📊 Enterprise AI Insights Studio</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem;">A fail-safe data intelligence engine built for high-performance executive analysis and matrix interactions.</p>', unsafe_allow_html=True)

# Main File Receiver Input
st.markdown('<div class="section-header">📂 Data Ingestion</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Step 1: Bulletproof File Loading Protection
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Clean whitespaces from column keys to protect down-stream analysis
        df.columns = df.columns.str.strip()
        
        # Step 2: Fallback-Safe Intelligent Column Identification
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Determine logical charts parameters without indexing out of bounds
        sales_col = next((c for c in df.columns if 'sales' in c.lower() or 'amount' in c.lower() or 'price' in c.lower()), None)
        profit_col = next((c for c in df.columns if 'profit' in c.lower() or 'gain' in c.lower()), None)
        product_col = next((c for c in df.columns if 'product' in c.lower() or 'category' in c.lower() or 'item' in c.lower()), None)
        
        # --- EXEC EXECUTIVE DASHBOARD GRID ---
        st.markdown('<div class="section-header">📋 Core Performance Indicators</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">TOTAL RECORDS</p><h2 style="margin:0.4rem 0 0 0;color:#58a6ff;font-size:1.8rem;">{df.shape[0]:,}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">DIMENSIONALITY</p><h2 style="margin:0.4rem 0 0 0;color:#58a6ff;font-size:1.8rem;">{df.shape[1]} Columns</h2></div>', unsafe_allow_html=True)
        
        with col3:
            if sales_col:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">GROSS VOLUME</p><h2 style="margin:0.4rem 0 0 0;color:#34d399;font-size:1.6rem;text-overflow:ellipsis;white-space:nowrap;overflow:hidden;">₹{df[sales_col].sum():,.2f}</h2></div>', unsafe_allow_html=True)
            elif len(numeric_cols) > 0:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">AGGREGATE ({numeric_cols[0]})</p><h2 style="margin:0.4rem 0 0 0;color:#34d399;font-size:1.6rem;">{df[numeric_cols[0]].sum():,}</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">GROSS VOLUME</p><h2 style="margin:0.4rem 0 0 0;color:#8b949e;font-size:1.6rem;">N/A</h2></div>', unsafe_allow_html=True)
                
        with col4:
            if profit_col:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">OPERATIONAL PROFIT</p><h2 style="margin:0.4rem 0 0 0;color:#ff7b72;font-size:1.6rem;">₹{df[profit_col].sum():,.2f}</h2></div>', unsafe_allow_html=True)
            elif product_col and not df[product_col].empty:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">DOMINANT CLASS</p><h2 style="margin:0.4rem 0 0 0;color:#ff7b72;font-size:1.4rem;text-overflow:ellipsis;white-space:nowrap;overflow:hidden;">{df[product_col].mode()[0]}</h2></div>', unsafe_allow_html=True)
            elif len(text_cols) > 0 and not df[text_cols[0]].empty:
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">TOP MODE ({text_cols[0]})</p><h2 style="margin:0.4rem 0 0 0;color:#ff7b72;font-size:1.4rem;text-overflow:ellipsis;white-space:nowrap;overflow:hidden;">{df[text_cols[0]].mode()[0]}</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><p style="margin:0;color:#8b949e;font-size:0.9rem;font-weight:600;">OPERATIONAL INSIGHT</p><h2 style="margin:0.4rem 0 0 0;color:#8b949e;font-size:1.6rem;">N/A</h2></div>', unsafe_allow_html=True)

        # Dynamic Grid Preview Snap
        st.markdown("<h4 style='margin-top: 1.5rem; color:#f0f6fc;'>Ingested Spreadsheet Grid Snippet</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(6), use_container_width=True)
        
        # --- AUTOMATIC VISUAL PROJECTIONS ROW (FAIL-SAFE) ---
        st.markdown('<div class="section-header">📊 Automatic Fail-Safe Data Trends</div>', unsafe_allow_html=True)
        chart_c1, chart_c2 = st.columns(2)
        
        # Determine charting targets dynamically with secure logic
        cat_target = product_col if product_col else (text_cols[0] if len(text_cols) > 0 else df.columns[0])
        num_target = sales_col if sales_col else (numeric_cols[0] if len(numeric_cols) > 0 else None)
        
        with chart_c1:
            if num_target and cat_target:
                st.markdown(f"**📈 Categorical Density Breakdown by {cat_target}**")
                chart_data = df.groupby(cat_target)[num_target].sum().sort_values(ascending=False).head(10)
                st.bar_chart(chart_data)
            else:
                # If no numeric column is present, safely plot record counts instead of breaking!
                st.markdown(f"**📈 Structural Entity Frequency Count ({cat_target})**")
                chart_data = df[cat_target].value_counts().head(10)
                st.bar_chart(chart_data)
                
        with chart_c2:
            if len(numeric_cols) > 0:
                st.markdown(f"**📉 Sequential Value Flow Profile ({numeric_cols[0]})**")
                st.line_chart(df[numeric_cols[0]].head(60))
            else:
                st.info("Continuous data missing. Line-chart generation pipeline bypassed gracefully.")

        # --- MANAGED AI STRATEGIC REPORT ---
        st.markdown('<div class="section-header">🧠 Automated AI Insight Report</div>', unsafe_allow_html=True)
        if "auto_summary" not in st.session_state:
            with st.spinner("AI Engine generating strategic data report layers..."):
                try:
                    # Creating a bulletproof sample context string
                    sample_str = df.head(15).to_string(index=False)
                    summary_prompt = (
                        f"You are a World-Class Chief Data Analytics Officer. Review this enterprise dataset summary information. "
                        f"Provide a beautifully structured report using neat markdown bullets. Key areas: Principal Findings, "
                        f"and Executive Strategic Action Plan. Ingested Data Context:\n{sample_str}"
                    )
                    response = model.generate_content(summary_prompt)
                    st.session_state.auto_summary = response.text
                except Exception as ex_sum:
                    st.session_state.auto_summary = f"Automated reporting infrastructure fallback executed. Summary metrics: {len(df.columns)} columns parsed."
        
        st.markdown(st.session_state.auto_summary)

        # --- CHAT ENGINE ROOM WITH COMPREHENSIVE DATA KNOWLEDGE ---
        st.markdown('<div class="section-header">💬 Chat Directly With Your Data Studio</div>', unsafe_allow_html=True)
        st.markdown("<p style='color:#8b949e; font-size:0.95rem; margin-bottom:1rem;'>Have deeper questions or edge-case confusion regarding this dataset? Enter your prompt below for instant real-time AI resolution.</p>", unsafe_allow_html=True)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if user_query := st.chat_input("Ask a follow-up analytics question to clarify any confusion..."):
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})
            
            # Formulating fully informed robust LLM context to prevent hallucinations or chat error state
            data_summary = (
                f"Dataset Summary: {df.shape[0]} total rows and {df.shape[1]} columns. "
                f"Available Headers: {', '.join(df.columns.tolist())}.\n"
                f"Data Preview Snippet Context Matrix:\n{df.head(10).to_string()}"
            )
            
            prompt = (
                f"You are a professional Data Intelligence Consultant. Answer the user prompt accurately based on the active data. "
                f"If the user asks an out-of-bounds or irrelevant question that cannot be answered by the data, guide them back politely "
                f"with a high-value corporate response. Dataset Context:\n{data_summary}\n\nUser Question: {user_query}"
            )
            
            with st.chat_message("assistant"):
                with st.spinner("AI interpreting data arrays..."):
                    try:
                        chat_response = model.generate_content(prompt)
                        st.markdown(chat_response.text)
                        st.session_state.messages.append({"role": "assistant", "content": chat_response.text})
                    except Exception as chat_err:
                        error_msg = f"Chat interface exception handled cleanly: {str(chat_err)}"
                        st.markdown(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
    except Exception as e:
        st.error(f"Ingestion Pipeline Guard Blocked a Terminal Exception: {str(e)}")

else:
    st.markdown("<div style='text-align: center; margin-top: 4rem; color: #8b949e;'><h3>📥 Core pipeline standby: Awaiting corporate matrix upload to populate live cells...</h3></div>", unsafe_allow_html=True)
