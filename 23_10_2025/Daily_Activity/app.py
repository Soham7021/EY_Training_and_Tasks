import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# 2. Initialize LangChain model pointing to OpenRouter
llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# 3. Set up Streamlit UI
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖")

# Title of the app
st.title("AI Chat Assistant")

# System Message input field
system_message = st.text_area("System Message", "You are a helpful and concise AI assistant.", height=100)

# Human Message input field
human_message = st.text_area("Human Message", "", height=150)

# Submit Button to trigger model invocation
if st.button("Submit"):
    if human_message:
        # 4. Prepare messages
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"<s>[INST] {human_message} [/INST]"),
        ]

        try:
            # 5. Invoke model and get response
            response = llm.invoke(messages)
            st.markdown(f"**Assistant:** {response.content.strip() or '(no content returned)'}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a human message to get a response.")

# Optional: Styling (to make it more beautiful)
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 5px;
        cursor: pointer;
    }

    .stButton>button:hover {
        background-color: #45a049;
    }

    .stTextArea textarea {
        font-size: 16px;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #ddd;
    }

    .stTextArea textarea:focus {
        border-color: #4CAF50;
    }

    .stMarkdown {
        font-size: 16px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)
