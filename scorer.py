import requests
import json

def score_candidate(job_description, resume_text):
    prompt = f"""
You are an AI hiring assistant.\nJob Description:\n{job_description}\n\nCandidate Resume:\n{resume_text}\n\nRate this candidate from 1 to 10 based on skill and experience match.\nExplain briefly why.\nRespond in JSON: {{\"score\": <int>, \"reason\": <string>}}\n"""
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
            return parsed["score"], parsed["reason"]
        except Exception:
            # Fallback: try to parse score and reason from text
            lines = result["response"].split("\n")
            score = 0
            reason = ""
            for line in lines:
                if "score" in line.lower():
                    try:
                        score = int(''.join(filter(str.isdigit, line)))
                    except:
                        score = 0
                if "reason" in line.lower() or "because" in line.lower():
                    reason = line
            return score, reason or result["response"]
    except Exception as e:
        print("[ERROR] Ollama API call failed:", e)
        return 0, "Ollama API error"
