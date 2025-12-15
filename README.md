# 📊 DataPilotX — AI-Powered Analytics Platform

DataPilotX is a full-stack AI-powered analytics application that allows users to upload CSV datasets and query them using natural language.
It combines modern backend engineering, large language models, and a clean frontend to deliver business-friendly insights with explainable logic.

---

## 🚀 Key Features

- 📁 CSV Upload & Dataset Management
- 🤖 Natural Language Querying (Ask AI)
- 🧠 LLM-powered Analytics using Groq + LangChain
- 🔍 Explainable AI
  - Final business answer
  - Optional reasoning
  - Optional computation code (Python / Pandas)
- 📊 Dataset Dashboard & Preview
- 🎨 Modern, Clean Frontend UI (React + Tailwind)
- ⚡ FastAPI Backend (high performance)
- 🛡️ Robust error handling & safe fallbacks

---

## 🧱 Tech Stack

### Backend
- FastAPI
- Python 3.14
- LangChain
- Groq LLM (free tier)
- Pandas
- Uvicorn

### Frontend
- React (Vite)
- Tailwind CSS
- Modern component-based architecture

### Tooling
- Git & GitHub
- Local development (macOS compatible)

---

## 🏗️ Project Architecture

DataPilotX/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── routers/
│   │   │   └── qa.py         # AI question answering
│   │   ├── dataset_store.py # In-memory dataset management
│   │   └── llm_factory.py   # LLM provider setup (Groq / Dummy)
│   └── data/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── AskAI.jsx
│   │   └── pages/
│   └── tailwind.config.js
│
└── README.md

---

## 🧠 How It Works

1. User uploads a CSV file.
2. Backend parses and stores the dataset.
3. User asks a question in natural language.
4. The system:
   - Selects the latest dataset (or a specified one)
   - Sends a context-aware prompt to the LLM
   - Receives structured output:
     - Answer
     - Reasoning
     - Code
5. Frontend displays:
   - A clean answer by default
   - An expandable section for reasoning & code

---

## ⚙️ Setup & Run Locally

### Clone the Repository
git clone https://github.com/rahulgithubral/DataPilotX.git
cd DataPilotX

---

### Backend Setup
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Create a .env file:
GROQ_API_KEY=your_groq_api_key_here

Run backend:
uvicorn app.main:app --reload

Backend runs at:
http://127.0.0.1:8000

---

### Frontend Setup
Open a new terminal:
cd frontend
npm install
npm run dev

Frontend runs at:
http://localhost:5173

---

## 🧪 Example Questions

- Which category has the highest total sales?
- Show sales trends over time.
- Summarise this dataset.
- Which product performed best?

---

## 💡 Design Philosophy

- Business-first answers
- Explainable AI by design
- Clean separation of backend & frontend
- Minimal but extensible architecture
- Interview-ready and real-world focused

---

## 🚧 Future Improvements

- Automatic chart generation
- Dark mode
- Export insights as reports
- Multi-dataset comparison
- Deployment (Docker / Cloud)

---

## 👤 Author

Rahul R S  
Software / AI Enthusiast

---

## ⭐ Why This Project Matters

This project demonstrates:
- Full-stack engineering
- LLM integration
- API design
- Frontend UX thinking
- Explainable AI principles

It is built to reflect real-world product engineering, not just a demo.

---

## 📜 License

MIT License
