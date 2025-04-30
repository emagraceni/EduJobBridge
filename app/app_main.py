
# ===== EduJobBridge Main App =====

# --- Add sys.path for easy imports ---
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Main imports ---
import streamlit as st
import pandas as pd
from app.skill_cleaner import clean_skills_in_dataframe
from app.soft_skill_injector import inject_default_soft_skills
from app.synonym_mapper import map_synonyms
from app.score_calculator import calculate_program_score

# --- Page Configuration ---
st.set_page_config(page_title="EduJobBridge", layout="wide")

st.title("🎓 EduJobBridge: University Program Skill Matcher")

st.markdown("""
Select a university program from the list below to evaluate how well it matches current job market skills.
Industry job market data is automatically loaded.
""")

# --- Program Options ---
program_options = {
    "Columbia - Computer Science BS": "data/columbia_cs_bs.csv",
    "Columbia - Software Engineering BS": "data/columbia_software_eng_bs.csv",
    "NYU - Computer Science BS": "data/nyu_cs_bs.csv",
    "Pace - Computer Science BS": "data/pace_cs_bs.csv",
    "Pace - Software Engineering BS": "data/pace_software_eng_bs.csv"
}

# --- Load Job Market Skills Automatically ---
job_market_skills_path = "data/job_market_skills_data.csv"
job_skills_df = pd.read_csv(job_market_skills_path)
job_skills_df = map_synonyms(job_skills_df, column="Skill")
job_skills_df = clean_skills_in_dataframe(job_skills_df, skill_column='Skill')

# --- User Select Program ---
selected_program = st.selectbox("🏫 Select a Program", list(program_options.keys()))

program_file_path = program_options[selected_program]
program_skills_df = pd.read_csv(program_file_path)
# Inject soft skills by default
program_skills_df = inject_default_soft_skills(program_skills_df)
program_skills_df = map_synonyms(program_skills_df, column="Skill")
program_skills_df = clean_skills_in_dataframe(program_skills_df, skill_column='Skill')

# Inject soft skills by default
program_skills_df = inject_default_soft_skills(program_skills_df)

st.success(f"✅ Loaded program: {selected_program}")

# --- Show Dataframes for Transparency ---
with st.expander("🔍 Preview Job Market Skills"):
    st.dataframe(job_skills_df)

with st.expander("🔍 Preview Program Skills (with default soft skills added)"):
    st.dataframe(program_skills_df)

st.markdown("---")
st.subheader("📊 Match Score Evaluation")

# --- Score Calculation ---
if st.button("✨ Calculate Match Score"):
    result = calculate_program_score(job_skills_df, program_skills_df)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.metric(label="📈 Overall Match Score", value=f"{result['score']}%")
        st.metric(label="🛠️ Technical Skills Match", value=f"{result.get('technical_score', '--')}%")
        st.metric(label="💬 Soft Skills Match", value=f"{result.get('soft_skill_score', '--')}%")

    with col_right:
        st.success("✅ Skills Covered (from top job market skills)")
        st.write(result['matched_skills'])

        st.warning("❌ Skills Missing (not taught in program)")
        st.write(result['missing_skills'])

    with st.expander("💼 Top Required Job Market Skills"):
        st.write(result['top_skills'])
