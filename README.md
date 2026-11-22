# Resume Lens India — AI ATS Analyzer & Career Copilot (Major Project)

Upload a resume (PDF, DOCX, or TXT) to get an in-depth **ATS Audit**, live **Indian Job Matches**, a **Google XYZ Bullet Point Optimizer**, a **Tailored Cover Letter Generator**, and an **Interactive AI Mock Interview Simulator**.

---

## 🚀 Key Highlights & Features

### 1. 📊 In-Depth ATS Diagnostic & Scoring Engine
- **100-Point ATS Scoring**: Evaluates candidate resumes against real-world Indian tech hiring benchmarks.
- **Dimensional Breakdown**: Granular scores for Keywords Match, ATS Formatting, Measurable Impact, and Structure.
- **Actionable Fixes Ranked by Impact**: Clear before/after rewrite suggestions highlighting metrics, active verbs, and standard headings.
- **🖨️ 1-Click Printable ATS Report**: Export clean, executive PDF audit reports directly from your browser.

### 2. 💼 Live Indian Job Matching & Skill Gap Analysis
- Fetches real-time job openings from **Adzuna India** across major tech hubs (Bengaluru, Hyderabad, Pune, Gurugram, Delhi NCR, Mumbai, Remote, etc.).
- **Smart Ranking Algorithm**:
  - 60% Skill overlap with resume
  - 30% Role title relevance
  - 10% Seniority alignment
- **Skill Badges**: Instantly highlights matching competencies (✓) and missing prerequisites (✗).
- **Salary in ₹ LPA**: Displays Indian compensation packages with clean formatting.

### 3. 🎯 (New Unique Feature) JD Match & AI Career Copilot Studio
- **Direct 1-Click Tailor**: Click **"⚡ Tailor & Prep"** on any job card to instantly target that exact opening.
- **Custom JD Support**: Paste any job description directly from LinkedIn, Naukri, or Hirist (with quick demo buttons for Swiggy, Razorpay, Flipkart).
- **Deep Gap Analysis**: Calculates specific role alignment %, matching strengths, and critical missing keywords.
- **✨ ATS Bullet Point Optimizer (Google XYZ Formula)**:
  - Rewrites experience points using Google's formula: *"Accomplished [X] as measured by [Y], by doing [Z]"*.
  - Weaves in missing job keywords naturally with quantifiable metrics.
  - Side-by-side diff comparison with 1-click **"Copy All Optimized Bullets"**.
- **✉️ AI-Tailored Indian Corporate Cover Letter**:
  - Generates a customized, high-converting cover letter referencing company objectives and candidate achievements.
  - 1-click Copy and `.txt` Download.
- **🎤 Interactive AI Mock Interviewer**:
  - Generates 5 curated Technical, System Design, Behavioral, and Resume-Gap questions.
  - Explains *Why Interviewers Ask This* and *Recommended Talking Points*.
  - **Live Practice Mode**: Candidate types (or dictates) their answer and receives instant AI scoring (1–10), constructive strengths, omitted technical points, and an exemplary model answer!

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Python 3.13+, FastAPI, SQLite (cache & persistence), httpx (async HTTP), pdfplumber, python-docx.
- **AI Core**: Google Gemini API (`gemini-3.5-flash-lite` / `gemini-3.1-flash-lite` with automatic fallback routing).
- **Job Data Feeds**: Adzuna India API (with graceful fallback for offline evaluation/demos).
- **Frontend**: Clean Vanilla JavaScript, modern responsive CSS3, semantic HTML5, zero external build toolchain needed.

---

## ⚡ Quick Start

```bash
# 1. Activate Virtual Environment
# Windows:
.venv\Scripts\activate

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Configure API keys in .env
# (Ensure GEMINI_API_KEY is present)

# 4. Start the server
uvicorn app.main:app --reload
```

Open **`http://127.0.0.1:8000`** in your browser.

---

## 🔑 Environment Configuration (`.env`)

| Key | Description | Required |
|---|---|---|
| `GEMINI_API_KEY` | Google AI Studio Key for ATS analysis & AI copilot | Yes |
| `GEMINI_MODEL` | Default model (`gemini-3.5-flash-lite` recommended) | Yes |
| `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` | Developer credentials for developer.adzuna.com | Optional / Live Jobs |
| `RAPIDAPI_KEY` | Optional RapidAPI JSearch integration | Optional |
| `CACHE_TTL_HOURS` | Job results cache TTL (default `12` hours) | Yes |

---

## 🎓 Viva / Demo Presentation Guide

1. **Upload Demo Resume**: Drag & drop `resume.pdf` or `resume.docx`.
2. **Review ATS Audit**: Show the circular score indicator, dimension bars, and actionable impact fixes.
3. **Live Job Match**: Search roles in Bengaluru or Remote; explain how the skill matching highlights exact missing tech tags.
4. **Trigger Tailor Studio**: Click **"⚡ Tailor & Prep"** on a job card (or select a sample JD like *Swiggy SDE-1*).
5. **Showcase Google XYZ Bullets**: Demonstrate how passive bullet points are upgraded into metric-driven accomplishments.
6. **Interactive Mock Interview**: Enter an answer to one of the 5 questions, click **"AI Score & Feedback"**, and demonstrate real-time AI grading!
