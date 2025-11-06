from typing import Dict
from utils import send_email_smtp
from models.schemas import JobMatchState

def send_email_notification(state: JobMatchState) -> Dict:
    """
    Sends a congratulatory email to candidate if email exists.
    Mirrors logic and templating from original monolith.
    """
    candidate_email = state.get('candidate_email', 'Not Found') or 'Not Found'
    resume_data = state.get('resume_data', {}) or {}
    candidate_name = resume_data.get('name', 'Candidate')
    job_role = state.get('job_requirements', {}).get('job_role', 'the position')
    score = state.get('overall_score', 0)

    if candidate_email in ("Not Found", "", None):
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
