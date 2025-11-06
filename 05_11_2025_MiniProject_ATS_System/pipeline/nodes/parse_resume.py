from typing import Dict
from models import llm
from models.schemas import ResumeData, JobMatchState
from langchain_core.messages import SystemMessage, HumanMessage
from utils import extract_text_from_pdf, extract_email_from_text

def parse_resume(state: JobMatchState) -> Dict:
    """
    Parse resume from either state['resume_pdf'] or state['resume_text'] using LLM.
    Returns dict with keys: 'resume_data', 'candidate_email', 'resume_text'
    """
    if state.get('resume_pdf'):
        resume_text = extract_text_from_pdf(state['resume_pdf'])
    else:
        resume_text = state.get('resume_text', '') or ''

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
            # prefer the explicitly extracted email from raw text
            try:
                resume_data.email = extracted_email
            except Exception:
                # if assignment fails, ignore (keep original)
                pass
        resume_dict = resume_data.dict()
        return {"resume_data": resume_dict, "candidate_email": resume_dict.get("email", "Not Found"), "resume_text": resume_text}
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return {"resume_data": {}, "candidate_email": "Not Found", "resume_text": resume_text}
