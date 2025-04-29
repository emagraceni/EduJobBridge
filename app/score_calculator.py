
# score_calculator.py (improved version)

import pandas as pd
from collections import Counter
from scripts.skill_cleaner import clean_skills_in_dataframe

def assign_frequency_weights(skills_series):
    """
    Assign industry frequency weights based on skill appearance frequency.
    Top 20% skills get weight 0.8-1.0, middle 50% get 0.4-0.8, bottom 30% get 0.2-0.4
    """
    skill_counts = skills_series.value_counts()
    total_skills = len(skill_counts)
    ranked_skills = skill_counts.index.tolist()

    weights = {}
    for idx, skill in enumerate(ranked_skills):
        percentile = idx / total_skills
        if percentile <= 0.2:
            weights[skill] = 0.8 + 0.2 * (1 - percentile/0.2)  # 0.8-1.0 range
        elif percentile <= 0.7:
            weights[skill] = 0.4 + 0.4 * (1 - (percentile-0.2)/0.5)  # 0.4-0.8 range
        else:
            weights[skill] = 0.2 + 0.2 * (1 - (percentile-0.7)/0.3)  # 0.2-0.4 range
    return weights

def calculate_program_score(job_skills_df, program_skills_df):
    """
    Calculate the program score based on matching job skills to program skills,
    considering industry frequency, job importance, and program importance.
    """
    # Clean skills
    job_skills_df = clean_skills_in_dataframe(job_skills_df, skill_column='Skill')
    program_skills_df = clean_skills_in_dataframe(program_skills_df, skill_column='Skill')

    # Assign industry frequency weights
    industry_freq_weights = assign_frequency_weights(job_skills_df['Skill'])

    # Prepare program skills
    program_skills = program_skills_df[['Skill', 'required_elective']]
    program_skill_status = {row['Skill']: row['required_elective'] for idx, row in program_skills.iterrows()}

    # Prepare job skills with importance (Required/Optional + Technical/Soft)
    job_skills = job_skills_df[['Skill', 'Required_Optional', 'Technical_Soft']]

    total_possible_points = 0
    earned_points = 0

    matched_skills = []
    missing_skills = []

    technical_skills_total = 0
    technical_skills_matched = 0
    soft_skills_total = 0
    soft_skills_matched = 0

    for idx, row in job_skills.iterrows():
        skill = row['Skill']
        job_importance = row['Required_Optional']
        skill_type = row['Technical_Soft']

        freq_weight = industry_freq_weights.get(skill, 0.5)  # Default if missing
        job_weight = 2 if job_importance.lower() == 'required' else 1

        total_possible_points += freq_weight * job_weight * 2  # Max if program also requires it

        if skill in program_skill_status:
            program_weight = 2 if program_skill_status[skill].lower() == 'required' else 1
            earned_points += freq_weight * job_weight * program_weight
            matched_skills.append(skill)

            # Track technical vs soft match
            if skill_type.lower() == 'technical':
                technical_skills_matched += 1
            else:
                soft_skills_matched += 1
        else:
            missing_skills.append(skill)

        # Track total technical/soft skills
        if skill_type.lower() == 'technical':
            technical_skills_total += 1
        else:
            soft_skills_total += 1

    overall_score = (earned_points / total_possible_points) * 100 if total_possible_points > 0 else 0
    technical_score = (technical_skills_matched / technical_skills_total) * 100 if technical_skills_total > 0 else 0
    soft_skill_score = (soft_skills_matched / soft_skills_total) * 100 if soft_skills_total > 0 else 0

    return {
        'score': round(overall_score, 2),
        'technical_score': round(technical_score, 2),
        'soft_skill_score': round(soft_skill_score, 2),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'top_skills': job_skills_df['Skill'].value_counts().head(10)
    }

