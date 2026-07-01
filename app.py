import streamlit as st
import pandas as pd
import openai

st.title("AI Data Analyst")
api_key = st.text_input("Apni OpenAI API Key dalein", type="password")

file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])

if file and api_key:
    client = openai.OpenAI(api_key=api_key)
    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    st.write("Data Preview:", df.head())
    
    if st.button("Analyse"):
        res = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "user", "content": f"Analyze this data: {df.to_string()}"}]
        )
        st.write(res.choices[0].message.content)
