# 🎯 AI-Powered Mock Interview Platform

An interactive, AI-driven mock interview platform built with **Streamlit** and **Anthropic Claude**. Practice interviews for any role, get real-time AI feedback, and track your progress over time.

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd mock_interview_platform
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run main.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
mock_interview_platform/
├── main.py                    ← Streamlit app (all pages)
├── mock_interview.ipynb       ← Dev & analysis notebook
├── requirements.txt
├── .gitignore
├── README.md
├── backend/
│   ├── __init__.py
│   ├── interview_engine.py    ← AI question generation
│   ├── evaluator.py           ← AI answer evaluation
│   └── session_manager.py     ← Session persistence
└── data/
    └── sessions.json          ← Auto-created
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI Questions | Dynamic role-specific questions via Claude API |
| 📊 Live Scoring | Real-time 1–10 scoring per answer |
| 💬 Feedback | Strengths, weaknesses, and improvement tips |
| 📖 Sample Answers | AI-generated model answers for comparison |
| 📈 Dashboard | Analytics charts across all sessions |
| 📜 History | Browse and review past sessions |
| ⚙️ Difficulty | Beginner / Intermediate / Advanced / Expert |

---

## 🎭 Supported Roles

- Software Engineer
- Data Scientist
- Product Manager
- DevOps Engineer
- Frontend / Backend Developer
- Machine Learning Engineer
- System Design Engineer
- HR Manager
- Business Analyst

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit Frontend             │
│  Home → Interview Room → Results → Dashboard │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────▼──────────┐
        │    Backend (Python)  │
        │  InterviewEngine     │
        │  ResponseEvaluator   │
        │  SessionManager      │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   Anthropic Claude   │
        │  Question Generation │
        │  Answer Evaluation   │
        └─────────────────────┘
```

---

## 📊 Scoring System

| Score | Grade | Label |
|---|---|---|
| 9–10 | A+ | Outstanding |
| 8–9  | A  | Excellent |
| 7–8  | B+ | Very Good |
| 6–7  | B  | Good |
| 5–6  | C  | Average |
| 4–5  | D  | Below Average |
| 1–4  | F  | Needs Improvement |

---

## 📓 Notebook

The `mock_interview.ipynb` notebook covers:
- Architecture overview
- API integration testing
- Question generation pipeline
- Answer evaluation pipeline
- Analytics & visualizations
- End-to-end simulation

---

## 📦 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **AI**: Anthropic Claude (claude-sonnet-4)
- **Analytics**: Pandas, Matplotlib, Seaborn
- **Storage**: JSON (local)

---

## 🎓 Learning Outcomes

By building this project you will understand:
- Full-stack AI app development
- LLM API integration
- Streamlit session state management
- NLP-based evaluation systems
- Data visualization with Pandas/Matplotlib
