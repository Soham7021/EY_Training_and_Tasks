# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/process")

# Streamlit page setup
st.set_page_config(page_title="LLM Assistant", layout="centered")
st.title("🤖 Helpful LLM Assistant")

# User input
user_input = st.text_input("Ask me anything:", "")

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"text": user_input}, timeout=30)
                response.raise_for_status()
                data = response.json()
                st.subheader("Answer:")
                st.write(data.get("result", "No response"))
            except Exception as e:
                st.error(f"Request failed: {e}")
