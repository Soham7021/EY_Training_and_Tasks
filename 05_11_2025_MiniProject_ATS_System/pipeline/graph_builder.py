from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from models.schemas import JobMatchState
from pipeline.nodes import (
    parse_job_description,
    parse_resume,
    match_and_score,
    generate_suggestions,
    send_email_notification
)
from typing import Literal

def route_based_on_score(state: JobMatchState) -> Literal["send_email", "generate_suggestions", "end"]:
    score = state.get('overall_score', 0)
    if score >= 5.0:
        return "send_email"
    else:
        return "generate_suggestions"

def build_workflow():
    """
    Build and compile the LangGraph StateGraph with the same structure you had.
    """
    graph = StateGraph(JobMatchState)
    graph.add_node("parse_job_description", parse_job_description)
    graph.add_node("parse_resume", parse_resume)
    graph.add_node("match_and_score", match_and_score)
    graph.add_node("generate_suggestions", generate_suggestions)
    graph.add_node("send_email", send_email_notification)

    graph.add_edge(START, "parse_job_description")
    graph.add_edge("parse_job_description", "parse_resume")
    graph.add_edge("parse_resume", "match_and_score")
    graph.add_conditional_edges(
        "match_and_score",
        route_based_on_score,
        {"send_email": "send_email", "generate_suggestions": "generate_suggestions", "end": END}
    )
    graph.add_edge("send_email", END)
    graph.add_edge("generate_suggestions", END)

    checkpointer = InMemorySaver()
    workflow = graph.compile(checkpointer=checkpointer)
    return workflow
