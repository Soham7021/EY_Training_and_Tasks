from .graph_builder import build_workflow

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
