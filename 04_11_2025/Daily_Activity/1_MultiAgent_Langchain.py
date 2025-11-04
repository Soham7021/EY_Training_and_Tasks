import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=512,
    api_key=api_key,
    base_url=base_url,
)

def research_agent(query: str) -> str:
    system_msg = SystemMessage(content="You are a helpful research assistant. Research and explain the topic clearly and factually.")
    user_msg = HumanMessage(content=f"Research the following topic: {query}")
    response = llm.invoke([system_msg, user_msg])
    return response.content

def summarizer_agent(text: str) -> str:
    system_msg = SystemMessage(content="You are a concise summarizer. Summarize the given text into 5 bullet points and a short paragraph.")
    user_msg = HumanMessage(content=f"Summarize this:\n{text}")
    response = llm.invoke([system_msg, user_msg])
    return response.content


def notifier_agent(summary: str, filename: str = "summary_log.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Autogen:- Notified and saved to {filename}")
        print("Notified")

def run_pipeline(query: str):
    print(f"Researching: {query}")
    research = research_agent(query)
    print("Summarizing research...")
    summary = summarizer_agent(research)
    print(summary)
    print("Saving summary to log file...")
    notifier_agent(summary)
    print("\n--- Final Summary ---\n")
    print(summary)

if __name__ == "__main__":
    run_pipeline("AI in Healthcare")