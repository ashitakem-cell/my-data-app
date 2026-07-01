import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Data Analyst")
st.title("AI Data Analyst (Free Gemini)")

# API Key input
api_key = st.text_input("enter your Google AI Studio API Key", type="password")

file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])

if file and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load data
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
            
        st.write("Data Preview:", df.head())
        
        if st.button("Analyse"):
            with st.spinner('AI data ko analyze kar raha hai...'):
                prompt = f"Analyze this data and provide insights: {df.to_string()}"
                response = model.generate_content(prompt)
                st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
