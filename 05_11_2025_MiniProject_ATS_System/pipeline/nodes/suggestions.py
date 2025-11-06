from typing import Dict
from models import llm
from models.schemas import ResumeImprovement, JobMatchState
from langchain_core.messages import SystemMessage, HumanMessage

def generate_suggestions(state: JobMatchState) -> Dict:
    """
    Generates resume improvement suggestions via LLM (ResumeImprovement schema).
    Returns dict: {'improvement_suggestions': {...}}
    """
    job_req = state.get('job_requirements', {})
    resume_data = state.get('resume_data', {})
    matching_score = state.get('matching_score', {})

    structured_llm = llm.with_structured_output(ResumeImprovement)
    messages = [
        SystemMessage(content="""
        Based on the job requirements and resume, suggest resume improvements.
        Respond ONLY with a JSON OBJECT containing fields:
        - missing_keywords (list)
        - skill_suggestions (list)
        - experience_suggestions (string)
        - general_tips (list)
        """),
        HumanMessage(content=f"Job: {job_req}\nResume: {resume_data}\nScore: {matching_score}")
    ]
    try:
        suggestions = structured_llm.invoke(messages)
        return {"improvement_suggestions": suggestions.dict()}
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return {"improvement_suggestions": {}}
