import os
import logging
import ast
import operator as op
from datetime import datetime
from typing import TypedDict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# LangGraph & LangChain imports
from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# --- Load environment variables ---
load_dotenv()

# --- Logging setup ---
LOG_FILE = os.getenv("LOG_FILE", "graph_app.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("langgraph-app")

# --- OpenRouter API setup ---
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.2,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)

# --- Graph State ---
class AgentState(TypedDict):
    text: str
    route: str
    result: str


app = FastAPI(title="LangGraph Router API")

# --- Safe calculator helper ---
ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}


def safe_eval_expr(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPS:
            return ALLOWED_OPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPS:
            return ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Unsupported expression")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)


# --- Node definitions ---
def router_node(state: AgentState) -> AgentState:
    text = state.get("text", "").lower().strip()
    logger.info("Router received: %s", text)

    if any(k in text for k in ("+", "-", "*", "/", "power", "sum", "minus", "calculate")):
        state["route"] = "calculator"
    elif any(w in text for w in ("date", "today", "day", "month", "year")):
        state["route"] = "date"
    else:
        state["route"] = "ans"

    logger.info("Router chose route: %s", state["route"])
    return state


def calculator_node(state: AgentState) -> AgentState:
    text = state.get("text", "")
    expr = text
    for token in ("calculate", "what is", "what's", "compute", "evaluate"):
        expr = expr.replace(token, "")
    expr = expr.strip()

    try:
        value = safe_eval_expr(expr)
        state["result"] = f"Result: {value}"
    except Exception as e:
        state["result"] = f"Calculator error: {str(e)}"
    logger.info("Calculator result: %s", state["result"])
    return state


def date_node(state: AgentState) -> AgentState:
    now = datetime.now()
    if "today" in state["text"].lower():
        state["result"] = f"Today's date is {now.strftime('%A, %d %B %Y')}"
    else:
        state["result"] = now.isoformat()
    logger.info("Date node result: %s", state["result"])
    return state


def ans_node(state: AgentState) -> AgentState:
    prompt = state.get("text", "")
    logger.info("LLM node sending to model: %s", prompt)
    try:
        out = llm.invoke([HumanMessage(content=prompt)])
        if hasattr(out, "content"):
            answer = out.content
        elif isinstance(out, list):
            answer = out[0].content
        elif hasattr(out, "generations"):
            answer = out.generations[0][0].text
        else:
            answer = str(out)
    except Exception as e:
        logger.exception("LLM call failed")
        answer = f"LLM call failed: {e}"

    state["result"] = answer
    logger.info("LLM node result length: %d", len(state["result"]))
    return state


# --- LangGraph Definition ---
Graph = StateGraph(AgentState)
Graph.add_node("router", router_node)
Graph.add_node("calculator", calculator_node)
Graph.add_node("date", date_node)
Graph.add_node("ans", ans_node)

Graph.add_edge(START, "router")


def route_condition(state: AgentState) -> str:
    return state.get("route", "ans")


Graph.add_conditional_edges("router", route_condition, {
    "calculator": "calculator",
    "date": "date",
    "ans": "ans",
})

Graph.set_finish_point("calculator")
Graph.set_finish_point("date")
Graph.set_finish_point("ans")

runnable = Graph.compile()

# --- API Schema ---
class Query(BaseModel):
    text: str


@app.post("/process")
def process(query: Query):
    text = query.text
    logger.info("API /process called with: %s", text)
    initial = {"text": text, "route": "", "result": ""}
    try:
        out = runnable.invoke(initial)
    except Exception as e:
        logger.exception("Graph run failed")
        raise HTTPException(status_code=500, detail=str(e))
    return {"input": text, "route": out.get("route"), "result": out.get("result")}
