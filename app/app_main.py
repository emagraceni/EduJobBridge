
import streamlit as st
import pandas as pd
from score_calculator import calculate_program_score

st.set_page_config(page_title="🎓 EduJobBridge", layout="wide")

st.title("🧠 EduJobBridge: Program Skill Match Dashboard")
st.markdown("""
This tool evaluates how well a university program prepares students for software engineering jobs based on current job market skills.
Upload a job market skills file and a program curriculum file to get started.
""")

# Layout: Split into two columns for file upload
col1, col2 = st.columns(2)

with col1:
    job_file = st.file_uploader("📂 Upload Job Market Skills CSV", type=["csv"])
    if job_file:
        job_skills_df = pd.read_csv(job_file)
        st.success("✅ Job skills file uploaded!")
        with st.expander("🔍 Preview Job Market Skills"):
            st.dataframe(job_skills_df)

with col2:
    program_file = st.file_uploader("📂 Upload Program Curriculum CSV", type=["csv"])
    if program_file:
        program_skills_df = pd.read_csv(program_file)
        st.success("✅ Program skills file uploaded!")
        with st.expander("🔍 Preview Program Curriculum Skills"):
            st.dataframe(program_skills_df)

# Calculate Score
if job_file and program_file:
    st.markdown("""---""")
    st.subheader("📊 Match Score Evaluation")

    if st.button("✨ Calculate Match Score"):
        result = calculate_program_score(job_skills_df, program_skills_df)

        col_left, col_right = st.columns([1, 2])
        with col_left:
            st.metric(label="📈 Match Score", value=f"{result['score']}%")

        with col_right:
            st.success("✅ Skills Covered (from top job market skills)")
            st.write(result["matched_skills"])

            st.warning("❌ Missing Skills (not taught in program)")
            st.write(result["missing_skills"])

        with st.expander("💼 Top Required Job Market Skills"):
            st.write(result["top_skills"])
else:
    st.info("👆 Upload both files above to enable score calculation.")
