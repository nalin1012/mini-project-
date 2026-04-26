cd backend #  AI-Powered Personalized Learning Platform

An intelligent full-stack EdTech system that detects knowledge gaps and delivers personalized, adaptive learning experiences powered by **AI, Machine Learning, and Real-time Analytics**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-16.1+-black?logo=next.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql)
![AI](https://img.shields.io/badge/AI-ML--Powered-purple)

---

## 🎯 Problem Statement

Traditional educational platforms use a **one-size-fits-all approach** and fail to:
- Identify concept-level knowledge gaps
- Adapt to individual learning pace
- Provide intelligent recommendations
- Track misconceptions dynamically
- Offer real-time guidance

**Our Solution:** An AI-powered platform that analyzes student performance, detects weak areas, and recommends personalized learning paths.

---

## 🚀 Key Features

### 1. **Knowledge Gap Detection (Core Feature)**
- ✅ Analyzes quiz performance per topic
- ✅ Identifies weak areas automatically
- ✅ Tracks learning progress in real-time
- ✅ Provides actionable recommendations

### 2. **Adaptive Quiz System**
- ✅ Dynamically generated questions based on topic
- ✅ Difficulty adjusts based on user performance
- ✅ If score < 60%: Easy questions recommended
- ✅ If score ≥ 80%: Advanced challenges offered
- ✅ One question at a time with immediate feedback
- ✅ Timer for each quiz session
- ✅ Result analysis with weak area identification

### 3. **AI Tutor (TutorVoice)**
- ✅ Interactive chatbot for concept explanation
- ✅ Ask questions on: Fractions, Algebra, Loops, Variables, Functions
- ✅ Get step-by-step explanations
- ✅ Real-time examples and tips
- ✅ Context-aware responses

### 4. **Modern Dashboard**
- ✅ Real-time statistics (Quizzes, Accuracy, Weak Areas)
- ✅ Subject explorer with 5 core subjects
- ✅ Knowledge gap alerts
- ✅ Learning progress tracking
- ✅ Personalized recommendations

### 5. **Secure Authentication**
- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ Input validation with Pydantic
- ✅ CORS middleware enabled
- ✅ Demo user mode for testing

### 6. **Backend-Frontend Integration**
- ✅ RESTful APIs for all features
- ✅ Real-time data synchronization
- ✅ Error handling and loading states
- ✅ Demo data fallback for testing

---

## 📁 Project Structure

```
mini-project/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── auth.py                 # JWT authentication & password hashing
│   ├── database.py             # Database configuration (SQLite/PostgreSQL)
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── quiz.py                 # Quiz generation & submission APIs
│   ├── progress.py             # Knowledge gap detection & tracking
│   ├── students.py             # AI Tutor chatbot backend
│   ├── recommendations.py      # ML-based recommendations
│   ├── machine_learning/
│   │   ├── __init__.py
│   │   └── ml_model.py         # ML model for gap detection
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Landing page
│   │   ├── login/page.tsx      # Login page
│   │   ├── register/page.tsx   # Registration page
│   │   ├── dashboard/page.tsx  # Main dashboard (API integrated)
│   │   ├── quiz/page.tsx       # Adaptive quiz page (API integrated)
│   │   ├── subjects/page.tsx   # Subject explorer
│   │   ├── profile/page.tsx    # User profile
│   │   └── layout.tsx          # Root layout
│   │
│   ├── components/
│   │   ├── login-form.tsx      # Login form with API
│   │   ├── tutor-chat.tsx      # AI Tutor chatbot UI (API integrated)
│   │   ├── dashboard-navbar.tsx
│   │   └── ui/                 # Reusable UI components
│   │
│   ├── lib/
│   │   └── utils.ts            # Utility functions
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.mjs
│
└── README.md                   # This file
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND (Next.js + React)            │
├─────────────────────────────────────────────────────────┤
│  Login | Dashboard | Quiz | Tutor Chat | Subjects       │
├─────────────────────────────────────────────────────────┤
│           REST APIs (Axios/Fetch) with JWT Auth          │
└─────────────┬───────────────────────────────────────────┘
              │ HTTP/REST
              │
┌─────────────▼───────────────────────────────────────────┐
│              BACKEND (FastAPI + Python)                  │
├─────────────────────────────────────────────────────────┤
│  Authentication | Quiz Generation | Knowledge Gap       │
│  Detection | AI Tutor | Recommendations                 │
├─────────────────────────────────────────────────────────┤
│        SQLAlchemy ORM | SQL Database Layer              │
└─────────────┬───────────────────────────────────────────┘
              │ SQL Queries
              │
┌─────────────▼───────────────────────────────────────────┐
│          DATABASE (SQLite or PostgreSQL)                 │
├─────────────────────────────────────────────────────────┤
│  Users | QuizResults | LearningProgress | WeakAreas     │
│  Subjects | Topics | Questions                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI 0.104.1
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **ORM:** SQLAlchemy 2.0
- **Authentication:** JWT + bcrypt
- **Validation:** Pydantic v2
- **Server:** Uvicorn

### Frontend
- **Framework:** Next.js 16.1
- **UI Library:** React 19
- **Styling:** Tailwind CSS v4
- **Components:** Radix UI
- **HTTP Client:** Fetch API
- **Language:** TypeScript

---

## 📊 Database Models

### User
```python
- id (PK)
- email (unique)
- hashed_password
- name
- role (student/teacher/admin)
- created_at
```

### QuizResult
```python
- id (PK)
- student_id (FK → User)
- topic_id (FK → Topic)
- question_id (FK → Question)
- selected_option
- is_correct (boolean)
- time_taken (seconds)
- created_at
```

### LearningProgress
```python
- id (PK)
- student_id (FK → User)
- subject_id (FK → Subject)
- concept
- mastery_score (0-1)
- sessions_completed
- correct_answers
- total_questions_attempted
- last_updated
```

### WeakArea
```python
- id (PK)
- student_id (FK → User)
- topic_id (FK → Topic)
- mastery_score (< 0.6 = weak)
- total_attempts
- correct_attempts
- last_tested
```

### Subject, Topic, Question
Standard educational content models

---

## 🔄 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Quiz
- `GET /api/quiz/generate/{subject}/{topic}` - Generate adaptive quiz
- `POST /api/quiz/submit-answer` - Submit quiz answer
- `GET /api/quiz/stats` - Get user quiz statistics

### Knowledge Gap Detection
- `GET /api/knowledge-gap/detect` - Detect knowledge gaps
- `GET /api/knowledge-gap/progress/{topic}` - Get topic progress
- `GET /api/knowledge-gap/dashboard-summary` - Get dashboard data
- `POST /api/knowledge-gap/mark-mastered/{topic}` - Mark topic mastered

### AI Tutor
- `POST /api/tutor/ask` - Ask tutor a question
- `GET /api/tutor/topics` - Get available topics
- `GET /api/tutor/explain/{topic}` - Get topic explanation
- `POST /api/tutor/practice-hint/{topic}` - Get practice hint

### Recommendations
- `GET /api/recommendations/analyze/{concept}` - Analyze performance
- `GET /api/recommendations/personalized/{user_id}` - Get recommendations

### General
- `GET /` - API health check
- `GET /api/health` - Health status
- `GET /api/subjects` - Get all subjects

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Backend Setup

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Create `.env` file (optional):**
```env
DATABASE_URL=sqlite:///./learning_platform.db
SECRET_KEY=your-secret-key-here
```

3. **Run the backend:**
```bash
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: `http://192.168.0.131:8001`
API Docs: `http://192.168.0.131:8001/api/docs` (Swagger UI)

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
pnpm install
# OR
npm install
```

2. **Create `.env.local` file:**
```env
NEXT_PUBLIC_API_URL=http://192.168.0.131:8001
```

3. **Run development server:**
```bash
pnpm dev
# OR
npm run dev
```

Frontend runs on: `http://localhost:3000`

---

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest test_api.py -v
```

### Manual API Testing (using curl)
```bash
# Register
curl -X POST http://192.168.0.131:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123","name":"Test User"}'

# Login
curl -X POST http://192.168.0.131:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123"}'

# Generate Quiz
curl -X GET "http://192.168.0.131:8001/api/quiz/generate/Math/Fractions?count=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📱 Usage Guide

### As a Student

1. **Register/Login**
   - Go to `/login` or `/register`
   - Use demo button for instant access

2. **View Dashboard**
   - See your learning stats
   - View weak areas (if any)
   - Check study recommendations

3. **Take a Quiz**
   - Click subject card or "Start a Quiz"
   - Answer questions one by one
   - Get instant feedback and score

4. **Use AI Tutor**
   - Open tutor chat on dashboard
   - Ask about: "Fractions", "Algebra", "Loops", etc.
   - Get explanations and examples

5. **Track Progress**
   - Check accuracy percentage
   - Review weak areas
   - Practice recommended topics

---

## 🎨 UI/UX Design

### Color Scheme
- **Primary:** Blue (#2563EB)
- **Secondary:** Purple (#9333EA)
- **Background:** Dark (#0B0F1A)
- **Accents:** Cyan, Neon Blue, Purple gradients

### Design Patterns
- Glassmorphism cards with transparency
- Neon glow effects on interactive elements
- Smooth hover animations
- Responsive grid layouts
- Dark theme with high contrast

### Pages
- **Login Page** - Clean authentication form
- **Dashboard** - Stats, weak areas, subject grid
- **Quiz Page** - Question-by-question with timer
- **Subjects Page** - Browse all topics
- **Profile Page** - User settings

---

## 🔐 Security Features

✅ **Password Security**
- Bcrypt hashing with salt
- Min 8 characters recommended
- Never stored in plain text

✅ **Authentication**
- JWT tokens with expiration (30 days)
- HTTP-only cookie support
- Bearer token validation

✅ **Data Validation**
- Pydantic schemas on all endpoints
- Email format validation
- Type checking

✅ **API Security**
- CORS middleware configured
- Rate limiting ready (can be added)
- SQL Injection prevention via ORM

---

## 📈 Performance Optimizations

- Client-side caching with localStorage
- Lazy loading of components
- API response pagination (ready)
- Database indexing on frequently queried fields
- CSS-in-JS optimization with Tailwind

---

## 🚀 Deployment

### Backend (Heroku/Railway)
```bash
git push heroku main
```

### Frontend (Vercel)
```bash
vercel deploy
```

### Update environment variables on deployment
```env
# Backend
DATABASE_URL=postgresql://...
SECRET_KEY=your-production-key

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourapp.com
```

---

## 📚 Future Improvements

- [ ] Advanced ML model for better gap detection
- [ ] Video content for topics
- [ ] Gamification (badges, leaderboards)
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Integration with LMS (Moodle, Canvas)
- [ ] Advanced analytics dashboard for teachers
- [ ] Speech-to-text for tutor queries
- [ ] Predictive analytics for student success
- [ ] Blockchain-based certificates

---

## 👥 Contributors

- **Project Lead:** AI/ML Team - GLA University
- **Full Stack Development:** B.Tech AIML Students
- **Mentor:** Dr. [Professor Name]

---

## 📜 License

MIT License - See LICENSE file for details

---

## 📞 Support

- **Documentation:** Full API docs at `/api/docs`
- **Issues:** Create an issue on GitHub
- **Email:** support@ailearning.edu

---

## ✨ Highlights

🎯 **What Makes This Special:**
1. **Real AI Integration** - Not just mockups, actual ML-powered gap detection
2. **Fully Integrated** - Backend and frontend work seamlessly
3. **Production-Ready** - Security, error handling, best practices
4. **Scalable** - Database models support millions of students
5. **Beautiful UI** - Modern glassmorphism design
6. **Adaptive Learning** - Difficulty adjusts based on performance
7. **Real-time Feedback** - Instant results and recommendations

---

## 🎓 Academic Context

**Course:** B.Tech AIML Mini Project  
**Batch:** 2024-2025  
**University:** GLA University  
**Duration:** One Semester  
**Team Size:** 3-4 students  

**Evaluation Criteria:**
- ✅ Feature Completeness
- ✅ Code Quality & Architecture
- ✅ UI/UX Design
- ✅ Documentation
- ✅ Integration
- ✅ Security
- ✅ Performance

**Target Score:** 70-80+ marks

---

**Last Updated:** April 26, 2026  
**Version:** 2.0 (Production Ready)

- Dynamic concept sequencing  
- Personalized difficulty adjustment  
- Continuous mastery updates  

---

###  AI-Powered Recommendations

- Content ranking based on knowledge gaps  
- Hybrid ML + rule-based recommender  
- Personalized revision suggestions  

---

###  Smart Quiz Generator

- ML-based question difficulty classification  
- Weak-concept targeting  
- Personalized quiz creation  

---

###  TutorVoice (Conversational AI)

- Text-based AI assistant  
- Concept explanations  
- Learning path guidance  

---

###  NoteFlow

- AI-generated personalized notes  
- Concept flow summaries  

---

###  MemoryBoost

- Microlearning approach  
- Spaced repetition scheduling (1–3–7 day cycle)  

---

##  System Architecture\

---

##  Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | React.js, Tailwind CSS |
| Backend | Flask / FastAPI (Python) |
| Machine Learning | Scikit-learn, NumPy |
| NLP | GPT / BERT |
| Database | PostgreSQL / MongoDB |
| Knowledge Graph | Neo4j |
| Authentication | JWT + Google OAuth 2.0 |

---

---

##  Installation

###  Clone Repository

```bash
git clone https://github.com/your-username/ai-personalized-learning.git
cd ai-personalized-learning
cd backend
pip install -r requirements.txt
python app.py
cd frontend
npm install
npm start



