import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Data Analyst")
st.title("AI Data Analyst (Free Gemini)")

# API Key input
api_key = st.text_input("Enter your Google AI Studio API Key", type="password")

file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])

if file and api_key:
    try:
        genai.configure(api_key=api_key)
        # Updated to a supported model version
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Load data
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
            
        st.write("Data Preview:", df.head())
        
        # Analysis trigger
        if st.button("Analyse"):
            with st.spinner("Analyzing your dataset..."):
                # Convert dataframe to a string format the model can read easily
                data_summary = df.to_string(index=False)
                
                prompt = f"""
                You are an expert data analyst. Analyze the following dataset and provide key insights, 
                trends, and a summary of what the data shows:
                
                {data_summary}
                """
                
                # Generate the analysis
                response = model.generate_content(prompt)
                
                st.subheader("Analysis Results")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"An error occurred: {e}")
