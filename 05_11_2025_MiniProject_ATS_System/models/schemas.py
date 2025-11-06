from typing import TypedDict, Optional, List, Dict, Union
from pydantic import BaseModel, Field

# --------------------------
# 📄 Pydantic Data Models
# --------------------------

class ResumeData(BaseModel):
    name: str = Field(default="Not Found", description="Candidate name")
    email: str = Field(default="Not Found", description="Candidate email address")
    phone: str = Field(default="Not Found", description="Candidate phone number")
    skills: List[str] = Field(default_factory=list, description="List of detected skills")
    experience: Union[str, List[Dict]] = Field(default="Not specified", description="Experience summary")
    education: Union[str, List[Dict]] = Field(default="Not specified", description="Education background")

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

# --------------------------
# 🔁 State for Graph Workflow
# --------------------------

class JobMatchState(TypedDict, total=False):
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
