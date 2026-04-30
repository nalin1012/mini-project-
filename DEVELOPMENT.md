# 🏗️ Development Environment Setup

## Prerequisites

- **Git** - [Download](https://git-scm.com)
- **Node.js v18+** - [Download](https://nodejs.org)
- **Python 3.11+** - [Download](https://python.org)
- **Docker** (optional) - [Download](https://docker.com)

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/nalin1012/mini-project-.git
cd mini-project-
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations (if needed)
# python -m alembic upgrade head

# Start backend server
uvicorn main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API Docs: http://localhost:8000/api/docs

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/api/docs
- **Backend ReDoc**: http://localhost:8000/api/redoc

---

## Backend Development

### Project Structure
```
backend/
├── main.py              # Entry point
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication routes
├── quiz.py              # Quiz routes
├── progress.py          # Progress tracking
├── users.py             # User management
├── notes.py             # Notes feature
├── chapters.py          # Chapter management
├── tutor.py             # AI Tutor routes
├── firebase_service.py  # Firebase integration
├── requirements.txt     # Dependencies
└── Dockerfile           # Container configuration
```

### Common Commands

```bash
# Run tests
pytest

# Run with auto-reload
uvicorn main:app --reload

# Run with specific host/port
uvicorn main:app --host 0.0.0.0 --port 8000

# Generate requirements
pip freeze > requirements.txt

# Add new package
pip install package-name
pip freeze > requirements.txt
```

### Database Operations

```bash
# Initialize database
python -c "from database import init_db; init_db()"

# Access database directly (SQLite)
sqlite3 learning_platform.db

# Query users
SELECT * FROM users;
```

---

## Frontend Development

### Project Structure
```
frontend/
├── app/
│   ├── page.tsx              # Home page
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles
│   ├── login/
│   ├── register/
│   ├── dashboard/
│   ├── subjects/
│   ├── learning/[subject]/
│   ├── quiz/
│   ├── results/
│   ├── admin/
│   └── profile/
├── components/
│   ├── ui/                   # UI components (Shadcn)
│   ├── login-form.tsx
│   ├── dashboard-navbar.tsx
│   ├── AIChatTutor.tsx
│   └── error-boundary.tsx
├── lib/
│   ├── api-config.ts         # API configuration
│   ├── error-handler.ts      # Error handling
│   ├── utils.ts
│   └── id-generator.ts
├── hooks/
│   └── use-toast.ts
└── package.json
```

### Common Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production build locally
npm start

# Run linter
npm run lint

# Install new package
npm install package-name
```

---

## Using Docker (Optional)

### Start All Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild Images
```bash
docker-compose up -d --build
```

---

## Git Workflow

### Feature Branch Development
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# After review, merge to develop branch
```

### Deployment Branches
- **develop**: Staging/development deployments
- **main**: Production deployments

---

## Useful Tools

### VSCode Extensions
- ES7+ React/Redux/React-Native snippets
- Python
- Pylance
- Thunder Client (or Postman)
- REST Client

### VSCode Settings
Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

### Testing API Endpoints

**Using Thunder Client/Postman:**
1. Create new request
2. Set method (GET, POST, etc.)
3. Set URL: `http://localhost:8000/api/endpoint`
4. Add headers: `Content-Type: application/json`
5. Add body (for POST/PUT requests)
6. Send request

**Using curl:**
```bash
# GET request
curl http://localhost:8000/api/endpoint

# POST request
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# With authorization token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/protected-endpoint
```

---

## Environment Variables

### Backend (.env)
```bash
ENVIRONMENT=development
DATABASE_URL=sqlite:///./learning_platform.db
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
JWT_SECRET=your-dev-secret
GOOGLE_API_KEY=your-google-key
FIREBASE_DATABASE_URL=your-firebase-url
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## Debugging

### Backend Debugging

**Using VSCode:**
1. Install Python extension
2. Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

### Frontend Debugging

**Using Browser DevTools:**
1. Press F12 in browser
2. Use Console tab for errors
3. Use Network tab to inspect API calls
4. Use Sources tab to set breakpoints

**Using VSCode:**
1. Install "Debugger for Chrome" extension
2. Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Next.js",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend",
      "sourceMapPathOverride": {
        "*": "${webRoot}/*"
      }
    }
  ]
}
```

---

## Troubleshooting

### Backend Issues

**ImportError: No module named 'main'**
- Make sure you're running from the backend directory
- Activate virtual environment

**Port 8000 already in use**
```bash
# Find and kill process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

**Database errors**
- Delete `learning_platform.db` and restart
- Re-run database initialization

### Frontend Issues

**Port 3000 already in use**
```bash
# Use different port
npm run dev -- -p 3001
```

**npm install fails**
```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API calls fail**
- Check backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check browser console for CORS errors

---

## Performance Optimization Tips

### Backend
- Use database indexes for frequently queried fields
- Cache frequently accessed data
- Implement pagination for list endpoints
- Use async functions where possible

### Frontend
- Implement lazy loading for images
- Use React.memo for expensive components
- Optimize bundle size with dynamic imports
- Use server-side rendering where applicable

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org)
- [React Best Practices](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)

---

**Happy Coding! 🚀**
