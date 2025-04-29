
import streamlit as st
import pandas as pd
from app.score_calculator import calculate_program_score
from app.skill_cleaner import clean_skills_in_dataframe

# Set page configuration
st.set_page_config(page_title="EduJobBridge", layout="wide")

st.title("🎓 EduJobBridge: University Program Skill Matcher")

st.markdown("""
Select a university program from the list below to evaluate how well it matches current job market skills.
Industry job market data is automatically loaded.
""")

# Predefined program options and corresponding CSV filenames
program_options = {
    "Columbia - Computer Science BS": "data/columbia_cs_bs.csv",
    "Columbia - Software Engineering BS": "data/columbia_software_eng_bs.csv",
    "NYU - Computer Science BS": "data/nyu_cs_bs.csv",
    "Pace - Computer Science BS": "data/pace_cs_bs.csv",
    "Pace - Software Engineering BS": "data/pace_software_eng_bs.csv"
}

# Load Job Market Skills automatically
job_market_skills_path = "data/job_market_skills_data.csv"
job_skills_df = pd.read_csv(job_market_skills_path)
job_skills_df = clean_skills_in_dataframe(job_skills_df, skill_column='Skill')

# Dropdown to select program
selected_program = st.selectbox("🏫 Select a Program", list(program_options.keys()))

# Load selected program CSV
program_file_path = program_options[selected_program]
program_skills_df = pd.read_csv(program_file_path)
program_skills_df = clean_skills_in_dataframe(program_skills_df, skill_column='Skill')

st.success(f"✅ Loaded program: {selected_program}")

with st.expander("🔍 Preview Job Market Skills"):
    st.dataframe(job_skills_df)

with st.expander("🔍 Preview Program Skills"):
    st.dataframe(program_skills_df)

st.markdown("---")
st.subheader("📊 Match Score Evaluation")

if st.button("✨ Calculate Match Score"):
    result = calculate_program_score(job_skills_df, program_skills_df)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.metric(label="📈 Overall Match Score", value=f"{result['score']}%")
        st.metric(label="🛠️ Technical Skills Match", value=f"{result['technical_score']}%")
        st.metric(label="💬 Soft Skills Match", value=f"{result['soft_skill_score']}%")

    with col_right:
        st.success("✅ Skills Covered (from top job market skills)")
        st.write(result['matched_skills'])

        st.warning("❌ Skills Missing (not taught in program)")
        st.write(result['missing_skills'])

    with st.expander("💼 Top Required Job Market Skills"):
        st.write(result['top_skills'])
