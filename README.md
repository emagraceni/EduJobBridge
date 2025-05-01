# EduJobBridge 🎓💼

EduJobBridge is a data-driven platform that analyzes how well university programs prepare students for the job market based on skill alignment. It compares course offerings from academic programs against required skills in real-world job postings and calculates a match score using weighted, normalized logic.

---

## 🚀 Features

- 🔍 **Skill Matching**: Compares program skills with job market demands.
- 🧠 **Scoring Logic**: Uses fuzzy matching, synonym mapping, and skill frequency weights.
- 📊 **Interactive Dashboard**: Built with Streamlit, lets users select and score programs.
- 🧼 **Data Cleaning Pipeline**: Standardizes and maps skills for fair comparison.
- 💡 **Visual Results**: Displays matched, missing, and top job skills side-by-side.

---

## ⚙️ How It Works

1. **Extract Skills**
   - Job postings (e.g. from LinkedIn/Indeed): skill + required/optional + frequency
   - University programs: skill + required/elective

2. **Clean & Normalize**
   - Synonym mapping (`"js"` → `"javascript"`)
   - Fuzzy matching using `rapidfuzz`
   - Lowercasing, trimming, injection of default soft skills

3. **Scoring Formula**
   - Each job skill is weighted by:
     ```
     frequency × (2 if required else 1)
     ```
   - Program skill matches are scored based on importance and role
   - Final score:
     ```
     (matched_weight / total_weight) × 100 + 15 (base score), capped at 100
     ```

---

## 📂 Directory Structure

```
EduJobBridge/
│
├── app/
│   ├── app_main.py              # Streamlit front-end
│   ├── score_calculator.py      # Scoring logic
│   ├── skill_cleaner.py         # Preprocessing logic
│   ├── synonym_mapper.py        # Synonym normalization
│   └── soft_skill_injector.py   # Soft skill injection
│
├── data/
│   ├── job_market_skills_data.csv
│   ├── columbia_cs_bs.csv
│   ├── pace_software_eng_bs.csv
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## 💻 Run Locally

```bash
git clone https://github.com/emagraceni/EduJobBridge.git
cd EduJobBridge
pip install -r requirements.txt
streamlit run app/app_main.py
```

---

## 🌐 Deploy on Streamlit Cloud

1. Push your repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Choose:
   - Repo: `emagraceni/EduJobBridge`
   - App file: `app/app_main.py`
4. Click **Deploy**

---

## 📈 Future Improvements

- Automated scraping of program and job skills
- NLP classification for course descriptions
- Role-specific filters (e.g., "Data Analyst" vs "ML Engineer")
- Public platform with user login and dashboards

---

## 👩‍💻 Built With

- 🐍 Python
- 🧠 Pandas, RapidFuzz
- 🌐 Streamlit
- 💡 Manual data extraction + skill injection

---

## 📬 Contact

Feel free to connect or contribute!