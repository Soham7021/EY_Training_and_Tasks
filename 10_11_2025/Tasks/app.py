# streamlit_app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/process")

st.set_page_config(page_title="LangGraph Router UI", layout="centered")
st.title("LangGraph Router (Calculator | Date | LLM)")

input_text = st.text_input("Enter your query", "")
if st.button("Submit"):
    if not input_text.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Sending to backend..."):
            try:
                resp = requests.post(API_URL, json={"text": input_text}, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                st.subheader("Result")
                st.markdown(f"**Route:** `{data.get('route')}`")
                st.text_area("Output", value=str(data.get("result")), height=200)
            except Exception as e:
                st.error(f"Request failed: {e}")
