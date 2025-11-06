from typing import Dict
from models import llm
from models.schemas import MatchingScore, JobMatchState
from langchain_core.messages import SystemMessage, HumanMessage
from utils import extract_key_skills, calculate_text_similarity, convert_to_native

def match_and_score(state: JobMatchState) -> Dict:
    """
    Computes matching by:
     - extracting summaries (key skills)
     - computing TF-IDF similarity on summaries
     - asking LLM to produce a structured MatchingScore
    Keeps original final overall_score: 60% LLM overall_score + 40% similarity_score
    """
    job_req = state.get('job_requirements', {})
    resume_data = state.get('resume_data', {})
    full_job_text = state.get('job_description_text', '') or ''
    full_resume_text = state.get('resume_text', '') or ''

    # Create concise summaries for scoring
    job_summary = extract_key_skills(full_job_text)
    resume_summary = extract_key_skills(full_resume_text)

    # Compute similarity with summaries
    similarity_score = calculate_text_similarity(job_summary, resume_summary)

    structured_llm = llm.with_structured_output(MatchingScore)
    messages = [
        SystemMessage(content="""
        Compare the job and resume summaries and respond ONLY with a JSON OBJECT matching the following schema:
        {
          "overall_score": float between 0 and 10,
          "skill_match_percentage": float between 0 and 100,
          "experience_match": boolean,
          "education_match": boolean,
          "strengths": list of strings,
          "gaps": list of strings
        }
        Do NOT return a list or any other format.
        """),
        HumanMessage(content=f"Job Summary: {job_summary}\nResume Summary: {resume_summary}")
    ]

    try:
        matching_result = structured_llm.invoke(messages)

        # Handle unexpected list response by falling back to default
        if isinstance(matching_result, list):
            print(f"Warning: Matching LLM returned a list instead of object: {matching_result}")
            matching_result = MatchingScore(
                overall_score=0.0,
                skill_match_percentage=0.0,
                experience_match=False,
                education_match=False,
                strengths=[],
                gaps=[]
            )

        match_dict = matching_result.dict()
        overall_score_value = float(match_dict.get("overall_score", 0))
        final_score = float((overall_score_value * 0.6) + (similarity_score * 0.4))
        final_score = round(final_score, 2)
        match_dict["overall_score"] = final_score

        result = {"matching_score": match_dict, "overall_score": final_score}
        return convert_to_native(result)
    except Exception as e:
        print(f"Error in matching: {e}")
        # Fallback
        result = {
            "matching_score": {
                "overall_score": similarity_score,
                "skill_match_percentage": 0.0,
                "experience_match": False,
                "education_match": False,
                "strengths": [],
                "gaps": []
            },
            "overall_score": similarity_score
        }
        return convert_to_native(result)
