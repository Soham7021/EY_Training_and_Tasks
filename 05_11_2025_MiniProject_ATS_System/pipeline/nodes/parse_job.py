from typing import Dict
from models import llm
from models.schemas import JobRequirements, JobMatchState
from langchain_core.messages import SystemMessage, HumanMessage

def parse_job_description(state: JobMatchState) -> Dict:
    """
    Extract job requirements from state['job_description_text'] using LLM
    Returns dict with 'job_requirements' key (matching your original behavior).
    """
    job_text = state.get('job_description_text', '') or ''

    structured_llm = llm.with_structured_output(JobRequirements)
    messages = [
        SystemMessage(content="""
        Extract job requirements from the following text.
        Provide ONLY a JSON OBJECT with fields:
        - required_skills (list of strings)
        - preferred_skills (list of strings)
        - experience_required (string)
        - education_required (string)
        - job_role (string)

        Do NOT return a list or any other format.
        Respond only with a single JSON object.
        """),
        HumanMessage(content=f"{job_text}")
    ]
    try:
        job_req = structured_llm.invoke(messages)  # JobRequirements instance
        job_dict = job_req.dict()
        return {"job_requirements": job_dict}
    except Exception as e:
        print(f"Error parsing job description: {e}")
        return {"job_requirements": {}}
