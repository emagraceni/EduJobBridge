
synonym_dict = {
    "oop": "object-oriented programming",
    "object oriented programming": "object-oriented programming",
    "js": "javascript",
    "version control": "git",
    "structured query language": "sql",
    "team collaboration": "teamwork",
    "collaboration": "teamwork",
    "debugging skills": "debugging",
    "unit testing": "testing",
    "test automation": "testing",
    "azure devops": "azure",
    "sql server": "sql",
    "communication skills": "communication",
    "problem solving": "problem-solving",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "sql programming": "sql",
    "python programming": "python",
    "csharp": "c#",
    "c++ programming": "c++",
    "git version control": "git"
}

def standardize_skill_name(skill):
    if not isinstance(skill, str):
        return skill
    return synonym_dict.get(skill.strip().lower(), skill.strip().lower())

import pandas as pd

def map_synonyms(df, column='Skill'):
    df[column] = df[column].astype(str).str.strip().str.lower()
    df[column] = df[column].apply(standardize_skill_name)
    return df
