import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (Fixing the Red Line & Enhancing UI)
st.markdown("""
    <style>
    /* Main app background and font */
    .main {
        background-color: #0f1116;
        color: #e2e8f0;
    }
    
    /* Elegant Title Styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ff4b4b, #ff7676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* KPI Card Styling */
    .metric-card {
        background: #1e222b;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ff4b4b;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
    }
    
    /* Removing the strange red border from input elements */
    div[data-testid="stTextInput"] > div {
        border: 1px solid #2e3440 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }
    div[data-testid="stTextInput"] > div:focus-within {
        border-color: #ff4b4b !important;
        box-shadow: 0 0 0 1px #ff4b4b !important;
    }
    
    /* Chat Input styling fix */
    .stChatInputContainer {
        border-color: #2e3440 !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #ff4b4b !important;
    }
    
    /* Modern Dashboard Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f8fafc;
        border-bottom: 2px solid #2e3440;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🛠️ Configuration")
    api_key = st.text_input("Enter Google AI Studio API Key", type="password", help="Get your key from Google AI Studio")
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.info("Upload your CSV or Excel sheet, then ask the AI to perform complex analysis, draw insights, or summarize trends instantly!")

# Main Title Area
st.markdown('<h1 class="main-title">📊 AI Data Analyst</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #94a3b8; font-size: 1.1rem;">Advanced data insights powered by Gemini</p>', unsafe_allow_html=True)

# File Uploader Container
st.markdown('<div class="section-header">📂 Upload Dataset</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file and api_key:
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        # Using the updated recommended model name for tabular/text tasks
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load Data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Layout: Visual KPIs
        st.markdown('<div class="section-header">📈 High-Level Summary</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.9rem;">Total Rows</p><h2 style="margin:0;color:#fff;">{df.shape[0]:,}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.9rem;">Total Columns</p><h2 style="margin:0;color:#fff;">{df.shape[1]}</h2></div>', unsafe_allow_html=True)
        
        # If numeric columns exist, show aggregated values dynamically
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            with col3:
                first_num = numeric_cols[0]
                st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.9rem;">Total {first_num}</p><h2 style="margin:0;color:#fff;">{df[first_num].sum():,}</h2></div>', unsafe_allow_html=True)
            if len(numeric_cols) > 1:
                with col4:
                    second_num = numeric_cols[1]
                    st.markdown(f'<div class="metric-card"><p style="margin:0;color:#94a3b8;font-size:0.9rem;">Avg {second_num}</p><h2 style="margin:0;color:#fff;">{df[second_num].mean():.2f}</h2></div>', unsafe_allow_html=True)

        # Data Preview
        st.markdown('<div class="section-header">👀 Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)
        
        # AI Interaction Agent Section
        st.markdown('<div class="section-header">🤖 Strategic Data Intelligence Agent</div>', unsafe_allow_html=True)
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if user_query := st.chat_input("Ask a strategic analytics question or request insights..."):
            with st.chat_message("user"):
                st.markdown(user_query)
            st.session_state.messages.append({"role": "user", "content": user_query})
            
            # Context generation for Gemini
            data_summary = f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns. Columns: {', '.join(df.columns.tolist())}. Sample data snippet:\n{df.head(3).to_string()}"
            prompt = f"You are an expert Data Analyst. Context about the data:\n{data_summary}\n\nUser Question: {user_query}"
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing data and generating trends..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        
elif not api_key and uploaded_file:
    st.info("⚠️ Please enter your Google AI Studio API Key in the sidebar to begin analysis.")
