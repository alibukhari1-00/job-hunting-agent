# CareerPrep Job-Hunting Agent

An intelligent, menu-driven Python agent that analyzes job postings against your resume,
generates actionable reports, tracks applications, and prepares you for interviews.

---

## Features

- **Job Analysis** — Extracts required skills from job postings
- **Skill Gap Analysis** — Compares job requirements vs your resume skills with a match score
- **Resume Suggestions** — Tailored advice to improve your resume for each role
- **Interview Prep** — Auto-generates role-specific interview questions
- **Application Tracker** — CSV-based tracker with status, dates, and next actions
- **Smart Reminders** — Context-aware reminders based on application status
- **Resume Scoring** — Multi-factor resume score (skills + length + action verbs)
- **Cover Letter Generator** — Personalized cover letters based on matched skills
- **Menu Interface** — Interactive CLI for all features

---

## Project Structure

```
job-hunting-agent/
├── app.py                  # Main application
├── requirements.txt        # Dependencies
├── README.md
├── reflection.md
├── input_jobs/             # Add job posting .txt files here
├── input_resumes/          # Add your resume .txt files here
├── input_kb/               # Add knowledge base .txt files here
├── outputs/                # All generated reports saved here
├── tracker/                # applications.csv saved here
└── samples/                # Sample input files
```

---

## Setup

```bash
# No external dependencies required — uses Python standard library only
python --version   # Requires Python 3.8+
```

---

## How to Run

```bash
cd job-hunting-agent
python app.py
```

You will see an interactive menu:

```
==================================================
  CareerPrep Job-Hunting Agent
==================================================
  1. Run Full Agent Pipeline
  2. Score My Resume
  3. Generate Cover Letter
  4. View Application Tracker
  5. Add Application to Tracker
  6. View Reminders
  0. Exit
==================================================
```

### Quick Start

1. Add job posting `.txt` files to `input_jobs/`
2. Add your resume `.txt` file to `input_resumes/`
3. (Optional) Add tips/notes to `input_kb/`
4. Run `python app.py` and select option `1`

---

## Output Files

All outputs are saved to `outputs/`:

| File | Description |
|------|-------------|
| `job_analysis_report.txt` | Extracted job skills and requirements |
| `skill_gap_report.txt` | Match score, matched and missing skills |
| `tailored_resume_suggestions.txt` | Resume improvement recommendations |
| `interview_questions.txt` | Role-specific interview questions |
| `resume_score_report.txt` | Multi-factor resume score |
| `cover_letter_<Company>.txt` | Generated cover letter |
| `reminders.txt` | Application reminders and follow-ups |
| `final_agent_report.txt` | Consolidated full report |

Application data is saved to `tracker/applications.csv`.

---

## Advanced Features

### 1. Resume Scoring
Scores your resume on three dimensions:
- Skill match with job description (60% weight)
- Resume length/content density (20% weight)
- Action verb usage (20% weight)

### 2. Cover Letter Generator
Generates a personalized cover letter using:
- Your matched skills from the job description
- Company and role name
- Professional template with placeholders for personal info

---

## Requirements

- Python 3.8 or higher
- No external packages needed
