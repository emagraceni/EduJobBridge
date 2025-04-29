
from rapidfuzz import process, fuzz
import pandas as pd

def clean_skills(skill_list, threshold=90):
    """
    Cleans and standardizes a list of skills using fuzzy matching.

    Args:
        skill_list (list): List of skill strings.
        threshold (int): Similarity threshold (0-100) to consider skills as duplicates.

    Returns:
        list: List of cleaned/standardized skills.
    """
    unique_skills = []
    cleaned_skills = []

    for skill in skill_list:
        skill = skill.strip().lower()

        if not unique_skills:
            unique_skills.append(skill)
            cleaned_skills.append(skill)
        else:
            match, score, _ = process.extractOne(skill, unique_skills, scorer=fuzz.token_sort_ratio)
            if score >= threshold:
                cleaned_skills.append(match)
            else:
                unique_skills.append(skill)
                cleaned_skills.append(skill)

    return cleaned_skills

def clean_skills_in_dataframe(df, skill_column='Skill', threshold=90):
    """
    Cleans a dataframe's skill column using fuzzy matching.

    Args:
        df (pd.DataFrame): DataFrame containing skills.
        skill_column (str): Name of the column containing skill names.
        threshold (int): Similarity threshold for merging.

    Returns:
        pd.DataFrame: DataFrame with cleaned skill names.
    """
    skills = df[skill_column].tolist()
    cleaned_skills = clean_skills(skills, threshold)
    df[skill_column] = cleaned_skills
    return df

if __name__ == "__main__":
    data = {'Skill': ['Python', 'python programming', 'Communication skills', 'Strong communication', 'SQL Databases', 'Structured Query Language (SQL)']}
    df = pd.DataFrame(data)
    print("Before cleaning:")
    print(df)

    cleaned_df = clean_skills_in_dataframe(df)
    print("\nAfter cleaning:")
    print(cleaned_df)
