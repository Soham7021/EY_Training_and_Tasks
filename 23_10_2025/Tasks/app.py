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
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>AI Chat Assistant</h1>", unsafe_allow_html=True)

# System Message input field
system_message = st.text_area(
    "System Message",
    "You are a helpful and concise AI assistant.",
    height=100,
    key="system_message"
)

# Human Message input field
human_message = st.text_area(
    "Human Message",
    "",
    height=150,
    key="human_message"
)

# Custom Button Style
submit_button = st.button("Submit", use_container_width=True)

# Chat container for displaying conversation
chat_container = st.container()


# Function to display message in chat
def display_message(sender, message):
    if sender == "Assistant":
        st.markdown(
            f"<div style='background-color: #f0f0f0; border-radius: 12px; padding: 10px; margin: 5px; font-size: 16px;'>"
            f"<strong>{sender}:</strong> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='background-color: #4CAF50; color: white; border-radius: 12px; padding: 10px; margin: 5px; font-size: 16px;'>"
            f"<strong>{sender}:</strong> {message}</div>", unsafe_allow_html=True)


# Handle the submit button press
if submit_button:
    if human_message.strip():  # Check if there is a human message
        # 4. Prepare messages
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=f"<s>[INST] {human_message.strip()} [/INST]"),
        ]

        try:
            # 5. Invoke model and get response
            response = llm.invoke(messages)
            assistant_reply = response.content.strip() or "(no content returned)"

            # Display messages in chat
            display_message("Human", human_message.strip())
            display_message("Assistant", assistant_reply)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a message for the assistant.")

# Optional: Styling (to make it more beautiful)
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 15px 24px;
        border-radius: 5px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #45a049;
    }

    .stTextArea textarea {
        font-size: 16px;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #ddd;
        width: 100%;
        background-color: #f9f9f9;
    }

    .stTextArea textarea:focus {
        border-color: #4CAF50;
        outline: none;
    }

    .stTextArea label {
        font-size: 18px;
        color: #333;
    }

    .stMarkdown {
        font-size: 16px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

