
import pandas as pd

def calculate_program_score(job_skills_df, program_skills_df):
    """
    Calculates a score indicating how well a program prepares students based on job market demand.

    Args:
        job_skills_df (pd.DataFrame): Contains skills from job listings with columns ['skill', 'required_optional', 'type']
        program_skills_df (pd.DataFrame): Contains skills taught in the program with columns ['skill', 'required_elective']

    Returns:
        dict: A dictionary with the score, matched skills, and missing skills.
    """
    # Normalize skill names
    job_skills_df['skill'] = job_skills_df['skill'].str.lower()
    program_skills_df['skill'] = program_skills_df['skill'].str.lower()

    # Get top required skills (frequency based)
    top_skills = (
        job_skills_df[job_skills_df['required_optional'].str.lower() == 'required']
        ['skill']
        .value_counts()
        .head(30)
        .index.tolist()
    )

    # Prepare sets for comparison
    program_skills_set = set(program_skills_df['skill'])
    top_skills_set = set(top_skills)

    matched_skills = top_skills_set.intersection(program_skills_set)
    missing_skills = top_skills_set - program_skills_set

    # Score based on required/elective
    score = 0
    for skill in matched_skills:
        skill_type = program_skills_df[program_skills_df['skill'] == skill]['required_elective'].values[0]
        score += 2 if skill_type.lower() == 'required' else 1

    max_score = len(top_skills) * 2
    percentage_score = (score / max_score) * 100

    return {
        'score': round(percentage_score, 2),
        'matched_skills': sorted(list(matched_skills)),
        'missing_skills': sorted(list(missing_skills)),
        'top_skills': top_skills
    }
