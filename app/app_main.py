
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px

from app.score_calculator import calculate_program_score
from app.skill_cleaner import clean_skills_in_dataframe
from app.soft_skill_injector import inject_default_soft_skills
from app.synonym_mapper import map_synonyms

st.set_page_config(page_title="EduJobBridge", layout="wide")

st.markdown("""
    <h1 style='text-align: center;'>🌐 EduJobBridge: Industry vs. Academia Skills Match</h1>
""", unsafe_allow_html=True)

# ✅ Load and clean job market data
job_skills_df = pd.read_csv("data/job_market_skills_data.csv")
job_skills_df = map_synonyms(job_skills_df, column="Skill")
job_skills_df = clean_skills_in_dataframe(job_skills_df, skill_column="Skill")

# File selector
program_file = st.selectbox("🎓 Select a Program", [
    "columbia_cs_bs.csv",
    "columbia_software_eng_bs.csv",
    "nyu_cs_bs.csv",
    "pace_cs_bs.csv",
    "pace_software_eng_bs.csv"
])

# ✅ Load and clean program data
program_skills_df = pd.read_csv(f"data/{program_file}")
program_skills_df = map_synonyms(program_skills_df, column="Skill")
program_skills_df = inject_default_soft_skills(program_skills_df)
program_skills_df = clean_skills_in_dataframe(program_skills_df)

# Layout
st.divider()
col1, col2 = st.columns(2)

with col1:
    with st.expander("📘 View Program Skills", expanded=True):
        st.dataframe(program_skills_df, use_container_width=True)

with col2:
    with st.expander("🏅 Top Job Market Skills Used", expanded=True):
        freq_df = job_skills_df["Skill"].value_counts().reset_index()
        freq_df.columns = ["Skill", "Frequency"]
        st.dataframe(freq_df.head(10), use_container_width=True)

# Score comparison
st.divider()
if st.button("📊 Calculate Match Score"):
    result = calculate_program_score(job_skills_df, program_skills_df)
    st.success(f"🔢 Match Score: {result['score']:.1f}%")
    with st.expander("✅ Matched Skills"):
        st.dataframe(pd.DataFrame(result['matched_skills']), use_container_width=True)

    with st.expander("❌ Missing Top Job Market Skills"):
        st.dataframe(pd.DataFrame(result['missing_skills']), use_container_width=True)

    with st.expander("💼 Top Required Job Market Skills"):
        st.dataframe(pd.DataFrame(result['top_skills']), use_container_width=True)
