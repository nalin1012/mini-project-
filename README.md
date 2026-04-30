# 🎓 AI-Powered Personalized Learning Platform

An intelligent full-stack EdTech system that detects knowledge gaps and delivers personalized, adaptive learning experiences powered by **AI, Machine Learning, and Real-time Analytics**.

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.1+-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-4.0+-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Version:** 2.1 (Production Ready) | **Last Updated:** April 27, 2026

---

## 📋 Table of Contents

- [🎯 Problem Statement](#-problem-statement)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [🔄 API Endpoints](#-api-endpoints)
- [📊 Database Schema](#-database-schema)
- [🧪 Testing](#-testing)
- [📱 Usage Guide](#-usage-guide)
- [🎨 UI/UX Design](#-uiux-design)
- [🔐 Security Features](#-security-features)
- [📈 Performance](#-performance)
- [🚀 Deployment](#-deployment)
- [📚 Future Roadmap](#-future-roadmap)
- [👥 Team & Support](#-team--support)

### New in v2.1
- ✅ Comprehensive logging system for debugging
- ✅ Enhanced database connection pooling
- ✅ Improved error handling in authentication
- ✅ Admin authorization security enhancements
- ✅ Caching optimization for user endpoints
- ✅ Expanded quiz bank with explanations and difficulty levels

---

## 🎯 Problem Statement

Traditional educational platforms use a **one-size-fits-all approach** and fail to:
- ❌ Identify concept-level knowledge gaps
- ❌ Adapt to individual learning pace
- ❌ Provide intelligent recommendations
- ❌ Track misconceptions dynamically
- ❌ Offer real-time, personalized guidance

**✅ Our Solution:** An AI-powered platform that:
- **Analyzes** student performance in real-time
- **Detects** knowledge gaps automatically
- **Recommends** personalized learning paths
- **Adapts** difficulty based on performance
- **Provides** instant feedback and guidance via AI Tutor

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
- Minimum 8 characters recommended
- Never stored in plain text
- Secure password reset workflow

✅ **Authentication & Authorization**
- JWT tokens with 30-day expiration
- HTTP-only cookie support
- Bearer token validation
- Role-based access control (Student/Teacher/Admin)

✅ **Data Validation & Protection**
- Pydantic schemas on all endpoints
- Email format validation
- Type checking and serialization
- XSS and CSRF protection ready

✅ **API Security**
- CORS middleware properly configured
- SQL Injection prevention via SQLAlchemy ORM
- Rate limiting infrastructure (ready to enable)
- Input sanitization on all endpoints
- Secure headers configuration

---

## 📈 Performance & Optimization

### Frontend Optimizations
- **Client-side Caching:** localStorage for user preferences and tokens
- **Code Splitting:** Dynamic imports for route-based code splitting
- **Image Optimization:** Next.js Image component for auto-optimization
- **CSS Optimization:** Tailwind CSS with tree-shaking
- **Lazy Loading:** Components load on-demand

### Backend Optimizations
- **Database Indexing:** Optimized queries on frequently accessed fields
- **Response Pagination:** Ready for large datasets
- **Async Processing:** FastAPI async/await for I/O operations
- **Caching Strategy:** Redis-ready (can be integrated)
- **Query Optimization:** SQLAlchemy relationship loading strategies

### Monitoring & Logging
- Structured logging for debugging
- Error tracking and reporting
- Performance metrics collection
- User activity audit logs

---

## 🌐 API Endpoints Summary

### Authentication (5 endpoints)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login with JWT
- `GET /api/auth/me` - Retrieve current user profile
- `POST /api/auth/logout` - Clear session
- `POST /api/auth/refresh` - Refresh JWT token

### Quiz Management (4 endpoints)
- `GET /api/quiz/generate/{subject}/{topic}` - Generate adaptive quiz
- `POST /api/quiz/submit-answer` - Submit quiz answer
- `GET /api/quiz/stats` - Retrieve user statistics
- `GET /api/quiz/history` - Get quiz attempt history

### Knowledge Gap Detection (5 endpoints)
- `GET /api/knowledge-gap/detect` - Detect weak areas
- `GET /api/knowledge-gap/progress/{topic}` - Topic-specific progress
- `GET /api/knowledge-gap/dashboard-summary` - Dashboard statistics
- `POST /api/knowledge-gap/mark-mastered/{topic}` - Mark topic complete
- `GET /api/knowledge-gap/weak-areas` - List all weak areas

### AI Tutor (4 endpoints)
- `POST /api/tutor/ask` - Ask tutor a question
- `GET /api/tutor/topics` - Available topics list
- `GET /api/tutor/explain/{topic}` - Topic explanation
- `POST /api/tutor/practice-hint/{topic}` - Get practice hints

### Recommendations (3 endpoints)
- `GET /api/recommendations/analyze/{concept}` - Performance analysis
- `GET /api/recommendations/personalized/{user_id}` - Custom recommendations
- `GET /api/recommendations/next-topics` - Suggested topics

### General (3 endpoints)
- `GET /` - API health check
- `GET /api/health` - Detailed health status
- `GET /api/subjects` - All available subjects

**Total: 24+ REST API Endpoints**

---

## 🚀 Deployment

### Backend Deployment Options

**Option 1: Heroku**
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

**Option 2: Railway / Render**
```bash
# Connect GitHub repository
# Configure environment variables
# Deploy with one click
```

**Option 3: Docker**
```bash
docker build -t learning-platform-api .
docker run -p 8001:8001 learning-platform-api
```

### Frontend Deployment Options

**Option 1: Vercel (Recommended for Next.js)**
```bash
npm install -g vercel
vercel deploy
```

**Option 2: Netlify**
```bash
npm run build
netlify deploy --prod --dir=.next
```

**Option 3: Docker**
```bash
docker build -t learning-platform-web .
docker run -p 3000:3000 learning-platform-web
```

### Production Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=your-production-secret-key-min-32-chars
ENVIRONMENT=production
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

**Frontend (.env.production)**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_NAME=Learning Platform
```

### Pre-deployment Checklist
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] API documentation updated
- [ ] Security headers configured
- [ ] SSL/TLS certificates installed
- [ ] Monitoring and logging setup
- [ ] Backup strategy in place

---

## 📚 Future Roadmap

### Phase 1 (Current)
- ✅ Core platform with quiz and gap detection
- ✅ AI Tutor chatbot
- ✅ Dashboard with analytics
- ✅ User authentication

### Phase 2 (Planned)
- [ ] Advanced ML model with improved accuracy
- [ ] Video content for topics
- [ ] Real-time collaboration features
- [ ] Student progress export (PDF/CSV)
- [ ] Mobile-responsive optimizations

### Phase 3 (Backlog)
- [ ] Gamification (badges, leaderboards, XP system)
- [ ] Live instructor support
- [ ] Integration with LMS (Moodle, Canvas, Blackboard)
- [ ] Blockchain-based certificates
- [ ] Advanced analytics for teachers
- [ ] Speech-to-text tutor interaction
- [ ] Predictive success analytics
- [ ] React Native mobile app

### Long-term Vision
- [ ] Multi-language support
- [ ] AI-generated video explanations
- [ ] Community learning forum
- [ ] Peer tutoring system
- [ ] Parent dashboard
- [ ] Integration with textbook publishers

---

## 👥 Team & Support

### Project Information
- **Course:** B.Tech AIML Mini Project
- **University:** GLA University
- **Academic Year:** 2024-2025
- **Team Size:** 3-4 students
- **Duration:** One Semester
- **Mentor:** Faculty Guide

### Evaluation Metrics
- ✅ Feature Completeness (25%)
- ✅ Code Quality & Architecture (20%)
- ✅ UI/UX Design (15%)
- ✅ API Integration (15%)
- ✅ Security Implementation (10%)
- ✅ Documentation (10%)
- ✅ Performance Optimization (5%)

### Getting Help

| Resource | Link |
|----------|------|
| **API Documentation** | `http://localhost:8001/api/docs` (Swagger UI) |
| **Alternative API Docs** | `http://localhost:8001/api/redoc` (ReDoc) |
| **GitHub Issues** | [Create an issue](../../issues) |
| **Documentation** | [See QUICK_START.md](QUICK_START.md) |
| **API Reference** | [See API_REFERENCE.md](API_REFERENCE.md) |

### Common Commands

```bash
# Backend
cd backend && python main.py                  # Start backend
python -m pytest test_api.py -v             # Run tests
pip install -r requirements.txt             # Install dependencies

# Frontend
cd frontend && npm run dev                   # Start dev server
npm run build                               # Production build
npm run lint                                # Check code style
```

---

## 📄 License & Attribution

**License:** MIT License  
See [LICENSE](LICENSE) file for full details

**This project uses:**
- FastAPI (BSD)
- Next.js (MIT)
- Tailwind CSS (MIT)
- SQLAlchemy (MIT)
- And other open-source libraries (see requirements.txt)

---

## ✨ Key Highlights

| Feature | Benefit |
|---------|---------|
| **Real AI Integration** | Not mockups - actual ML-powered gap detection |
| **Fully Integrated** | Seamless backend-frontend integration |
| **Production-Ready** | Security, error handling, best practices |
| **Scalable Architecture** | Support for millions of students |
| **Beautiful UI** | Modern glassmorphism design |
| **Adaptive Learning** | Difficulty adjusts based on performance |
| **Real-time Feedback** | Instant results and personalized recommendations |

---

## 📊 Quick Stats

- **24+** REST API Endpoints
- **8** Core Database Models
- **5** Main Frontend Pages
- **3+** User Roles (Student, Teacher, Admin)
- **8** Learning Subjects
- **50+** Default Quiz Questions
- **100%** TypeScript + Async Backend
- **0** Third-party quiz services

---

## 🎓 Learning Outcomes

By completing this project, students have learned:
- Full-stack web development (frontend & backend)
- REST API design and implementation
- Database modeling and SQL optimization
- Authentication and security best practices
- Machine learning integration
- UI/UX design principles
- DevOps and deployment strategies
- Testing and debugging
- Project management and documentation

---

**Made with ❤️ by the GLA University AIML Team**

Last Updated: **April 26, 2026**  
Version: **2.0** | Status: **Production Ready** ✅

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



