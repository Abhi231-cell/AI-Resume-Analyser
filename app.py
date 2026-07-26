import streamlit as st
import pandas as pd
from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from ats_score import calculate_ats_score
from recommendations import get_recommendations

st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Analyser")
st.write("Upload your resume and a job description to calculate your ATS score and receive AI-based suggestions.")

resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if st.button("Analyse Resume"):

    if resume is None:
        st.error("Please upload your resume.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please enter a job description.")
        st.stop()

    resume_text = extract_resume_text(resume)

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    score, matched, missing = calculate_ats_score(
        resume_skills,
        jd_skills
    )

    st.success("Analysis Complete ✅")

    st.metric("ATS Score", f"{score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matched Skills")
        if matched:
            for skill in matched:
                st.success(skill)
        else:
            st.write("No matching skills found.")

    with col2:
        st.subheader("Missing Skills")
        if missing:
            for skill in missing:
                st.error(skill)
        else:
            st.write("No missing skills.")

    st.subheader("AI Recommendations")

    suggestions = get_recommendations(score, missing)

    for item in suggestions:
        st.write("✔", item)
