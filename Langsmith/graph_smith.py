# !pip install -U langchain langchain-openai openai
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import TypedDict, Optional
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph,START, END
from pydantic import BaseModel, Field


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)



class EmailEvaluation(BaseModel):
    score: float = Field(..., ge=0, le=10, description="Evaluation score of the email on a scale from 0 to 10.")
    feedback: str = Field(..., description="Constructive feedback explaining the score and how the email can be improved.")


class EmailState(TypedDict):
  email_topic: str
  email: str
  score: float
  # history: list[]
  # approved: bool
  iteration: int
  max_iteration: int


def Writer(state: EmailState):
  message = [
      SystemMessage(content="You are a very average Email writer and you learn slowly"),
      HumanMessage(content=f"""Write a Email on this topic{state['email_topic']}""")
  ]
  response = llm.invoke(message).content
  return {'email': response}

evaluator_llm = llm.with_structured_output(EmailEvaluation)
def Evaluator(state: EmailState):
    message = [
        SystemMessage(
            content=(
                "You are an email evaluation assistant. "
                "Evaluate the following email and respond ONLY in JSON format with the following fields: "
                "{'score': <float from 0 to 10>, 'feedback': <string>}. "
                "Do not include any text outside the JSON."
            )
        ),
        HumanMessage(content=state['email'])
    ]
    response = evaluator_llm.invoke(message)
    # return {'score': response.score}
    return {'score': response.score, 'feedback': response.feedback}


def Optimizer(state:EmailState):
  message = [
    SystemMessage(content="You smart Email Writer You little Optimize the given Email"),
    HumanMessage(content=state['email'])
  ]
  response = llm.invoke(message).content
  iteration = state['iteration'] + 1
  return {'email': response, 'iteration': iteration}

def router(state:EmailState):
  if state['score']>=9 or state['iteration']>=state['max_iteration']:
    return 'Approved'
  else:
    return "Not_Approved"

graph = StateGraph(EmailState)
graph.add_node("Writer", Writer)
graph.add_node("Evaluator", Evaluator)
graph.add_node("Optimizer", Optimizer)


graph.add_edge(START, 'Writer')
graph.add_edge('Writer', 'Evaluator')
graph.add_conditional_edges('Evaluator', router, {'Approved': END, 'Not_Approved': 'Optimizer'})
graph.add_edge('Optimizer', 'Evaluator')

checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer=checkpointer)
config1 = {"configurable": {"thread_id": "1"}}

initial_state = {
    "email_topic": "Resignation",
    "iteration": 1,
    "max_iteration": 5
}

result = workflow.invoke(initial_state, config1)

# print(result['email'])

print(result)

