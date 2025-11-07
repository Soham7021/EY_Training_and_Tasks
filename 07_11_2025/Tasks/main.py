import os
import json
from langchain_openai import ChatOpenAI
from fastapi import FastAPI
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

app = FastAPI()
client = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

HISTORY_FILE = "history.json"


class Prompt(BaseModel):
    query: str


app.mount("/static", StaticFiles(directory="."), name="static")
@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/generate")
async def generate_response(prompt: Prompt):
    if not prompt.query or not prompt.query.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Query cannot be empty or just whitespace."}
        )

    try:
        response = client.invoke([
            SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content=prompt.query)
        ])

        answer = response.content

        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)

        history.append({"question": prompt.query, "answer": answer})

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

        return {"response": answer}
    except Exception as e:
        return {"error": str(e)}
