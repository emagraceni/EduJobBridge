import streamlit as st
import pandas as pd
from score_calculator import calculate_program_score

st.set_page_config(page_title="Program Skill Scorer", layout="wide")
st.title("🎓 University Program vs Job Market Skill Match")

st.markdown("""
Upload your datasets below to score how well a university program matches job market requirements.
""")

# Upload job market skills file
job_file = st.file_uploader("Upload Job Market Skills CSV", type=["csv"])

# Upload school program skills file
program_file = st.file_uploader("Upload Program Skills CSV (e.g., Columbia, NYIT, Pace)", type=["csv"])

if job_file and program_file:
    job_skills_df = pd.read_csv(job_file)
    program_skills_df = pd.read_csv(program_file)

    if st.button("Calculate Score"):
        result = calculate_program_score(job_skills_df, program_skills_df)

        st.success(f"Program Score: {result['score']}%")

        st.subheader("✅ Skills Covered in Program (from Top Job Skills)")
        st.write(result['matched_skills'])

        st.subheader("❌ Top Job Skills NOT Covered in Program")
        st.write(result['missing_skills'])

        st.subheader("💼 Top Required Job Market Skills")
        st.write(result['top_skills'])
else:
    st.info("Please upload both CSV files to begin.")
