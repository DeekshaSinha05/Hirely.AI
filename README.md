# Hirely.AI

Automated Resume Screening & Interview Scheduling using Local LLMs (Ollama)

---

## 📌 Overview

This project introduces an AI-powered hiring assistant that automates resume screening and interview scheduling, minimizing human intervention. Leveraging a local LLM (via Ollama), it analyzes resumes, scores candidates, and suggests interview times—all while being privacy-friendly and cost-efficient.

---

## 🎯 Key Features

- Accepts multiple PDF resumes
- Extracts structured text using PyMuPDF
- Analyzes candidates against a job description with a local LLM (e.g., LLaMA 3)
- Scores candidates from 1 to 10, with justification
- **LLM-driven tools-based workflow:** LLM response includes a `tools` list (e.g., `["send_email"]`) for extensible actions
- Sends only well-formatted, professional emails to top candidates, always ending with the signature `Best regards,\nHirely.AI Team`
- Removes all placeholders (e.g., `{slot}`) before sending emails
- Suggests interview slots from a rotating weekly calendar (mocked)

---

## 🛠️ Tech Stack

| Component         | Tool/Lib        | Description                               |
| ----------------- | --------------- | ----------------------------------------- |
| 🧠 LLM Engine     | Ollama + LLaMA3 | Local inference, no OpenAI API costs      |
| 📄 PDF Parsing    | PyMuPDF         | Extracts structured text from resumes     |
| 🧑‍💻 Programming | Python 3.x      | Easy-to-read and extend                   |
| 📁 Resume Format  | PDF             | Realistic resumes with Faker              |

---

## ⚙️ Configuration

Before running the pipeline, you must configure your email credentials and (optionally) adjust other settings:

1. **Email Credentials:**
   - Create a file named `resources.py` in the project root (if not already present).
   - Add the following lines, replacing with your sender email and app password (for Gmail, use an App Password):
     ```python
     SENDER_EMAIL = "your_email@gmail.com"
     SENDER_PASSWORD = "your_app_password"
     ```
   - **Security Tip:** Never commit real credentials to version control. Use environment variables or a secrets manager for production.

2. **Ollama LLM Model:**
   - Ensure Ollama is installed and the LLaMA3 model is available locally.
   - The default API endpoint is `http://localhost:11434/api/generate` (see `scorer.py`).

3. **Job Description:**
   - Edit the `JOB_DESCRIPTION` variable in `main.py` to match your open role.

4. **LLM Prompt/JSON Structure:**
   - The LLM expects and returns a strict JSON format (see sample prompt below). No extra text or markdown is allowed in the response.

5. **Sample `resources.py` file:**
   ```python
   SENDER_EMAIL = "your_email@gmail.com"
   SENDER_PASSWORD = "your_app_password"
   ```

---

## ▶️ How to Run

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
2. **Start Ollama with the LLaMA3 model:**
   ```bash
   ollama run llama3
   ```
   (Make sure Ollama is installed and the LLaMA3 model is available.)
3. **Add PDF resumes** to the `resumes/` folder.
4. **Run the pipeline:**
   ```bash
   python3 main.py
   ```
5. **View results**: Top candidates and suggested interview slots will be printed in the terminal. Emails will be sent to top candidates if `send_email` is present in the LLM's tools list.

---

## ▶️ Generate Realistic Sample Resumes

To quickly add realistic PDF resumes for testing, run:

```bash
pip3 install Faker fpdf
python3 generate_resumes.py
```

This will create multiple realistic resumes for different tech roles in the `resumes/` folder.

---

## 🧪 How to Test

1. **Generate or collect sample PDF resumes** and place them in the `resumes/` folder.
   - You can use the [Faker](https://faker.readthedocs.io/) library to generate fake resume content and export as PDF.
2. **Run the main pipeline:**
   ```bash
   python3 main.py
   ```
3. **Check the terminal output:**
   - You should see a ranked list of candidates with scores and reasons.
   - Suggested interview slots will also be displayed.
   - Emails will be sent only if `send_email` is present in the LLM's tools list for that candidate.
4. **(Optional) Test with different job descriptions:**
   - Edit the `JOB_DESCRIPTION` variable in `main.py` to try different roles.
5. **(Optional) Add more resumes or modify existing ones** to see how the scoring changes.

If you encounter errors, ensure:
- All dependencies are installed (`pip3 install -r requirements.txt`)
- Ollama is running and the LLaMA3 model is available
- Your PDF files are not corrupted

---

## 📂 Project Structure

```
/ai-hiring-agent/
├── main.py                # Entry point: orchestrates the pipeline
├── resume_parser.py       # PDF extraction logic (PyMuPDF)
├── scorer.py              # LLM prompt, scoring, and tools-based action logic (Ollama)
├── scheduler.py           # Mock interview slot suggestion
├── requirements.txt       # Python dependencies
├── /resumes/              # Sample PDF resumes
└── README.md              # Project documentation
```

---

## 🚀 How It Works (Pipeline)

1. Upload PDF resumes
2. Extract text using PyMuPDF
3. Score each candidate via Ollama + prompt
4. LLM returns a JSON with score, reason, tools list, and (if needed) email subject/body
5. Rank and print top candidates
6. Suggest interview slots (mocked for now)
7. Send emails only if `send_email` is present in the tools list, ensuring all formatting and signature requirements are met

---

## 🤖 Sample Prompt Used (LLM)

```
You are an AI hiring assistant.
Job Description:
{job_description}

Candidate Resume:
{resume_text}

Rate this candidate from 1 to 10 based on skill and experience match.
Explain briefly why.
If the candidate should be contacted for an interview, include 'send_email' in the tools list, otherwise leave the list empty.
If 'send_email' is present in tools, also provide a well-formatted, complete, and professional email subject and body for the candidate, referencing the interview slot as {slot}. The email body must always be a clear, polite, and complete invitation, never blank or just a JSON dump. The email_body must be at least 5 lines (each line separated by a newline), and must include a greeting, a reason for the invitation, the interview slot, a request for confirmation, and must always end with the signature 'Best regards,\nHirely.AI Team'.

Respond ONLY in the following JSON format (no explanation, no markdown, no extra text):
{
  "score": <int>,
  "reason": <string>,
  "tools": <list of strings>,
  "email_subject": <string>,
  "email_body": <string>
}
```

---

## 📈 Possible Extensions

- Integrate real-time interview scheduling with Google Calendar API
- Use embeddings + vector DB for advanced semantic matching
- Build a front-end UI (Streamlit or Flask)
- Support multiple job descriptions or job families

