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
5. **View results**: Top candidates and suggested interview slots will be printed in the terminal.

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
├── scorer.py              # LLM prompt & scoring logic (Ollama)
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
4. Rank and print top candidates
5. Suggest interview slots (mocked for now)

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
```

---

## 📈 Possible Extensions

- Integrate real-time interview scheduling with Google Calendar API
- Use embeddings + vector DB for advanced semantic matching
- Build a front-end UI (Streamlit or Flask)
- Support multiple job descriptions or job families

---

## 👩‍🏫 Ideal For

- AI code-along lab sessions (30 mins)
- Students learning local LLM apps
- Startups building recruitment tools
- Offline demos (no internet needed!)
