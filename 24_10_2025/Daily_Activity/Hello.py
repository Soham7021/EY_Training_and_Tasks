import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------------------------------------------------
# 1. Load environment variables
# ----------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# ----------------------------------------------------------
# 2. Initialize model (Mistral via OpenRouter)
# ----------------------------------------------------------
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# ----------------------------------------------------------
# 3. Define a dynamic ChatPromptTemplate
# ----------------------------------------------------------
prompt = ChatPromptTemplate.from_template(
    "<s>[INST] You are a concise assistant. Answer {topic} based on this {conversation}. [/INST]"
)

# Output parser converts model output to plain string
parser = StrOutputParser()

#4 creating reusable method

def generate_explanation(conversation, topic):
    chain = prompt | llm | parser
    inputt = {
        "topic": topic,
        "conversation": conversation,

    }
    response = chain.invoke(inputt)
    return response

def convo():
    conversation = ""
    while True:
        a = input("YOU: ")
        if a.lower() == "exit":
            break
        res = generate_explanation(conversation, a)
        conversation += res
        print("Assistant: ", res)

if __name__ == "__main__":
    convo()


