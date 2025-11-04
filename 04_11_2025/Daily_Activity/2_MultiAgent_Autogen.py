from autogen import AssistantAgent
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm_config = {
    "model": "meta-llama/llama-3-8b-instruct",
    "api_key": api_key,
    "base_url": base_url,
    "temperature": 0.7,
    "max_tokens": 700,
}

researcher = AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="You are a research assistant. Research the given topic and provide factual, clear insights in about 10 concise bullet points.",
)

summarizer = AssistantAgent(
    name="Summarizer",
    llm_config=llm_config,
    system_message="You are a summarizer. Create a short summary (3–5 sentences) and 5 key bullet points from the given research notes.",
)

def notifier_agent(summary: str, filename: str = "summary_log.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Autogen:- Notified and saved to {filename}")
        print("Notified")

def run_pipeline(topic: str):
    research = researcher.generate_reply(
        messages=[{"role": "user", "content": f"Research this topic: {topic}"}]
    )
    summary = summarizer.generate_reply(
        messages=[{"role": "user", "content": f"Summarize this research:\n{research}"}]
    )
    print(summary)
    notifier_agent(summary)

if __name__ == "__main__":
    topic = "Impact of Artificial Intelligence on Healthcare"
    run_pipeline(topic)
