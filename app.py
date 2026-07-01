import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("AI Data Analyst (Free Gemini)")

# API Key input
api_key = st.text_input("Apni Google AI Studio API Key dalein", type="password")

file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])

if file and api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    st.write("Data Preview:", df.head())
    
    if st.button("Analyse"):
        prompt = f"Analyze this data: {df.to_string()}"
        response = model.generate_content(prompt)
        st.write(response.text)
