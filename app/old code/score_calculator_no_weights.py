from app.skill_cleaner import clean_skills_in_dataframe
from app.synonym_mapper import standardize_skill_name
from rapidfuzz import fuzz

def calculate_program_score(job_skills_df, program_skills_df):
    # Clean and map synonyms
    job_skills_df = clean_skills_in_dataframe(job_skills_df, skill_column='Skill')
    job_skills_df['Skill'] = job_skills_df['Skill'].apply(standardize_skill_name)
    job_skills = job_skills_df['Skill'].dropna().tolist()

    program_skills_df = clean_skills_in_dataframe(program_skills_df, skill_column='Skill')
    program_skills_df['Skill'] = program_skills_df['Skill'].apply(standardize_skill_name)

    total_weight = 0
    matched_weight = 0
    matched_skills = []
    missing_skills = []

    for job_skill in job_skills:
        found_match = False
        for _, row in program_skills_df.iterrows():
            prog_skill = row['Skill']
            required_status = str(row.get('Required_Elective') or row.get('Required') or '').strip().lower()
            is_required = required_status == 'required'
            weight = 2 if is_required else 1

            # Fuzzy match threshold
            if fuzz.token_sort_ratio(job_skill, prog_skill) >= 85:
                matched_weight += weight
                matched_skills.append(job_skill)
                found_match = True
                break

        # Each job skill counts as 2 (important) by default
        total_weight += 2
        if not found_match:
            missing_skills.append(job_skill)

    score = (matched_weight / total_weight) * 100 if total_weight else 0
    final_score = min(round(score + 15, 1), 100.0)  # Add base score, cap at 100

    top_skills = job_skills_df['Skill'].value_counts().reset_index().head(10).values.tolist()

    return {
        'score': final_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'top_skills': top_skills
    }