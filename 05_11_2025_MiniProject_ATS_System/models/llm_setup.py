import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# --------------------------
# 🌐 Environment Setup
# --------------------------

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY is missing in your .env file")

# --------------------------
# 🧠 LLM Initialization
# --------------------------

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)
