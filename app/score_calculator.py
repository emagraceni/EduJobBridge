
from app.skill_cleaner import clean_skills_in_dataframe
from collections import Counter

def calculate_program_score(job_df, program_df):
    # Count job skill frequency
    job_df['Skill'] = job_df['Skill'].str.strip()
    skill_counts = Counter(job_df['Skill'])

    # Weight job skills by frequency
    job_df['Weight'] = job_df['Skill'].map(lambda s: skill_counts[s] / len(job_df))

    # Filter top N job market skills
    top_skills = job_df.sort_values(by='Weight', ascending=False).drop_duplicates(subset='Skill').head(50)

    # Match skills between program and job market
    matched_skills = []
    missing_skills = []

    for _, row in top_skills.iterrows():
        skill = row['Skill']
        matched = program_df[program_df['Skill'].str.lower() == skill.lower()]
        if not matched.empty:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Ensure 'Required' column exists
    if 'Required' not in program_df.columns:
        program_df['Required'] = 'Required'

    # Calculate score
    total_score = 0
    max_possible_score = 0

    for _, row in top_skills.iterrows():
        skill = row['Skill']
        weight = row['Weight']
        max_possible_score += weight * 2  # 2 if required, 1 if optional

        match_row = program_df[program_df['Skill'].str.lower() == skill.lower()]
        if not match_row.empty:
            required_val = match_row.iloc[0].get('Required', 'Required').strip().lower()
            if required_val == 'required':
                total_score += weight * 2
            else:
                total_score += weight * 1

    raw_score = (total_score / max_possible_score) * 100 if max_possible_score > 0 else 0

    # Apply normalization
    base_score = 15
    scaling_factor = 1.25
    adjusted_score = base_score + raw_score * scaling_factor
    adjusted_score = min(round(adjusted_score, 2), 100.0)

    return {
        "score": adjusted_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "top_skills": top_skills[['Skill', 'Weight']].reset_index(drop=True)
    }
