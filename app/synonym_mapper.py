
import pandas as pd

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
    "problem solving": "problem-solving"
}

def map_synonyms(df, column='Skill'):
    df[column] = df[column].astype(str).str.strip().str.lower()
    df[column] = df[column].apply(lambda skill: synonym_dict.get(skill, skill))
    return df
