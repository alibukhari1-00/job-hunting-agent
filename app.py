import os
import csv
import re
import json
import logging
from datetime import datetime, timedelta

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

JOB_DIR    = "input_jobs"
RESUME_DIR = "input_resumes"
KB_DIR     = "input_kb"
OUTPUT_DIR = "outputs"
TRACKER_DIR = "tracker"

KEYWORDS = [
    "python", "machine learning", "data preprocessing", "github", "git",
    "api", "prompt engineering", "sql", "communication", "problem solving",
    "oop", "database", "jupyter", "pandas", "numpy", "deep learning",
    "html", "css", "flask", "streamlit", "resume", "interview",
    "tensorflow", "pytorch", "scikit-learn", "nlp", "computer vision",
    "docker", "kubernetes", "aws", "azure", "gcp", "rest api", "graphql",
    "agile", "scrum", "ci/cd", "unit testing", "data analysis",
    "visualization", "tableau", "power bi", "excel", "statistics",
    "linear algebra", "probability", "java", "c++", "javascript",
    "react", "node.js", "mongodb", "postgresql", "redis", "spark",
    "hadoop", "airflow", "mlops", "feature engineering", "time series",
    "leadership", "teamwork", "critical thinking", "project management"
]

TRACKER_FILE = os.path.join(TRACKER_DIR, "applications.csv")
TRACKER_FIELDS = [
    "application_id", "company", "role", "source", "status",
    "applied_date", "interview_date", "follow_up_date", "next_action", "notes"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

# ─── CHECKPOINT 1 & 2 — FOLDER SETUP ─────────────────────────────────────────

def ensure_folders():
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR]:
        os.makedirs(folder, exist_ok=True)
        log.info(f"Folder ready: {folder}")

# ─── CHECKPOINT 3 — FILE READING ──────────────────────────────────────────────

def read_text_files(folder):
    combined_text = ""
    file_count = 0
    if not os.path.exists(folder):
        log.warning(f"Folder not found: {folder}")
        return combined_text, file_count

    files = [f for f in os.listdir(folder) if f.lower().endswith(".txt")]
    if not files:
        log.warning(f"No .txt files found in: {folder}")
        return combined_text, file_count

    for filename in files:
        path = os.path.join(folder, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                combined_text += f"\n\n--- FILE: {filename} ---\n{content}"
                file_count += 1
                log.info(f"Read file: {filename} ({len(content)} chars)")
        except Exception as e:
            log.error(f"Failed to read {filename}: {e}")

    return combined_text, file_count

def save_text(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    log.info(f"Saved: {path}")

# ─── CHECKPOINT 4 — ANALYSIS ──────────────────────────────────────────────────

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s/+#.]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def extract_keywords(text):
    normalized = normalize(text)
    found = [kw for kw in KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', normalized)]
    return list(set(found))

def compare_skills(job_skills, resume_skills):
    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]
    score = 0 if not job_skills else round((len(matched) / len(job_skills)) * 100, 2)
    return matched, missing, score

# ─── CHECKPOINT 5 — REPORT GENERATORS ────────────────────────────────────────

def generate_job_analysis_report(job_text, job_skills):
    lines = [
        "=" * 60,
        "JOB ANALYSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "EXTRACTED JOB REQUIREMENTS:",
        "-" * 40,
    ]
    if job_skills:
        for i, skill in enumerate(sorted(job_skills), 1):
            lines.append(f"  {i:2}. {skill}")
    else:
        lines.append("  No specific skills detected.")
    lines += ["", f"Total skills identified: {len(job_skills)}", ""]
    lines += [
        "RAW JOB CONTENT PREVIEW:",
        "-" * 40,
        job_text[:800].strip() + ("..." if len(job_text) > 800 else ""),
        ""
    ]
    return "\n".join(lines)

def generate_skill_gap_report(matched, missing, score):
    lines = [
        "=" * 60,
        "SKILL GAP ANALYSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        f"MATCH SCORE: {score}%",
        "",
        f"MATCHED SKILLS ({len(matched)}):",
        "-" * 40,
    ]
    for s in sorted(matched):
        lines.append(f"  ✔ {s}")
    lines += ["", f"MISSING SKILLS ({len(missing)}):", "-" * 40]
    for s in sorted(missing):
        lines.append(f"  ✘ {s}")
    lines += [""]
    if score >= 80:
        lines.append("Assessment: STRONG match — apply with confidence.")
    elif score >= 50:
        lines.append("Assessment: MODERATE match — address skill gaps before applying.")
    else:
        lines.append("Assessment: WEAK match — significant upskilling recommended.")
    lines.append("")
    return "\n".join(lines)

def generate_resume_suggestions(missing, kb_text):
    lines = [
        "=" * 60,
        "TAILORED RESUME SUGGESTIONS",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "SKILLS TO ADD / HIGHLIGHT:",
        "-" * 40,
    ]
    if missing:
        for skill in sorted(missing):
            lines.append(f"  • Add evidence of: {skill}")
    else:
        lines.append("  Your resume already covers all detected job skills!")
    lines += [
        "",
        "GENERAL RESUME TIPS:",
        "-" * 40,
        "  • Quantify achievements (e.g., 'Improved accuracy by 15%')",
        "  • Use action verbs: built, designed, optimized, deployed",
        "  • Keep to 1–2 pages; tailor for each application",
        "  • Include GitHub/portfolio links",
        "  • List relevant certifications and courses",
        "",
    ]
    if kb_text:
        lines += [
            "KNOWLEDGE BASE INSIGHTS:",
            "-" * 40,
            kb_text[:500].strip() + ("..." if len(kb_text) > 500 else ""),
            ""
        ]
    return "\n".join(lines)

def generate_interview_questions(job_skills, matched):
    question_bank = {
        "python":            "Explain Python's GIL and when it matters.",
        "machine learning":  "Walk through your end-to-end ML project workflow.",
        "sql":               "Write a query to find the second-highest salary.",
        "api":               "How do you design a RESTful API? Describe versioning.",
        "git":               "Explain Git branching strategy for a team project.",
        "github":            "How do you handle pull request reviews?",
        "docker":            "What is the difference between an image and a container?",
        "aws":               "Describe a cloud architecture you have designed.",
        "deep learning":     "Compare CNNs and RNNs — when do you use each?",
        "pandas":            "How do you handle missing data in a DataFrame?",
        "numpy":             "Explain broadcasting in NumPy with an example.",
        "flask":             "How do you secure a Flask REST API?",
        "streamlit":         "How did you deploy a Streamlit app?",
        "nlp":               "Explain tokenization and its importance in NLP.",
        "communication":     "Describe a time you explained a technical concept to a non-technical stakeholder.",
        "problem solving":   "Walk me through how you debug a production issue.",
        "leadership":        "Tell me about a time you led a team under pressure.",
        "agile":             "How do you manage sprint planning and retrospectives?",
        "statistics":        "Explain p-value and confidence intervals.",
        "data analysis":     "Describe your data cleaning process for a messy dataset.",
    }
    lines = [
        "=" * 60,
        "INTERVIEW PREPARATION QUESTIONS",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "ROLE-SPECIFIC QUESTIONS (based on job requirements):",
        "-" * 40,
    ]
    asked = set()
    for skill in sorted(job_skills):
        if skill in question_bank and skill not in asked:
            lines.append(f"\n  [{skill.upper()}]")
            lines.append(f"  Q: {question_bank[skill]}")
            asked.add(skill)
    if not asked:
        lines.append("  No specific questions mapped — review job description manually.")
    lines += [
        "",
        "GENERAL INTERVIEW QUESTIONS:",
        "-" * 40,
        "  Q: Tell me about yourself.",
        "  Q: Why do you want this role?",
        "  Q: What is your greatest professional achievement?",
        "  Q: Where do you see yourself in 5 years?",
        "  Q: Do you have any questions for us?",
        ""
    ]
    return "\n".join(lines)

# ─── CHECKPOINT 6 — TRACKER ───────────────────────────────────────────────────

def init_tracker():
    if not os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=TRACKER_FIELDS).writeheader()
        log.info("Tracker CSV created.")

def load_tracker():
    rows = []
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    return rows

def save_tracker(rows):
    with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def add_application(company, role, source="job board", status="Not Applied", notes=""):
    rows = load_tracker()
    app_id = f"APP{len(rows) + 1:03d}"
    today = datetime.now().strftime("%Y-%m-%d")
    follow_up = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    rows.append({
        "application_id": app_id,
        "company":        company,
        "role":           role,
        "source":         source,
        "status":         status,
        "applied_date":   today if status != "Not Applied" else "",
        "interview_date": "",
        "follow_up_date": follow_up,
        "next_action":    "Apply" if status == "Not Applied" else "Follow up",
        "notes":          notes
    })
    save_tracker(rows)
    log.info(f"Tracker updated: {app_id} — {company} / {role}")
    return app_id

# ─── CHECKPOINT 7 — REMINDERS ─────────────────────────────────────────────────

def generate_reminders(rows):
    today = datetime.now().date()
    lines = [
        "=" * 60,
        "APPLICATION REMINDERS",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        ""
    ]
    if not rows:
        lines.append("No applications tracked yet.")
        lines.append("")
        return "\n".join(lines)

    for row in rows:
        app_id  = row.get("application_id", "N/A")
        company = row.get("company", "Unknown")
        role    = row.get("role", "Unknown")
        status  = row.get("status", "").strip().lower()
        int_date_str = row.get("interview_date", "").strip()
        fup_date_str = row.get("follow_up_date", "").strip()

        lines.append(f"[{app_id}] {company} — {role}")

        if status == "interview scheduled" and int_date_str:
            try:
                int_date = datetime.strptime(int_date_str, "%Y-%m-%d").date()
                days_left = (int_date - today).days
                if days_left >= 0:
                    lines.append(f"  ⚡ INTERVIEW in {days_left} day(s) on {int_date_str} — Prepare now!")
                else:
                    lines.append(f"  ✔ Interview was on {int_date_str} — Send thank-you note if not done.")
            except ValueError:
                lines.append(f"  ⚡ Interview scheduled — check date format.")
        elif status == "not applied":
            lines.append(f"  📋 ACTION: Submit application ASAP.")
        elif status == "applied":
            if fup_date_str:
                try:
                    fup_date = datetime.strptime(fup_date_str, "%Y-%m-%d").date()
                    days_left = (fup_date - today).days
                    if days_left <= 0:
                        lines.append(f"  🔔 FOLLOW-UP overdue since {fup_date_str} — reach out today!")
                    else:
                        lines.append(f"  🔔 Follow-up due in {days_left} day(s) on {fup_date_str}.")
                except ValueError:
                    lines.append(f"  🔔 Follow up when possible.")
            else:
                lines.append(f"  🔔 Follow up within 7 days of applying.")
        elif status == "offer received":
            lines.append(f"  🎉 OFFER received — evaluate and respond promptly!")
        elif status == "rejected":
            lines.append(f"  ℹ️  Rejected — request feedback and move on.")
        else:
            lines.append(f"  ℹ️  Status: {row.get('status', 'Unknown')} — review next action.")

        lines.append("")
    return "\n".join(lines)

# ─── CHECKPOINT 8 — MAIN PIPELINE ─────────────────────────────────────────────

def select_file(folder, label):
    """Let user pick a specific file from a folder, or use all."""
    if not os.path.exists(folder):
        return None
    files = [f for f in os.listdir(folder) if f.lower().endswith(".txt")]
    if not files:
        return None
    print(f"\n  Available {label} files:")
    for i, f in enumerate(files, 1):
        print(f"    {i}. {f}")
    print(f"    0. Use ALL files")
    choice = input(f"  Select {label} file (0 for all): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        return os.path.join(folder, files[int(choice) - 1])
    return None  # None means use all

def read_single_file(path):
    """Read a single file and return its text."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        log.info(f"Read file: {os.path.basename(path)} ({len(content)} chars)")
        return content, 1
    except Exception as e:
        log.error(f"Failed to read {path}: {e}")
        return "", 0

def run_agent(job_file=None, resume_file=None):
    log.info("=" * 50)
    log.info("CareerPrep Job-Hunting Agent — Starting")
    log.info("=" * 50)

    ensure_folders()
    init_tracker()

    # Step 1 — Read files (specific or all)
    if job_file:
        job_text, job_count = read_single_file(job_file)
    else:
        job_text, job_count = read_text_files(JOB_DIR)

    if resume_file:
        resume_text, resume_count = read_single_file(resume_file)
    else:
        resume_text, resume_count = read_text_files(RESUME_DIR)

    kb_text, kb_count = read_text_files(KB_DIR)
    log.info(f"Files read — Jobs: {job_count}, Resumes: {resume_count}, KB: {kb_count}")

    # Step 2 — Extract skills
    job_skills    = extract_keywords(job_text)    if job_text    else []
    resume_skills = extract_keywords(resume_text) if resume_text else []
    log.info(f"Skills extracted — Job: {len(job_skills)}, Resume: {len(resume_skills)}")

    # Step 3 — Compare
    matched, missing, score = compare_skills(job_skills, resume_skills)
    log.info(f"Match score: {score}% | Matched: {len(matched)} | Missing: {len(missing)}")

    # Step 4 — Generate core reports
    job_report       = generate_job_analysis_report(job_text, job_skills)
    gap_report       = generate_skill_gap_report(matched, missing, score)
    resume_report    = generate_resume_suggestions(missing, kb_text)
    interview_report = generate_interview_questions(job_skills, matched)

    # Step 5 — Update tracker (demo entry if empty)
    rows = load_tracker()
    if not rows:
        add_application("Demo Corp", "AI Engineer", "LinkedIn", "Not Applied", "Auto-added by agent")
        add_application("Tech Startup", "ML Engineer", "Indeed", "Applied", "Submitted portfolio")
        add_application("Big Tech Co", "Data Scientist", "Referral", "Interview Scheduled", "Interview 2025-08-01")
        rows = load_tracker()
        for r in rows:
            if r["company"] == "Big Tech Co":
                r["interview_date"] = "2025-08-01"
                r["status"] = "Interview Scheduled"
        save_tracker(rows)
        rows = load_tracker()

    # Step 6 — Generate reminders (with urgency)
    reminders = generate_reminders_with_urgency(rows)

    # Step 7 — Generate new advanced reports
    project_map      = generate_project_mapping(resume_text, job_skills)
    interview_ans    = generate_interview_answers(job_skills, kb_text)
    checklist        = generate_preparation_checklist(job_skills, matched, missing, resume_text)
    linkedin_msg     = generate_linkedin_message("[Company]", "[Role]", resume_text)
    memory           = save_memory(job_skills, resume_skills, matched, missing, score)

    # Step 8 — Save core outputs
    save_text(os.path.join(OUTPUT_DIR, "job_analysis_report.txt"),         job_report)
    save_text(os.path.join(OUTPUT_DIR, "skill_gap_report.txt"),            gap_report)
    save_text(os.path.join(OUTPUT_DIR, "tailored_resume_suggestions.txt"), resume_report)
    save_text(os.path.join(OUTPUT_DIR, "interview_questions.txt"),         interview_report)

    # Final consolidated report
    final = "\n\n".join([
        job_report, gap_report, resume_report, interview_report,
        project_map, interview_ans, checklist, reminders
    ])
    save_text(os.path.join(OUTPUT_DIR, "final_agent_report.txt"), final)

    log.info("All reports saved to outputs/")
    log.info("Agent run complete.")
    return score, matched, missing

# ─── CHECKPOINT 12 — ADVANCED FEATURES ───────────────────────────────────────

# Advanced Feature 1: Resume Scoring
def score_resume(resume_text, job_text):
    job_skills    = extract_keywords(job_text)
    resume_skills = extract_keywords(resume_text)
    matched, missing, score = compare_skills(job_skills, resume_skills)

    word_count = len(resume_text.split())
    length_score = min(100, (word_count / 400) * 100)

    action_verbs = ["built", "designed", "developed", "optimized", "deployed",
                    "led", "managed", "created", "improved", "implemented"]
    verb_hits = sum(1 for v in action_verbs if v in resume_text.lower())
    verb_score = min(100, verb_hits * 10)

    final_score = round((score * 0.6) + (length_score * 0.2) + (verb_score * 0.2), 2)

    lines = [
        "=" * 60,
        "RESUME SCORING REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        f"  Skill Match Score  : {score}%",
        f"  Resume Length Score: {round(length_score, 2)}% (word count: {word_count})",
        f"  Action Verb Score  : {verb_score}% ({verb_hits} verbs found)",
        f"  FINAL RESUME SCORE : {final_score} / 100",
        "",
        "  Grade: " + (
            "A — Excellent" if final_score >= 80 else
            "B — Good"      if final_score >= 60 else
            "C — Average"   if final_score >= 40 else
            "D — Needs Work"
        ),
        ""
    ]
    report = "\n".join(lines)
    save_text(os.path.join(OUTPUT_DIR, "resume_score_report.txt"), report)
    log.info(f"Resume score: {final_score}/100")
    return final_score, report

# Advanced Feature 2: Cover Letter Generator
def generate_cover_letter(company, role, resume_text, job_text):
    matched, _, _ = compare_skills(
        extract_keywords(job_text),
        extract_keywords(resume_text)
    )
    top_skills = ", ".join(sorted(matched)[:5]) if matched else "relevant technical skills"
    today = datetime.now().strftime("%B %d, %Y")

    letter = f"""
{today}

Hiring Manager
{company}

Dear Hiring Manager,

I am writing to express my strong interest in the {role} position at {company}.
With a solid foundation in {top_skills}, I am confident in my ability to
contribute meaningfully to your team from day one.

Throughout my academic and project experience, I have developed hands-on
expertise in the core technologies your role demands. I thrive in collaborative
environments, enjoy solving complex problems, and am committed to continuous
learning — values I understand are central to {company}'s culture.

I would welcome the opportunity to discuss how my background aligns with your
team's goals. Thank you for your time and consideration.

Sincerely,
[Your Name]
[Your Email] | [Your Phone] | [Your LinkedIn]
""".strip()

    path = os.path.join(OUTPUT_DIR, f"cover_letter_{company.replace(' ', '_')}.txt")
    save_text(path, letter)
    log.info(f"Cover letter generated for {company} — {role}")
    return letter

# ─── NEW ADVANCED FEATURES ────────────────────────────────────────────────────

# Feature 2: Project-to-Job Mapping
def extract_projects(resume_text):
    """Extract project names and descriptions from resume."""
    projects = []
    lines = resume_text.split('\n')
    in_project_section = False
    current_project = None
    
    for line in lines:
        line_lower = line.lower().strip()
        if 'project' in line_lower and (':' in line or len(line_lower) < 50):
            in_project_section = True
        
        # Detect numbered project entries like "1. Project Name"
        if in_project_section and re.match(r'^\d+\.\s+(.+)', line.strip()):
            match = re.match(r'^\d+\.\s+(.+)', line.strip())
            if current_project:
                projects.append(current_project)
            current_project = {'name': match.group(1).strip(), 'description': ''}
        elif current_project and line.strip().startswith('-'):
            current_project['description'] += ' ' + line.strip()[1:].strip()
    
    if current_project:
        projects.append(current_project)
    
    return projects

def map_projects_to_skills(projects, job_skills):
    """Map each project to job skills it demonstrates."""
    mapping = []
    for proj in projects:
        proj_text = (proj['name'] + ' ' + proj['description']).lower()
        matched_skills = [skill for skill in job_skills if skill in proj_text]
        if matched_skills:
            mapping.append({
                'project': proj['name'],
                'skills': matched_skills
            })
    return mapping

def generate_project_mapping(resume_text, job_skills):
    projects = extract_projects(resume_text)
    mapping = map_projects_to_skills(projects, job_skills)
    
    lines = [
        "=" * 60,
        "PROJECT-TO-JOB MAPPING",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "This report maps your resume projects to job requirements.",
        ""
    ]
    
    if not mapping:
        lines.append("No clear project-to-skill mappings detected.")
        lines.append("Tip: Ensure your resume has a PROJECTS section with skill keywords.")
    else:
        for item in mapping:
            lines.append(f"PROJECT: {item['project']}")
            lines.append("  Demonstrates:")
            for skill in sorted(item['skills']):
                lines.append(f"    • {skill}")
            lines.append("")
    
    lines.append("")
    report = "\n".join(lines)
    save_text(os.path.join(OUTPUT_DIR, "project_mapping.txt"), report)
    log.info("Project mapping generated")
    return report

# Feature 3: Interview Answer Generator
def generate_interview_answers(job_skills, kb_text):
    answer_bank = {
        "python": "I have extensive Python experience from academic projects and personal work. I've used it for data analysis, ML model development, and API creation. I'm comfortable with OOP, functional programming, and async patterns.",
        "machine learning": "I follow a structured ML workflow: problem definition, data collection, EDA, preprocessing, feature engineering, model selection, training, evaluation, and deployment. I've worked with supervised and unsupervised learning.",
        "sql": "I use SQL for data extraction and analysis. I'm proficient in joins, subqueries, window functions, and query optimization. I've worked with PostgreSQL and MySQL in past projects.",
        "api": "I design RESTful APIs following best practices: resource-based URLs, proper HTTP methods, status codes, versioning via URL or headers, and authentication using JWT or OAuth.",
        "git": "I use Git for version control with feature branching. I follow GitFlow: main for production, develop for integration, feature branches for new work, and pull requests for code review.",
        "docker": "Docker allows me to containerize applications for consistent environments. I create Dockerfiles, use docker-compose for multi-container setups, and understand image layers and optimization.",
        "aws": "I've deployed applications on AWS using EC2, S3, and RDS. I understand IAM for security, CloudWatch for monitoring, and have basic knowledge of Lambda and API Gateway.",
        "deep learning": "I've built neural networks using TensorFlow and PyTorch. CNNs for image tasks, RNNs/LSTMs for sequences. I understand backpropagation, optimization algorithms, and regularization techniques.",
        "nlp": "I've worked on NLP projects involving tokenization, embeddings, and transformer models. I understand preprocessing steps like stemming, lemmatization, and have used libraries like NLTK and spaCy.",
        "communication": "I regularly explain technical concepts to non-technical stakeholders by using analogies, visual aids, and focusing on business impact rather than implementation details.",
        "problem solving": "I approach problems systematically: understand requirements, break down into smaller parts, research solutions, implement iteratively, test thoroughly, and document learnings.",
    }
    
    lines = [
        "=" * 60,
        "INTERVIEW ANSWERS (SAMPLE RESPONSES)",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "Use these as starting points — personalize with YOUR specific examples.",
        ""
    ]
    
    for skill in sorted(job_skills):
        if skill in answer_bank:
            lines.append(f"[{skill.upper()}]")
            lines.append(f"A: {answer_bank[skill]}")
            lines.append("")
    
    if kb_text:
        lines += [
            "KNOWLEDGE BASE TIPS:",
            "-" * 40,
            kb_text[:400].strip() + ("..." if len(kb_text) > 400 else ""),
            ""
        ]
    
    report = "\n".join(lines)
    save_text(os.path.join(OUTPUT_DIR, "interview_answers.txt"), report)
    log.info("Interview answers generated")
    return report

# Feature 4: Company Preparation Checklist
def generate_preparation_checklist(job_skills, matched, missing, resume_text):
    projects = extract_projects(resume_text)
    
    lines = [
        "=" * 60,
        "COMPANY PREPARATION CHECKLIST",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
        "SKILLS TO REVISE:",
        "-" * 40,
    ]
    
    if matched:
        lines.append("Your strong areas (refresh these):")
        for skill in sorted(matched)[:10]:
            lines.append(f"  ✓ {skill}")
    
    lines.append("")
    if missing:
        lines.append("Skills to learn/brush up (priority):")
        for skill in sorted(missing)[:5]:
            lines.append(f"  ⚠ {skill}")
    
    lines += [
        "",
        "TOPICS TO PREPARE:",
        "-" * 40,
        "  • Review job description thoroughly",
        "  • Research company culture and recent news",
        "  • Prepare STAR method examples for behavioral questions",
        "  • Practice coding problems (if technical role)",
        "  • Prepare questions to ask the interviewer",
        "",
        "PROJECTS TO REVIEW:",
        "-" * 40,
    ]
    
    if projects:
        for proj in projects[:5]:
            lines.append(f"  • {proj['name']}")
            lines.append(f"    Be ready to explain: architecture, challenges, outcomes")
    else:
        lines.append("  • Review all projects listed on your resume")
    
    lines += [
        "",
        "PRE-INTERVIEW CHECKLIST:",
        "-" * 40,
        "  [ ] Test video/audio setup",
        "  [ ] Prepare quiet, professional environment",
        "  [ ] Have resume and job description open",
        "  [ ] Prepare pen and paper for notes",
        "  [ ] Dress professionally",
        "  [ ] Join 5 minutes early",
        ""
    ]
    
    report = "\n".join(lines)
    save_text(os.path.join(OUTPUT_DIR, "preparation_checklist.txt"), report)
    log.info("Preparation checklist generated")
    return report

# Feature 5: Reminder Urgency System
def generate_reminders_with_urgency(rows):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    week_end = today + timedelta(days=7)
    
    overdue = []
    today_items = []
    tomorrow_items = []
    this_week = []
    later = []
    
    for row in rows:
        app_id = row.get("application_id", "N/A")
        company = row.get("company", "Unknown")
        role = row.get("role", "Unknown")
        status = row.get("status", "").strip().lower()
        int_date_str = row.get("interview_date", "").strip()
        fup_date_str = row.get("follow_up_date", "").strip()
        
        item = f"[{app_id}] {company} — {role}"
        
        # Check interview date
        if status == "interview scheduled" and int_date_str:
            try:
                int_date = datetime.strptime(int_date_str, "%Y-%m-%d").date()
                if int_date < today:
                    overdue.append(item + " | Interview was scheduled — send thank-you note")
                elif int_date == today:
                    today_items.append(item + " | INTERVIEW TODAY — final prep!")
                elif int_date == tomorrow:
                    tomorrow_items.append(item + " | Interview tomorrow — prepare now")
                elif int_date <= week_end:
                    this_week.append(item + f" | Interview on {int_date_str}")
                else:
                    later.append(item + f" | Interview on {int_date_str}")
            except ValueError:
                later.append(item + " | Interview scheduled (check date)")
        
        # Check follow-up date
        elif status == "applied" and fup_date_str:
            try:
                fup_date = datetime.strptime(fup_date_str, "%Y-%m-%d").date()
                if fup_date < today:
                    overdue.append(item + " | Follow-up overdue")
                elif fup_date == today:
                    today_items.append(item + " | Follow up today")
                elif fup_date == tomorrow:
                    tomorrow_items.append(item + " | Follow up tomorrow")
                elif fup_date <= week_end:
                    this_week.append(item + f" | Follow up by {fup_date_str}")
                else:
                    later.append(item + f" | Follow up by {fup_date_str}")
            except ValueError:
                later.append(item + " | Follow up when possible")
        
        elif status == "not applied":
            today_items.append(item + " | Submit application ASAP")
        else:
            later.append(item + f" | Status: {row.get('status', 'Unknown')}")
    
    lines = [
        "=" * 60,
        "APPLICATION REMINDERS (BY URGENCY)",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        ""
    ]
    
    if overdue:
        lines.append("🚨 OVERDUE:")
        lines.append("-" * 40)
        for item in overdue:
            lines.append(f"  {item}")
        lines.append("")
    
    if today_items:
        lines.append("📅 TODAY:")
        lines.append("-" * 40)
        for item in today_items:
            lines.append(f"  {item}")
        lines.append("")
    
    if tomorrow_items:
        lines.append("📆 TOMORROW:")
        lines.append("-" * 40)
        for item in tomorrow_items:
            lines.append(f"  {item}")
        lines.append("")
    
    if this_week:
        lines.append("📋 THIS WEEK:")
        lines.append("-" * 40)
        for item in this_week:
            lines.append(f"  {item}")
        lines.append("")
    
    if later:
        lines.append("📌 UPCOMING:")
        lines.append("-" * 40)
        for item in later:
            lines.append(f"  {item}")
        lines.append("")
    
    if not (overdue or today_items or tomorrow_items or this_week or later):
        lines.append("No applications tracked yet.")
        lines.append("")
    
    report = "\n".join(lines)
    save_text(os.path.join(OUTPUT_DIR, "reminders.txt"), report)
    log.info("Reminders with urgency generated")
    return report

# Feature 6: LinkedIn Message Generator
def generate_linkedin_message(company, role, resume_text):
    resume_skills = extract_keywords(resume_text)
    top_skills = ", ".join(sorted(resume_skills)[:4]) if resume_skills else "relevant skills"
    
    message = f"""Hi [Recruiter Name],

I hope this message finds you well. I came across the {role} position at {company} and am very interested in the opportunity.

I have a strong background in {top_skills}, and I believe my experience aligns well with the role's requirements. I'm particularly drawn to {company}'s work in [mention specific area if known].

I'd love to learn more about the position and discuss how I can contribute to your team. Would you be open to a brief conversation?

Thank you for your time and consideration.

Best regards,
[Your Name]
[Your LinkedIn Profile URL]"""
    
    path = os.path.join(OUTPUT_DIR, "linkedin_message.txt")
    save_text(path, message)
    log.info("LinkedIn message generated")
    return message

# Feature 7: JSON Memory File
def save_memory(job_skills, resume_skills, matched, missing, score):
    memory = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "job_skills": sorted(job_skills),
        "resume_skills": sorted(resume_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_score": score,
        "total_job_skills": len(job_skills),
        "total_resume_skills": len(resume_skills)
    }
    
    path = os.path.join(TRACKER_DIR, "memory.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)
    log.info(f"Memory saved to {path}")
    return memory

def load_memory():
    path = os.path.join(TRACKER_DIR, "memory.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ─── MENU INTERFACE ───────────────────────────────────────────────────────────

def print_menu():
    print("\n" + "=" * 50)
    print("  CareerPrep Job-Hunting Agent")
    print("=" * 50)
    print("  1.  Run Full Agent Pipeline")
    print("  2.  Score My Resume")
    print("  3.  Generate Cover Letter")
    print("  4.  View Application Tracker")
    print("  5.  Add Application to Tracker")
    print("  6.  View Reminders (with urgency)")
    print("  7.  Generate Project-to-Job Mapping")
    print("  8.  Generate Interview Answers")
    print("  9.  Generate Preparation Checklist")
    print("  10. Generate LinkedIn Message")
    print("  11. View Agent Memory")
    print("  0.  Exit")
    print("=" * 50)

def menu_loop():
    ensure_folders()
    init_tracker()

    while True:
        print_menu()
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            print("\n  Select files to analyze (press Enter / type 0 to use all):")
            job_file    = select_file(JOB_DIR, "job")
            resume_file = select_file(RESUME_DIR, "resume")
            score, matched, missing = run_agent(job_file, resume_file)
            print(f"\n  ✔ Pipeline complete. Match score: {score}%")
            print(f"  Matched: {len(matched)} | Missing: {len(missing)}")
            print(f"  Reports saved to '{OUTPUT_DIR}/'")

        elif choice == "2":
            job_text,    _ = read_text_files(JOB_DIR)
            resume_text, _ = read_text_files(RESUME_DIR)
            if not job_text or not resume_text:
                print("  ⚠ Add .txt files to input_jobs/ and input_resumes/ first.")
            else:
                final_score, report = score_resume(resume_text, job_text)
                print(report)

        elif choice == "3":
            company = input("  Company name: ").strip() or "Unknown Company"
            role    = input("  Role title  : ").strip() or "Software Engineer"
            job_text,    _ = read_text_files(JOB_DIR)
            resume_text, _ = read_text_files(RESUME_DIR)
            letter = generate_cover_letter(company, role, resume_text, job_text)
            print("\n" + letter)

        elif choice == "4":
            rows = load_tracker()
            if not rows:
                print("  No applications tracked yet.")
            else:
                print(f"\n  {'ID':<8} {'Company':<20} {'Role':<20} {'Status':<20}")
                print("  " + "-" * 70)
                for r in rows:
                    print(f"  {r['application_id']:<8} {r['company']:<20} {r['role']:<20} {r['status']:<20}")

        elif choice == "5":
            company = input("  Company : ").strip()
            role    = input("  Role    : ").strip()
            source  = input("  Source  : ").strip() or "job board"
            status  = input("  Status  : ").strip() or "Not Applied"
            notes   = input("  Notes   : ").strip()
            app_id  = add_application(company, role, source, status, notes)
            print(f"  ✔ Added {app_id}")

        elif choice == "6":
            rows = load_tracker()
            print("\n" + generate_reminders_with_urgency(rows))

        elif choice == "7":
            job_text,    _ = read_text_files(JOB_DIR)
            resume_text, _ = read_text_files(RESUME_DIR)
            job_skills = extract_keywords(job_text)
            report = generate_project_mapping(resume_text, job_skills)
            print("\n" + report)

        elif choice == "8":
            job_text, _ = read_text_files(JOB_DIR)
            kb_text,  _ = read_text_files(KB_DIR)
            job_skills  = extract_keywords(job_text)
            report = generate_interview_answers(job_skills, kb_text)
            print("\n" + report)

        elif choice == "9":
            job_text,    _ = read_text_files(JOB_DIR)
            resume_text, _ = read_text_files(RESUME_DIR)
            job_skills    = extract_keywords(job_text)
            resume_skills = extract_keywords(resume_text)
            matched, missing, _ = compare_skills(job_skills, resume_skills)
            report = generate_preparation_checklist(job_skills, matched, missing, resume_text)
            print("\n" + report)

        elif choice == "10":
            company      = input("  Company name: ").strip() or "[Company]"
            role         = input("  Role title  : ").strip() or "[Role]"
            resume_text, _ = read_text_files(RESUME_DIR)
            msg = generate_linkedin_message(company, role, resume_text)
            print("\n" + msg)

        elif choice == "11":
            memory = load_memory()
            if not memory:
                print("  No memory file found. Run the pipeline first.")
            else:
                print(f"\n  Last run     : {memory.get('timestamp')}")
                print(f"  Match score  : {memory.get('match_score')}%")
                print(f"  Job skills   : {memory.get('total_job_skills')}")
                print(f"  Resume skills: {memory.get('total_resume_skills')}")
                print(f"  Matched      : {len(memory.get('matched_skills', []))}")
                print(f"  Missing      : {len(memory.get('missing_skills', []))}")

        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice.")

# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    menu_loop()
