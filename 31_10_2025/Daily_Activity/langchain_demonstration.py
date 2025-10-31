import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

prompt_summary = ChatPromptTemplate.from_template(
    "<s>[INST] You are a concise assistant. Based on the conversation so far: {conversation_history}, summarize the topic '{topic}' in simple terms in two to three lines only. [/INST]"
)

prompt_quiz = ChatPromptTemplate.from_template(
    "<s>[INST] Based on the conversation so far: {conversation_history}, generate one question quiz on the topic '{summary}' with MCQ and answers at the end. [/INST]"
)

parser = StrOutputParser()

def multiply(a: int, b: int) -> int:
    return a * b

def generate_summary(conversation_history, topic):
    chain = prompt_summary | llm | parser
    response = chain.invoke({
        "conversation_history": conversation_history,
        "topic": topic
    })
    return response

def generate_quiz(conversation_history, summary):
    chain = prompt_quiz | llm | parser
    response = chain.invoke({
        "conversation_history": conversation_history,
        "summary": summary
    })
    return response

def conversation():
    conversation_history = ""
    while True:
        user_input = input("User Input: ")
        if user_input.lower() == "exit":
            print("Thank You!")
            break

        if user_input.lower().startswith("multiply"):
            try:
                parts = user_input.split()
                a, b = int(parts[1]), int(parts[2])
                result = multiply(a, b)
                print("Tool:", result)
                conversation_history += f"User: {user_input}\nAssistant: {result}\n"
                continue
            except Exception:
                print("Agent: Please use 'Multiply a b' format.")
                continue

        summary_response = generate_summary(conversation_history, user_input)
        print("\nSummary of the Topic:")
        print(summary_response)

        quiz_response = generate_quiz(conversation_history, summary_response)
        print("\nQuiz on the Topic:")
        print(quiz_response)

        conversation_history += (
            f"User: {user_input}\nAssistant: {summary_response}\nQuiz: {quiz_response}\n"
        )
        print("\nUpdated Conversation History:")
        print(conversation_history)

if __name__ == '__main__':
    conversation()
