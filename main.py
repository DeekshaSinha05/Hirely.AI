import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from resume_parser import extract_resume_text
from scorer import score_candidate
from scheduler import suggest_interview_slots
import re
from resources import SENDER_EMAIL, SENDER_PASSWORD
import logging

logging.basicConfig(filename='hirely_ai.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

RESUME_DIR = "resumes"
JOB_DESCRIPTION = """
Software Engineer with experience in Python, machine learning, and cloud infrastructure. Must have strong problem-solving skills and experience with REST APIs.
"""

def extract_email(resume_text):
    # Always use dscodetest@gmail.com as the receiver email for testing
    email = "dscodetest@gmail.com"
    logging.info(f"Extracted email (forced for test): {email}")
    return email

def email_candidate(candidate_name, candidate_email, slot):
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD  # Use app password or env var in production
    subject = "Interview Availability Check - Hirely.AI"
    body = f"Dear {candidate_name},\n\nWe are considering you for an interview slot: {slot}.\nPlease reply to confirm your availability or suggest alternatives.\n\nBest,\nHirely.AI Team"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = candidate_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, candidate_email, msg.as_string())
        print(f"[INFO] Email sent to {candidate_name} at {candidate_email} for slot {slot}")
        logging.info(f"Email sent to {candidate_name} <{candidate_email}> for slot {slot}")
    except Exception as e:
        print(f"[ERROR] Failed to send email to {candidate_email}: {e}")
        logging.error(f"Failed to send email to {candidate_email}: {e}")

def main():
    resumes = [f for f in os.listdir(RESUME_DIR) if f.endswith(".pdf")]
    candidates = []
    for resume_file in resumes:
        resume_path = os.path.join(RESUME_DIR, resume_file)
        resume_text = extract_resume_text(resume_path)
        score, reason = score_candidate(JOB_DESCRIPTION, resume_text)
        email = extract_email(resume_text)
        candidates.append({
            "name": resume_file,
            "score": score,
            "reason": reason,
            "email": email
        })
    candidates.sort(key=lambda x: x["score"], reverse=True)
    print("\nTop Candidates:")
    for c in candidates:
        print(f"{c['name']}: {c['score']} - {c['reason']}")
    print("\nSuggested Interview Slots:")
    slots = suggest_interview_slots(len(candidates))
    for i, slot in enumerate(slots):
        print(slot)
        # Email top N candidates (e.g., top 3)
        if i < 3 and candidates[i]["email"]:
            candidate_name = candidates[i]["name"].replace('_', ' ').replace('.pdf', '')
            email_candidate(candidate_name, candidates[i]["email"], slot)

if __name__ == "__main__":
    main()
