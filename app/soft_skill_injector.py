import pandas as pd
def inject_default_soft_skills(program_df):
    default_soft_skills = [
        {"Skill": "Communication", "Type": "Soft", "Required": "Required"},
        {"Skill": "Teamwork", "Type": "Soft", "Required": "Required"},
        {"Skill": "Problem Solving", "Type": "Soft", "Required": "Required"},
        {"Skill": "Time Management", "Type": "Soft", "Required": "Optional"},
        {"Skill": "Presentation", "Type": "Soft", "Required": "Optional"},
        {"Skill": "Collaboration", "Type": "Soft", "Required": "Required"},
    ]

    soft_skills_df = pd.DataFrame(default_soft_skills)

    # Ensure column consistency
    for col in ["Skill", "Type", "Required"]:
        if col not in program_df.columns:
            program_df[col] = ""

    # Combine and remove potential duplicates by skill name
    combined = pd.concat([program_df, soft_skills_df], ignore_index=True)
    combined = combined.drop_duplicates(subset="Skill", keep="first").reset_index(drop=True)

    return combined
