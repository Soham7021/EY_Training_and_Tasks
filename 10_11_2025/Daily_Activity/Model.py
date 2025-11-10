import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime

# --- Load environment variables ---
load_dotenv()

# --- Logging setup ---
LOG_FILE = os.getenv("LOG_FILE", "llm_app.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("openrouter-llm-app")

# --- OpenRouter setup ---
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# Initialize LLM
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.2,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)

# --- FastAPI app ---
app = FastAPI(title="LLM Assistant with Date Awareness")

# --- Request schema ---
class Query(BaseModel):
    text: str

# --- Endpoint ---
@app.post("/process")
def process(query: Query):
    text = query.text.strip()
    logger.info("API /process called with: %s", text)

    if not text:
        raise HTTPException(status_code=400, detail="Empty query provided")

    # Get current date and time
    now = datetime.now()
    current_time = now.strftime("%A, %d %B %Y, %I:%M %p")

    try:
        # Include current date/time in system message
        system_prompt = (
            f"You are a helpful assistant. The current date and time is {current_time}. "
            f"Use this information to answer any questions about today's date or time. "
            f"Answer every question asked to you clearly and concisely."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text),
        ]

        response = llm.invoke(messages)
        result = getattr(response, "content", str(response))

        logger.info("Response generated successfully, length=%d", len(result))
        return {"input": text, "result": result}

    except Exception as e:
        logger.exception("LLM call failed")
        raise HTTPException(status_code=500, detail=f"LLM call failed: {e}")
