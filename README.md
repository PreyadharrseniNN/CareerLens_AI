# CareerLens AI 🚀
**Intelligent Resume Analyzer & Career Recommendation System**

CareerLens AI is a Flask-based web application that parses resumes in PDF and DOCX formats, extracts technical skills and personality traits using intelligent boundary-aware text matching, identifies obsolete/legacy technologies and suggests modern alternatives, computes a multi-factor career readiness score, and provides personalized job recommendations and step-by-step career roadmaps.

---

## 🌟 Key Features

1. **Multi-Format Resume Parsing**: Seamless text extraction from `.pdf` and `.docx` files (including tables and formatted sections).
2. **Intelligent Skill Extraction**: High-precision boundary matching prevents false positives (e.g., distinguishing `Java` from `JavaScript`).
3. **Skill Obsolescence Watchdog**: Detects legacy technologies (e.g., `jQuery`, `Hadoop`, `SVN`, `Visual Basic`) and recommends current industry successors (`React`, `Spark`, `Git`, `Python`).
4. **Soft Trait & Personality Analysis**: Identifies professional traits like `Leadership`, `Problem Solving`, and `Team Player` from contextual keywords.
5. **Multi-Factor Scoring**: Generates an interpretable 0–100 career readiness score with detailed breakdown.
6. **Role Matching & Fit Analytics**: Recommends top job matches with match percentages, visualized via interactive Chart.js charts.
7. **Actionable Career Roadmaps**: Generates structured 3-month, 6-month, and 1-year skill acquisition milestones based on missing skills.

---

## 📁 Project Structure

```
CareerLens AI/
├── app.py                      # Flask web application and routing
├── generate_sample.py          # Helper script to generate a sample DOCX resume
├── requirements.txt            # Python dependencies
├── core/
│   ├── __init__.py
│   ├── analyzer.py             # Skill extraction, obsolescence detection & scoring
│   ├── parser.py               # PDF and DOCX file text extraction
│   └── recommender.py          # Job role recommendation & roadmap generator
├── data/
│   ├── job_roles.json          # Target roles and required skill sets
│   ├── obsolete_skills.json    # Obsolete tools mapped to modern alternatives
│   ├── personality_traits.json # Soft trait keyword indicators
│   └── skills.json             # Comprehensive technical skill database
├── static/
│   └── css/
│       └── style.css           # Glassmorphism UI styling and animations
└── templates/
    ├── index.html              # Drag-and-drop resume upload portal
    └── result.html             # Analysis dashboard and visualizations
```

---

## ⚡ Quickstart

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Generate Sample Resume (Optional)
```bash
python generate_sample.py
```
This generates `sample_resume.docx` in the root folder for testing.

### 3. Run the Application
```bash
python app.py
```
Navigate to `http://127.0.0.1:5000` in your web browser.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.11, Flask, Jinja2, Werkzeug
- **Document Processing**: python-docx, PyPDF2
- **Frontend**: HTML5, CSS3 (Glassmorphism), Bootstrap 5, FontAwesome, Chart.js
