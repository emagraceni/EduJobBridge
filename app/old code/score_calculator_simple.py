def calculate_program_score(job_skills_df, program_skills_df):
    job_skills = set(job_skills_df["Skill"].dropna().str.strip().str.lower())
    program_skills = set(program_skills_df["Skill"].dropna().str.strip().str.lower())

    matched_skills = job_skills & program_skills
    missing_skills = list(job_skills - program_skills)

    # Scoring logic
    score = len(matched_skills) / len(job_skills) if job_skills else 0
    score *= 100

    return {
        "score": round(score, 1),
        "matched_skills": list(matched_skills),
        "missing_skills": missing_skills,
        "top_skills": job_skills_df["Skill"].value_counts().reset_index().head(10).values.tolist()
    }