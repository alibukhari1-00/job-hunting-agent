"""
validate.py — Runs the full agent pipeline non-interactively and prints results.
Usage: python validate.py
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import (
    run_agent, score_resume, generate_cover_letter,
    read_text_files, load_tracker
)

print("=" * 60)
print("CareerPrep Agent — Validation Run")
print("=" * 60)

# 1. Full pipeline
score, matched, missing = run_agent()
print(f"\n[Pipeline] Match Score : {score}%")
print(f"[Pipeline] Matched     : {len(matched)} skills")
print(f"[Pipeline] Missing     : {len(missing)} skills")

# 2. Resume scoring
job_text,    _ = read_text_files("input_jobs")
resume_text, _ = read_text_files("input_resumes")
final_score, _ = score_resume(resume_text, job_text)
print(f"\n[Resume Score] {final_score} / 100")

# 3. Cover letter
letter = generate_cover_letter("TechVision AI", "ML Engineer", resume_text, job_text)
print(f"\n[Cover Letter] Generated ({len(letter)} chars)")

# 4. Tracker
rows = load_tracker()
print(f"\n[Tracker] {len(rows)} application(s) tracked")
for r in rows:
    print(f"  {r['application_id']} | {r['company']:<20} | {r['role']:<20} | {r['status']}")

# 5. Output files
outputs = sorted(os.listdir("outputs"))
print(f"\n[Outputs] {len(outputs)} file(s) in outputs/")
for f in outputs:
    size = os.path.getsize(os.path.join("outputs", f))
    print(f"  {f} ({size} bytes)")

print("\n" + "=" * 60)
print("Validation complete — all systems OK.")
print("=" * 60)
