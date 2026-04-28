# Reflection — CareerPrep Job-Hunting Agent

## Work Done

Built a complete, end-to-end job-hunting agent in Python covering:

- **File I/O pipeline** — reads job postings, resumes, and knowledge base from folders
- **Keyword extraction** — normalized text matching against an extended 60+ keyword list
- **Skill gap analysis** — compares job requirements vs resume skills with a percentage score
- **Report generation** — six distinct output reports saved to the `outputs/` folder
- **CSV application tracker** — tracks company, role, status, dates, and next actions
- **Smart reminders** — context-aware messages based on application status and dates
- **Resume scoring** — multi-factor scoring (skill match + length + action verbs)
- **Cover letter generator** — personalized letters using matched skills
- **Menu-driven CLI** — interactive interface for all features without code changes

## Challenges

1. **Keyword matching accuracy** — Simple substring matching can produce false positives
   (e.g., "c" matching inside words). Solved by using `\b` word-boundary regex.

2. **Empty folder handling** — Agent must not crash when input folders are empty.
   Solved with early-return guards and informative log warnings.

3. **Tracker date logic** — Reminder logic needed careful date parsing with try/except
   to handle missing or malformed dates gracefully.

4. **Report quality without an LLM** — Generating useful, readable reports using only
   rule-based logic required careful template design and conditional messaging.

## What I Learned

- How to design a modular, single-file Python agent with clear separation of concerns
- Importance of defensive programming (empty inputs, missing files, bad dates)
- How keyword extraction and skill gap analysis form the core of resume-matching tools
- How to build a practical CLI menu that makes a tool accessible without a GUI

## Possible Improvements

1. **LLM integration** — Connect to OpenAI or AWS Bedrock for natural language report generation
2. **Streamlit UI** — Replace CLI menu with a web dashboard for better UX
3. **PDF parsing** — Use `pdfplumber` or `PyMuPDF` to read PDF resumes directly
4. **Email reminders** — Auto-send follow-up reminders via `smtplib`
5. **Job scraping** — Integrate with LinkedIn or Indeed APIs to auto-fetch job postings
6. **Vector similarity** — Use embeddings for semantic skill matching beyond keyword overlap
