
# 🧠 EduJobBridge

**EduJobBridge** is a data-driven tool that evaluates how well university software engineering programs prepare students for industry-required skills.

It compares course offerings from schools like **Columbia**, **Pace**, and **NYU** against in-demand skills gathered from real job listings on platforms like LinkedIn and Indeed.

---

## 🧩 Project Features

✅ Extracts top technical & soft skills from job descriptions  
✅ Evaluates university programs based on how many of those skills they cover  
✅ Scores each program based on whether skills are taught in **required** or **elective** courses  
✅ Fully interactive **Streamlit dashboard** for uploading data and viewing results

---

## 📂 Folder Structure

```
EduJobBridge/
├── data/                  # CSVs for job market skills + each school's curriculum
├── scripts/               # Streamlit app and scoring logic
├── docs/                  # Literature review and reference material
├── .gitignore
├── requirements.txt       # Python dependencies
└── README.md              # You're here!
```

---

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/emagraceni/EduJobBridge.git
   cd EduJobBridge
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Streamlit app:
   ```bash
   streamlit run scripts/app.py
   ```

4. Use the dashboard to upload:
   - A job market skills CSV (e.g., `job_market_skills_data.csv`)
   - A school program CSV (e.g., `columbia_skills.csv`)

The app will score the program and display:
- Covered skills ✅  
- Missing skills ❌  
- A match score out of 100% 📊

---

## ✍️ Contributing

Want to help add more schools? Improve the UI? Automate scraping? You’re welcome to contribute!

1. Fork the repo
2. Create a new branch
3. Commit and push changes
4. Submit a pull request

---

## 📚 Credits

Created by **@emagraceni** as part of an academic + portfolio project.  

---
