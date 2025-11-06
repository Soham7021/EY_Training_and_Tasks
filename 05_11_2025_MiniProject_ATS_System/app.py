import streamlit as st
from io import BytesIO
from pipeline.run_pipeline import run_job_matching_pipeline
from utils.pdf_utils import extract_text_from_pdf

# -------------------------------
# 🌈 Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Resume-Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 💅 Custom CSS Styling
# -------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .score-high {background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb;}
    .score-medium {background-color: #fff3cd; color: #856404; border: 2px solid #ffeaa7;}
    .score-low {background-color: #f8d7da; color: #721c24; border: 2px solid #f5c6cb;}
    .info-box {background-color: #e7f3ff; padding: 1rem; border-radius: 5px; border-left: 4px solid #2196F3; margin: 1rem 0;}
    .success-box {background-color: #d4edda; padding: 1rem; border-radius: 5px; border-left: 4px solid #28a745; margin: 1rem 0;}
    .warning-box {background-color: #fff3cd; padding: 1rem; border-radius: 5px; border-left: 4px solid #ffc107; margin: 1rem 0;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧠 Initialize Session State
# -------------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "processing" not in st.session_state:
    st.session_state.processing = False

# -------------------------------
# 🏷️ Header
# -------------------------------
st.markdown('<div class="main-header">🎯 AI-Powered Resume-Job Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Intelligent ATS System with LangGraph + LLaMA-3</div>', unsafe_allow_html=True)

# -------------------------------
# 📋 Sidebar Info
# -------------------------------
with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    1. **Paste Job Description**  
    2. **Upload Resume (PDF)** *or* **Paste Resume Text**  
    3. Click **Analyze Match**  
    4. View Score + Improvement Tips  

    ### 🎯 Scoring
    - **8–10:** ✅ Excellent Match — Email Sent  
    - **6–8:** ⚠️ Good Match — Improve Slightly  
    - **0–6:** ❌ Needs Work  

    ### 🧠 Features
    - LLM-Powered Parsing (LLaMA 3)
    - TF-IDF + Semantic Scoring
    - Smart Resume Feedback
    - Auto Email Notifications
    """)
    st.divider()
    st.info("**Model:** LLaMA-3-8B\n**Framework:** LangGraph\n**Similarity:** TF-IDF + Cosine")

# -------------------------------
# ✍️ Input Area
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Job Description")
    job_description = st.text_area(
        "Paste the Job Description:",
        height=300,
        placeholder="Example:\nSenior Python Developer\nRequirements:\n- 5+ years in Python\n- Django or FastAPI...",
        help="Paste the full job description here"
    )

with col2:
    st.subheader("👤 Resume")
    input_type = st.radio("Choose Input Method:", ["Upload PDF", "Paste Text"], horizontal=True)

    resume_text = ""
    resume_pdf = None

    if input_type == "Upload PDF":
        uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
        if uploaded_file:
            resume_pdf = uploaded_file.read()
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            with st.expander("📄 Preview Extracted Text"):
                preview = extract_text_from_pdf(resume_pdf)
                st.text_area("Extracted Text", preview[:800] + "...", height=150)
    else:
        resume_text = st.text_area(
            "Paste your Resume:",
            height=300,
            placeholder="John Doe\nEmail: john@example.com\nSkills: Python, Django, AWS...",
        )

# -------------------------------
# 🚀 Run Button
# -------------------------------
st.divider()
col_btn = st.columns([1, 2, 1])[1]
with col_btn:
    analyze_button = st.button("🚀 Analyze Match", use_container_width=True, disabled=st.session_state.processing)

if analyze_button:
    if not job_description.strip():
        st.error("❌ Please provide a job description.")
    elif input_type == "Upload PDF" and not resume_pdf:
        st.error("❌ Please upload your resume PDF.")
    elif input_type == "Paste Text" and not resume_text.strip():
        st.error("❌ Please paste your resume text.")
    else:
        st.session_state.processing = True
        with st.spinner("🤖 Analyzing your resume... please wait 30–60 seconds"):
            try:
                results = run_job_matching_pipeline(
                    job_description=job_description,
                    resume_text=resume_text if input_type == "Paste Text" else None,
                    resume_pdf=resume_pdf if input_type == "Upload PDF" else None
                )
                st.session_state.results = results
                st.session_state.processing = False
                st.success("✅ Analysis Complete!")
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
                st.exception(e)
                st.session_state.processing = False

# -------------------------------
# 📊 Results Display
# -------------------------------
if st.session_state.results:
    r = st.session_state.results
    st.divider()
    st.header("📊 Match Analysis")

    score = r.get("overall_score", 0)
    match = r.get("matching_score", {})
    suggestions = r.get("improvement_suggestions", {})

    # Score Box
    if score >= 8:
        cls, emoji, text = "score-high", "🎉", "Excellent Match!"
    elif score >= 6:
        cls, emoji, text = "score-medium", "⚠️", "Good Match with Room to Improve"
    else:
        cls, emoji, text = "score-low", "🧩", "Needs Major Improvements"

    st.markdown(f"""
    <div class="score-box {cls}">
        {emoji} Overall Score: <b>{score}/10</b><br>
        <small>{text}</small>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    st.subheader("📈 Detailed Metrics")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Skills Match", f"{match.get('skill_match_percentage', 0):.1f}%")
    col_m2.metric("Experience Match", "✅ Yes" if match.get('experience_match') else "❌ No")
    col_m3.metric("Education Match", "✅ Yes" if match.get('education_match') else "❌ No")

    # Strengths & Gaps
    st.subheader("💪 Strengths & 🎯 Gaps")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        for s in match.get("strengths", []):
            st.markdown(f"✅ {s}")
    with col_s2:
        for g in match.get("gaps", []):
            st.markdown(f"⚠️ {g}")

    # Email Info
    if r.get("email_sent"):
        st.markdown(
            f"<div class='success-box'>📧 Email sent to <b>{r.get('candidate_email', 'candidate')}</b>!</div>",
            unsafe_allow_html=True
        )

    # Suggestions
    if suggestions and score < 8:
        st.subheader("💡 Improvement Suggestions")
        if suggestions.get("missing_keywords"):
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**Missing Keywords:**")
            for kw in suggestions["missing_keywords"]:
                st.markdown(f"- {kw}")
            st.markdown('</div>', unsafe_allow_html=True)

        if suggestions.get("skill_suggestions"):
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**Skills to Add/Emphasize:**")
            for sk in suggestions["skill_suggestions"]:
                st.markdown(f"- {sk}")
            st.markdown('</div>', unsafe_allow_html=True)

        if suggestions.get("experience_suggestions"):
            st.markdown(f"<div class='warning-box'>{suggestions['experience_suggestions']}</div>", unsafe_allow_html=True)

        if suggestions.get("general_tips"):
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**General Tips:**")
            for tip in suggestions["general_tips"]:
                st.markdown(f"- {tip}")
            st.markdown('</div>', unsafe_allow_html=True)

    # Resume & Job Info Expanders
    st.divider()
    with st.expander("👤 Candidate Info"):
        st.json(r.get("resume_data", {}))
    with st.expander("📋 Job Requirements"):
        st.json(r.get("job_requirements", {}))

    st.divider()
    if st.button("🔄 Analyze Another Resume", use_container_width=True):
        st.session_state.results = None

# -------------------------------
# 🧾 Footer
# -------------------------------
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; padding: 2rem 0;'>
    <p>Built with ❤️ using LangGraph, Streamlit, and LLaMA-3</p>
    <p>© 2025 AI Resume-Job Matcher | Powered by Advanced NLP</p>
</div>
""", unsafe_allow_html=True)
