import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import TypedDict, Optional, List, Dict, Literal, Union
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
import PyPDF2
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import json
import numpy as np
from email_utils import send_email_smtp

warnings.filterwarnings("ignore")
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

class ResumeData(BaseModel):
    name: str = Field(default="Not Found")
    email: str = Field(default="Not Found")
    phone: str = Field(default="Not Found")
    skills: List[str] = Field(default_factory=list)
    experience: Union[str, List[Dict]] = Field(default="Not specified")
    education: Union[str, List[Dict]] = Field(default="Not specified")

class JobRequirements(BaseModel):
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    experience_required: str = Field(default="Not specified")
    education_required: str = Field(default="Not specified")
    job_role: str = Field(default="Not specified")

class MatchingScore(BaseModel):
    overall_score: float = Field(..., ge=0, le=10)
    skill_match_percentage: float = Field(..., ge=0, le=100)
    experience_match: bool = Field(default=False)
    education_match: bool = Field(default=False)
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)

class ResumeImprovement(BaseModel):
    missing_keywords: List[str] = Field(default_factory=list)
    skill_suggestions: List[str] = Field(default_factory=list)
    experience_suggestions: str = Field(default="")
    general_tips: List[str] = Field(default_factory=list)

class JobMatchState(TypedDict):
    job_description_text: str
    resume_text: str
    resume_pdf: Optional[bytes]
    job_requirements: Optional[Dict]
    resume_data: Optional[Dict]
    matching_score: Optional[Dict]
    overall_score: float
    improvement_suggestions: Optional[Dict]
    candidate_email: str
    email_sent: bool
    iteration: int
    max_iteration: int

def extract_key_skills(text: str, limit: int = 10) -> str:
    skill_keywords = ['python', 'c++', 'java', 'sql', 'aws', 'docker', 'kubernetes',
                      'machine learning', 'deep learning', 'nlp', 'django', 'flask', 'react']
    text_lower = text.lower()
    matched_skills = [skill for skill in skill_keywords if skill in text_lower]
    return ", ".join(matched_skills[:limit])

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def calculate_text_similarity(text1: str, text2: str) -> float:
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(similarity * 10, 2)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def extract_email_from_text(text: str) -> str:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "Not Found"

def convert_to_native(obj):
    if isinstance(obj, dict):
        return {k: convert_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native(i) for i in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj

def parse_job_description(state: JobMatchState) -> dict:
    job_text = state['job_description_text']
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

def parse_resume(state: JobMatchState) -> dict:
    if state.get('resume_pdf'):
        resume_text = extract_text_from_pdf(state['resume_pdf'])
    else:
        resume_text = state['resume_text']

    structured_llm = llm.with_structured_output(ResumeData)
    messages = [
        SystemMessage(content="""
You are an assistant that extracts structured information from a candidate's resume text.
Extract the following details as accurately as possible:
- Name
- Email
- Phone number
- List of skills (as an array of strings)
- Experience summary (either a string or list of role details)
- Education details (either a string or list of education entries)

Please respond ONLY with a JSON object containing these fields to match the ResumeData schema:
{
  "name": "...",
  "email": "...",
  "phone": "...",
  "skills": ["skill1", "skill2", ...],
  "experience": "...",
  "education": "..."
}
Respond without any additional text or commentary.
"""),
        HumanMessage(content=f"{resume_text}")
    ]
    try:
        resume_data = structured_llm.invoke(messages)  # ResumeData instance
        extracted_email = extract_email_from_text(resume_text)
        if extracted_email != "Not Found":
            resume_data.email = extracted_email
        resume_dict = resume_data.dict()
        return {"resume_data": resume_dict, "candidate_email": resume_data.email, "resume_text": resume_text}
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return {"resume_data": {}, "candidate_email": "Not Found"}

def create_summary_for_scoring(job_text: str, resume_text: str) -> tuple[str, str]:
    job_summary = extract_key_skills(job_text)
    resume_summary = extract_key_skills(resume_text)
    return job_summary, resume_summary

def match_and_score(state: JobMatchState) -> dict:
    job_req = state.get('job_requirements', {})
    resume_data = state.get('resume_data', {})
    full_job_text = state['job_description_text']
    full_resume_text = state['resume_text']

    # Create concise summaries for scoring
    job_summary = extract_key_skills(full_job_text)
    resume_summary = extract_key_skills(full_resume_text)

    # Compute similarity with summaries
    similarity_score = calculate_text_similarity(job_summary, resume_summary)

    # Prepare the structured output model
    structured_llm = llm.with_structured_output(MatchingScore)

    # Prepare the message prompt with strict schema instructions
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
        # Invoke the LLM
        matching_result = structured_llm.invoke(messages)

        # Handle unexpected list response
        if isinstance(matching_result, list):
            print(f"Warning: Matching LLM returned a list instead of object: {matching_result}")
            # Use default or extract first element if possible
            matching_result = MatchingScore(
                overall_score=0.0,
                skill_match_percentage=0.0,
                experience_match=False,
                education_match=False,
                strengths=[],
                gaps=[]
            )

        # Convert to dict and calculate final score
        match_dict = matching_result.dict()
        # Cast overall_score to float if it's not
        overall_score_value = float(match_dict.get("overall_score", 0))
        final_score = float((overall_score_value * 0.6) + (similarity_score * 0.4))
        final_score = round(final_score, 2)
        match_dict["overall_score"] = final_score

        # Build result
        result = {"matching_score": match_dict, "overall_score": final_score}
        return convert_to_native(result)
    except Exception as e:
        print(f"Error in matching: {e}")
        # Fallback in case of error
        result = {
            "matching_score": {
                "overall_score": similarity_score,
                "skill_match_percentage": 0.0,
                "experience_match": False,
                "education_match": False
            },
            "overall_score": similarity_score
        }
        return convert_to_native(result)

def generate_suggestions(state: JobMatchState) -> Dict:
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

def send_email_notification(state: JobMatchState) -> Dict:
    candidate_email = state.get('candidate_email', 'Not Found')
    candidate_name = state.get('resume_data', {}).get('name', 'Candidate')
    job_role = state.get('job_requirements', {}).get('job_role', 'the position')
    score = state.get('overall_score', 0)
    if candidate_email == "Not Found" or candidate_email == "":
        return {"email_sent": False}

    subject = f"Congratulations! You're Shortlisted for {job_role}"
    body = (
        f"Dear {candidate_name},\n\n"
        f"Congratulations! 🎉\n\n"
        f"We are pleased to inform you that your resume has been shortlisted for the position of {job_role}.\n\n"
        f"Your profile scored {score}/10 in our initial screening.\n\n"
        f"Best regards,\nRecruitment Team"
    )

    sent = send_email_smtp(candidate_email, subject, body)

    return {"email_sent": sent}

def route_based_on_score(state: JobMatchState) -> Literal["send_email", "generate_suggestions", "end"]:
    score = state.get('overall_score', 0)
    if score >= 5.0:
        return "send_email"
    else:
        return "generate_suggestions"

def build_workflow():
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

def run_job_matching_pipeline(job_description: str, resume_text: str = "", resume_pdf: bytes = None):
    workflow = build_workflow()
    initial_state = {
        "job_description_text": job_description,
        "resume_text": resume_text,
        "resume_pdf": resume_pdf,
        "iteration": 1,
        "max_iteration": 1,
        "overall_score": 0.0,
        "email_sent": False
    }
    config = {"configurable": {"thread_id": "job_matching_session_1"}}
    result = workflow.invoke(initial_state, config)
    return result
