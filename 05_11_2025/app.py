import streamlit as st
from io import BytesIO
from graph_pipeline import run_job_matching_pipeline, extract_text_from_pdf

st.set_page_config(
    page_title="AI Resume-Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

if 'results' not in st.session_state:
    st.session_state.results = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

st.markdown('<div class="main-header">🎯 AI-Powered Resume-Job Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Intelligent ATS System with LangGraph</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    1. **Paste Job Description** in the text area
    2. **Upload Resume** (PDF) OR paste resume text
    3. Click **Analyze Match** button
    4. View your matching score and suggestions

    ### Scoring System
    - **8-10**: ✅ Excellent Match - Email sent
    - **6-8**: ⚠️ Good Match - Improvements suggested
    - **0-6**: ❌ Needs Work - Major improvements needed

    ### Features
    - ✨ AI-powered resume parsing
    - 🎯 Intelligent skill matching
    - 📊 Detailed scoring analysis
    - 💡 Actionable improvement suggestions
    - 📧 Auto-email for qualified candidates
    """)
    st.divider()
    st.markdown("### ⚙️ System Info")
    st.info("**Model**: LLaMA-3-8B\n**Framework**: LangGraph\n**NLP**: TF-IDF + Cosine Similarity")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Job Description")
    job_description = st.text_area(
        "Paste the job description here:",
        height=300,
        placeholder="Example:\n\nSenior Python Developer\nRequired Skills:\n- 5+ years Python experience\n...",
        help="Copy and paste the complete job description"
    )

with col2:
    st.subheader("👤 Resume")
    resume_input_method = st.radio(
        "Choose input method:",
        ["Upload PDF", "Paste Text"],
        horizontal=True
    )

    resume_text = ""
    resume_pdf = None

    if resume_input_method == "Upload PDF":
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF only)",
            type=['pdf'],
            help="Upload a PDF file of your resume"
        )
        if uploaded_file is not None:
            resume_pdf = uploaded_file.read()
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            with st.expander("📄 Preview extracted text"):
                preview_text = extract_text_from_pdf(resume_pdf)
                st.text_area("Extracted Text", preview_text[:500] + "...", height=150)
    else:
        resume_text = st.text_area(
            "Paste your resume here:",
            height=300,
            placeholder="Example:\n\nJohn Doe\njohn.doe@email.com\nSenior Engineer...\n\nSkills: Python, Django, ...",
            help="Copy and paste your complete resume"
        )

st.divider()
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_button = st.button(
        "🚀 Analyze Match",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.processing
    )

if analyze_button:
    if not job_description or not job_description.strip():
        st.error("❌ Please provide a job description!")
    elif resume_input_method == "Upload PDF" and resume_pdf is None:
        st.error("❌ Please upload a resume PDF!")
    elif resume_input_method == "Paste Text" and (not resume_text or not resume_text.strip()):
        st.error("❌ Please paste your resume text!")
    else:
        st.session_state.processing = True
        with st.spinner("🔄 Analyzing resume... This may take 30-60 seconds..."):
            try:
                if resume_input_method == "Upload PDF":
                    results = run_job_matching_pipeline(
                        job_description=job_description,
                        resume_pdf=resume_pdf
                    )
                else:
                    results = run_job_matching_pipeline(
                        job_description=job_description,
                        resume_text=resume_text
                    )
                st.session_state.results = results
                st.session_state.processing = False
                st.success("✅ Analysis complete!")
                # st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.exception(e)
                st.session_state.processing = False

# Display results if available
if st.session_state.results:
    results = st.session_state.results
    st.divider()
    st.header("📊 Analysis Results")
    score = results.get('overall_score', 0)
    if score >= 8:
        score_class, score_emoji, score_text = "score-high", "🎉", "Excellent Match!"
    elif score >= 6:
        score_class, score_emoji, score_text = "score-medium", "⚠️", "Good Match with Room for Improvement"
    else:
        score_class, score_emoji, score_text = "score-low", "📝", "Needs Significant Improvement"

    st.markdown(
        f'<div class="score-box {score_class}">{score_emoji} Overall Score: {score}/10<br><small>{score_text}</small></div>',
        unsafe_allow_html=True
    )
    st.subheader("📈 Detailed Metrics")
    matching_score = results.get('matching_score', {})
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        skill_match = matching_score.get('skill_match_percentage', 0)
        st.metric("Skills Match", f"{skill_match:.1f}%", f"{skill_match - 70:.1f}% vs avg" if skill_match > 0 else None)
    with col_m2:
        exp_match = matching_score.get('experience_match', False)
        st.metric("Experience Match", "✅ Yes" if exp_match else "❌ No")
    with col_m3:
        edu_match = matching_score.get('education_match', False)
        st.metric("Education Match", "✅ Yes" if edu_match else "❌ No")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.subheader("💪 Strengths")
        strengths = matching_score.get('strengths', [])
        if strengths:
            for strength in strengths: st.markdown(f"✅ {strength}")
        else: st.info("No specific strengths identified")
    with col_s2:
        st.subheader("🎯 Gaps")
        gaps = matching_score.get('gaps', [])
        if gaps:
            for gap in gaps: st.markdown(f"⚠️ {gap}")
        else: st.success("No major gaps found!")

    if results.get('email_sent'):
        candidate_email = results.get('candidate_email', 'your email')
        st.markdown(
            f'<div class="success-box">📧 <b>Email Notification Sent!</b><br>A congratulatory email has been prepared for {candidate_email}</div>',
            unsafe_allow_html=True
        )
    if score < 8 and results.get('improvement_suggestions'):
        st.divider()
        st.header("💡 Improvement Suggestions")
        suggestions = results.get('improvement_suggestions', {})
        missing_keywords = suggestions.get('missing_keywords', [])
        if missing_keywords:
            st.subheader("🔑 Missing Keywords")
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("Add these keywords to improve ATS matching:")
            for keyword in missing_keywords:
                st.markdown(f"- **{keyword}**")
            st.markdown('</div>', unsafe_allow_html=True)
        skill_suggestions = suggestions.get('skill_suggestions', [])
        if skill_suggestions:
            st.subheader("🛠️ Skills to Highlight/Add")
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            for skill in skill_suggestions:
                st.markdown(f"- {skill}")
            st.markdown('</div>', unsafe_allow_html=True)
        exp_suggestions = suggestions.get('experience_suggestions', '')
        if exp_suggestions:
            st.subheader("📝 Experience Section Tips")
            st.markdown(f'<div class="warning-box">{exp_suggestions}</div>', unsafe_allow_html=True)
        general_tips = suggestions.get('general_tips', [])
        if general_tips:
            st.subheader("✨ General Improvement Tips")
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            for tip in general_tips:
                st.markdown(f"- {tip}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    with st.expander("👤 Parsed Candidate Information"):
        resume_data = results.get('resume_data', {})
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.write("**Name:**", resume_data.get('name', 'Not Found'))
            st.write("**Email:**", resume_data.get('email', 'Not Found'))
            st.write("**Phone:**", resume_data.get('phone', 'Not Found'))
        with col_c2:
            st.write("**Experience:**", resume_data.get('experience', 'Not specified'))
            st.write("**Education:**", resume_data.get('education', 'Not specified'))
        skills = resume_data.get('skills', [])
        if skills: st.write("**Skills:**", ", ".join(skills))
    with st.expander("📋 Parsed Job Requirements"):
        job_req = results.get('job_requirements', {})
        col_j1, col_j2 = st.columns(2)
        with col_j1:
            st.write("**Job Role:**", job_req.get('job_role', 'Not specified'))
            st.write("**Experience Required:**", job_req.get('experience_required', 'Not specified'))
            st.write("**Education Required:**", job_req.get('education_required', 'Not specified'))
        with col_j2:
            required_skills = job_req.get('required_skills', [])
            if required_skills: st.write("**Required Skills:**", ", ".join(required_skills))
            preferred_skills = job_req.get('preferred_skills', [])
            if preferred_skills: st.write("**Preferred Skills:**", ", ".join(preferred_skills))
    st.divider()
    if st.button("🔄 Analyze Another Resume", type="secondary", use_container_width=True):
        st.session_state.results = None
        st.session_state['results'] = st.session_state.get('results')

st.divider()
st.markdown("""
<div style='text-align: center; color: #888; padding: 2rem 0;'>
    <p>Built with ❤️ using LangGraph, Streamlit, and LLaMA-3</p>
    <p>© 2025 AI Resume-Job Matcher | Powered by Advanced NLP</p>
</div>
""", unsafe_allow_html=True)
