AI-Powered Personalized Learning Platform

An intelligent full-stack EdTech system that detects hidden student knowledge gaps and delivers personalized, adaptive, and explainable learning experiences using Machine Learning, Knowledge Graphs, and NLP.

📌 Project Overview

Traditional learning systems follow a one-size-fits-all approach and fail to identify concept-level knowledge gaps.

This platform applies Artificial Intelligence and Machine Learning to:

Detect unseen knowledge gaps

Personalize learning paths

Recommend adaptive content

Generate smart quizzes

Provide explainable AI-driven suggestions

Support learners with a conversational tutor

🎓 Developed as a B.Tech AIML Mini Project – GLA University

🧠 Key Features
🔐 Authentication

Secure student registration & login

Google OAuth 2.0 social login

JWT-based session management

🧩 Knowledge Modeling

Knowledge Graph modeling of domain concepts

Prerequisite relationship mapping

Student proficiency tracking

📊 Knowledge Gap Detection (Core ML)

Bayesian Knowledge Tracing / Mastery model

Concept-level probability estimation

Hidden prerequisite gap detection

🔄 Adaptive Learning Engine

Dynamic concept sequencing

Personalized difficulty adjustment

Continuous mastery updates

🎯 AI-Powered Recommendations

Content ranking based on knowledge gaps

Hybrid ML + rule-based recommender

Personalized revision suggestions

📝 Smart Quiz Generator

ML-based question difficulty classification

Weak-concept targeting

Personalized quiz creation

🤖 TutorVoice (Conversational AI)

Text-based AI assistant

Concept explanations

Learning path guidance

📘 NoteFlow

AI-generated personalized notes

Concept flow summaries

🔁 MemoryBoost

Microlearning approach

Spaced repetition scheduling (1–3–7 day cycle)

🏗 System Architecture
Frontend (React + Tailwind)
        ↓
Backend API (Flask / FastAPI)
        ↓
ML Engine (Gap Detection + Recommendation)
        ↓
Database (PostgreSQL / MongoDB)
        ↓
Knowledge Graph (Neo4j)
🛠 Tech Stack
Layer	Technology
Frontend	React.js, Tailwind CSS
Backend	Flask / FastAPI (Python)
Machine Learning	Scikit-learn, NumPy
NLP	GPT / BERT
Database	PostgreSQL / MongoDB
Knowledge Graph	Neo4j
Authentication	JWT + Google OAuth 2.0
📂 Project Structure
/frontend
/backend
/models
/knowledge_graph
README.md
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-username/ai-personalized-learning.git
cd ai-personalized-learning
2️⃣ Backend Setup
cd backend
pip install -r requirements.txt
python app.py
3️⃣ Frontend Setup
cd frontend
npm install
npm start
🔐 Environment Variables

Create a .env file inside backend:

SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_secret
DATABASE_URL=your_database_url
📈 Future Enhancements

Deep Knowledge Tracing (LSTM)

Voice-based AI assistant

Teacher analytics dashboard

Emotion-aware learning detection

Multi-subject scalability

🎓 Academic Context

This project demonstrates practical implementation of:

Machine Learning in Education

Knowledge Graph Modeling

Explainable AI

NLP-based Conversational Systems

Adaptive Learning Systems

👨‍💻 Authors

Backend & ML Lead

Frontend Developer

QA & Documentation

B.Tech CSE (AIML) – GLA University

⭐ Why This Project Matters

This platform moves beyond static learning by integrating AI-driven personalization and concept-level mastery detection to enhance learning efficiency and engagement.
