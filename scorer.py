import requests
import json

def score_candidate(job_description, resume_text):
    prompt = (
        f"""
You are an AI hiring assistant.\nJob Description:\n{job_description}\n\nCandidate Resume:\n{resume_text}\n\nRate this candidate from 1 to 10 based on skill and experience match.\nExplain briefly why.\nIf the candidate should be contacted for an interview, include 'send_email' in the tools list, otherwise leave the list empty.\nIf 'send_email' is present in tools, also provide a well-formatted, complete, and professional email subject and body for the candidate, referencing the interview slot as {{slot}}. The email body must always be a clear, polite, and complete invitation, never blank or just a JSON dump. The email_body must be at least 5 lines (each line separated by a newline), and must include a greeting, a reason for the invitation, the interview slot, a request for confirmation, and must always end with the signature 'Best regards,\nHirely.AI Team'.\n\nRespond ONLY in the following JSON format (no explanation, no markdown, no extra text):\n{{\n  \"score\": <int>,\n  \"reason\": <string>,\n  \"tools\": <list of strings>,\n  \"email_subject\": <string>,\n  \"email_body\": <string>\n}}\n"""
    )
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print("\n[DEBUG] Ollama API output:\n", result.get("response", ""))
        # Try to extract JSON from the response
        try:
            json_start = result["response"].find('{')
            json_str = result["response"][json_start:]
            parsed = json.loads(json_str)
            score = parsed.get("score", 0)
            reason = parsed.get("reason", "")
            tools = parsed.get("tools", [])
            email_subject = parsed.get("email_subject", "Interview Availability Check - Hirely.AI")
            email_body = parsed.get("email_body", "")
            # Clean up email_subject: remove leading/trailing quotes and commas
            if email_subject:
                email_subject = email_subject.strip().strip('"').strip("',. ")
            # Determine if send_email is in tools
            should_email = "send_email" in tools if isinstance(tools, list) else False
            # Replace {slot} in email_body with actual slot if present
            # (slot will be replaced in main.py, so here just ensure placeholder is present)
            if should_email and (not email_body or len(email_body.strip().splitlines()) < 5 or email_body.strip().startswith('{')):
                email_body = (
                    f"Dear Candidate,\n\n"
                    f"We are pleased to invite you for an interview for the Software Engineer position.\n"
                    f"The interview is scheduled for {{slot}}.\n"
                    f"Please reply to confirm your availability or suggest an alternative time.\n"
                    f"\nBest regards,\nHirely.AI Team"
                )
            # Ensure {slot} is present in the email body
            if should_email and "{slot}" not in email_body:
                # Try to insert slot after the first line mentioning 'interview'
                lines = email_body.splitlines()
                for idx, line in enumerate(lines):
                    if "interview" in line.lower():
                        lines.insert(idx + 1, "The interview is scheduled for {slot}.")
                        break
                else:
                    lines.append("The interview is scheduled for {slot}.")
                email_body = "\n".join(lines)
            return score, reason, tools, email_subject, email_body
        except Exception:
            # Fallback: try to parse score and reason from text
            lines = result["response"].split("\n")
            score = 0
            reason = ""
            tools = []
            email_subject = "Interview Availability Check - Hirely.AI"
            email_body = ""
            for line in lines:
                if "score" in line.lower():
                    try:
                        score = int(''.join(filter(str.isdigit, line)))
                    except:
                        score = 0
                if "reason" in line.lower() or "because" in line.lower():
                    reason = line
                if "tools" in line.lower() and "send_email" in line.lower():
                    tools = ["send_email"]
                if "email_subject" in line.lower():
                    email_subject = line.split(":", 1)[-1].strip().strip('"').strip("',. ")
                if "email_body" in line.lower():
                    email_body = line.split(":", 1)[-1].strip()
            # Ensure fallback email_body is well formatted and at least 5 lines
            should_email = "send_email" in tools
            if should_email and (not email_body or len(email_body.strip().splitlines()) < 5 or email_body.strip().startswith('{')):
                email_body = (
                    f"Dear Candidate,\n\n"
                    f"We are pleased to invite you for an interview for the Software Engineer position.\n"
                    f"The interview is scheduled for {{slot}}.\n"
                    f"Please reply to confirm your availability or suggest an alternative time.\n"
                    f"\nBest regards,\nHirely.AI Team"
                )
            # Ensure {slot} is present in the email body
            if should_email and "{slot}" not in email_body:
                lines = email_body.splitlines()
                for idx, line in enumerate(lines):
                    if "interview" in line.lower():
                        lines.insert(idx + 1, "The interview is scheduled for {slot}.")
                        break
                else:
                    lines.append("The interview is scheduled for {slot}.")
                email_body = "\n".join(lines)
            return score, reason or result["response"], tools, email_subject, email_body
    except Exception as e:
        print("[ERROR] Ollama API call failed:", e)
        return 0, "Ollama API error", [], "Interview Availability Check - Hirely.AI", ""
