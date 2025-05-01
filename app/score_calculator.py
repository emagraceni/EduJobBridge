from app.skill_cleaner import clean_skills_in_dataframe
from app.synonym_mapper import standardize_skill_name
from rapidfuzz import fuzz

def calculate_program_score(job_skills_df, program_skills_df):
    # Clean and normalize
    job_skills_df = clean_skills_in_dataframe(job_skills_df, skill_column='Skill')
    program_skills_df = clean_skills_in_dataframe(program_skills_df, skill_column='Skill')
    job_skills_df['Skill'] = job_skills_df['Skill'].apply(standardize_skill_name)
    program_skills_df['Skill'] = program_skills_df['Skill'].apply(standardize_skill_name)

    total_weight = 0
    matched_weight = 0
    matched_skills = []
    missing_skills = []

    for _, job_row in job_skills_df.iterrows():
        job_skill = job_row['Skill']
        is_required = str(job_row.get("Required", "required")).strip().lower() == "required"
        freq_weight = job_row.get("Frequency", 1)
        weight = freq_weight * (2 if is_required else 1)
        total_weight += weight

        matched = False
        for _, prog_row in program_skills_df.iterrows():
            prog_skill = prog_row['Skill']
            if fuzz.token_sort_ratio(job_skill, prog_skill) >= 85:
                matched_skills.append(job_skill)
                matched_weight += weight
                matched = True
                break

        if not matched:
            missing_skills.append(job_skill)

    score = (matched_weight / total_weight) * 100 if total_weight else 0
    final_score = min(round(score + 15, 1), 100.0)  # normalization and cap

    top_skills = job_skills_df['Skill'].value_counts().reset_index().head(10).values.tolist()

    return {
        "score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "top_skills": top_skills
    }