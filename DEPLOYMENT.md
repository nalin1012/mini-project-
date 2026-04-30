# 🚀 AI Learning Platform - Production Deployment Guide

## Table of Contents
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Backend Deployment](#backend-deployment)
- [Frontend Deployment](#frontend-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Local Development with Docker

```bash
# Clone the repository
git clone https://github.com/nalin1012/mini-project-.git
cd mini-project-

# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

---

## Prerequisites

### Required Tools
- **Git** - Version control
- **Docker & Docker Compose** - Containerization (optional but recommended)
- **Node.js** - v18 or later (for frontend development)
- **Python** - v3.11 (for backend development)
- **GitHub Account** - For CI/CD pipeline
- **Render Account** - For backend deployment
- **Vercel Account** - For frontend deployment

### GitHub Repository Setup
1. Create a new repository on GitHub
2. Add your GitHub username to the `.github/workflows/ci-cd.yml` file
3. Configure repository secrets (see CI/CD section)

---

## Environment Setup

### 1. Backend Environment Variables

#### Local Development (`.env`)
```bash
ENVIRONMENT=development
DATABASE_URL=sqlite:///./learning_platform.db
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
FRONTEND_URL=http://localhost:3000
JWT_SECRET=your-secret-key-for-dev
GOOGLE_API_KEY=your-google-api-key
FIREBASE_DATABASE_URL=your-firebase-url
```

#### Production (Set in Render Dashboard)
```bash
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@host:5432/db
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
FRONTEND_URL=https://your-domain.com
JWT_SECRET=generate-strong-random-secret
GOOGLE_API_KEY=your-google-api-key
FIREBASE_DATABASE_URL=your-firebase-url
```

**Generate a Strong JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Frontend Environment Variables

#### Development (`.env.local`)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_APP_NAME=AI Personalized Learning Platform
```

#### Production (Set in Vercel Dashboard)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_APP_NAME=AI Personalized Learning Platform
```

⚠️ **Important:** Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Never put secrets in these variables.

---

## Backend Deployment

### Option 1: Deploy to Render (Recommended for beginners)

#### Step 1: Prepare the Backend
```bash
# Ensure requirements.txt is up to date
cd backend
pip freeze > requirements.txt
cd ..

# Commit changes
git add .
git commit -m "Update requirements for production"
git push origin main
```

#### Step 2: Create Render Service
1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Create new **Web Service**
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: ai-learning-backend
   - **Environment**: Python 3
   - **Region**: Oregon (or closest to you)
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - **Root Directory**: backend

#### Step 3: Add Environment Variables
In Render Dashboard → Environment:
```
ENVIRONMENT=production
DATABASE_URL=postgresql://[generated-by-render]
JWT_SECRET=[generate-strong-secret]
CORS_ORIGINS=https://your-vercel-domain.com
FRONTEND_URL=https://your-vercel-domain.com
GOOGLE_API_KEY=[your-key]
FIREBASE_DATABASE_URL=[your-url]
```

#### Step 4: Deploy
- Render will auto-deploy on push to main branch
- Monitor deployment in Render Dashboard
- Get your backend URL (e.g., `https://ai-learning-backend.onrender.com`)

### Option 2: Deploy with Docker to Railway, DigitalOcean, or AWS

```bash
# Build Docker image
docker build -t ai-learning-backend:latest ./backend

# Tag for registry
docker tag ai-learning-backend:latest your-registry/ai-learning-backend:latest

# Push to registry
docker push your-registry/ai-learning-backend:latest

# Deploy using your platform's CLI or dashboard
```

---

## Frontend Deployment

### Deploy to Vercel (Recommended)

#### Step 1: Prepare the Frontend
```bash
cd frontend
npm install
npm run build

# Test production build locally
npm run start

cd ..
git add .
git commit -m "Prepare frontend for production"
git push origin main
```

#### Step 2: Create Vercel Project
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Select your repository
5. Configure:
   - **Framework**: Next.js
   - **Root Directory**: frontend
   - **Build Command**: npm run build
   - **Output Directory**: .next

#### Step 3: Add Environment Variables
In Vercel Dashboard → Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_APP_NAME=AI Personalized Learning Platform
```

#### Step 4: Deploy
- Vercel will auto-deploy on push to main branch
- Get your frontend URL (e.g., `https://ai-learning.vercel.app`)

#### Step 5: Update Backend CORS
After getting your frontend URL, update backend CORS_ORIGINS:
```bash
# In Render Dashboard or your hosting platform
CORS_ORIGINS=https://your-vercel-domain.vercel.app,https://your-custom-domain.com
```

---

## CI/CD Pipeline

### GitHub Actions Setup

The CI/CD pipeline is configured in `.github/workflows/ci-cd.yml` and runs:
1. **On every push to main/develop**
2. **On every pull request**

#### Configure GitHub Secrets

Go to Repository Settings → Secrets and add:

```
RENDER_API_KEY=[from-render-dashboard]
RENDER_BACKEND_PRODUCTION_SERVICE_ID=[your-service-id]
RENDER_BACKEND_STAGING_SERVICE_ID=[your-staging-service-id]

VERCEL_TOKEN=[from-vercel-settings]
VERCEL_ORG_ID=[your-org-id]
VERCEL_PROJECT_ID=[your-project-id]
```

#### Pipeline Stages

1. **Tests** (Runs on all branches)
   - Backend tests with pytest
   - Frontend linting and build
   - Security scanning

2. **Staging Deployment** (Runs on develop branch)
   - Automated deployment to staging environment
   - Run integration tests

3. **Production Deployment** (Runs on main branch)
   - Automated deployment to production
   - Requires manual approval (optional)

### Manual Deployment

If CI/CD fails or you need manual control:

```bash
# Backend
git push origin main  # Render auto-deploys

# Frontend
git push origin main  # Vercel auto-deploys
```

---

## Monitoring & Maintenance

### 1. Monitor Application Health

**Backend Health Check:**
```bash
curl https://your-backend-url/api/health
```

**Frontend Performance:**
- Use Vercel Analytics Dashboard
- Monitor error rates and page performance

### 2. View Logs

**Render Backend Logs:**
- Render Dashboard → Services → ai-learning-backend → Logs

**Vercel Frontend Logs:**
- Vercel Dashboard → Deployments → Select deployment → View logs

### 3. Database Maintenance

**PostgreSQL Backups (if using):**
```bash
# Render handles automatic daily backups
# Access in Render Dashboard → Database → Backups
```

**SQLite Backups (development):**
```bash
cp backend/learning_platform.db backend/learning_platform.db.backup
```

### 4. Update Dependencies

```bash
# Backend
cd backend
pip list --outdated
pip install -U package-name
pip freeze > requirements.txt

# Frontend
cd ../frontend
npm update
npm audit fix

git add .
git commit -m "Update dependencies"
git push origin main
```

---

## Troubleshooting

### Common Issues

#### 1. CORS Errors
**Error:** `Access to XMLHttpRequest at 'backend-url' blocked by CORS policy`

**Solution:**
```bash
# Check CORS_ORIGINS in backend environment
# Should include your frontend domain
CORS_ORIGINS=https://your-frontend-url.com

# Restart backend after updating
```

#### 2. 401 Unauthorized Errors
**Problem:** User redirected to login immediately

**Solution:**
```bash
# Check JWT_SECRET is same on backend
# Clear browser localStorage
# Try login again
```

#### 3. API Connection Timeout
**Error:** `Unable to connect to server`

**Solution:**
```bash
# Verify backend is running
curl https://your-backend-url/api/health

# Check NEXT_PUBLIC_API_URL in frontend
# Should not have trailing slash
```

#### 4. Database Errors

**PostgreSQL Connection Error:**
```bash
# Verify DATABASE_URL format:
# postgresql://user:password@host:port/database

# Test connection:
psql postgresql://user:password@host:port/database
```

#### 5. Build Failures

**Frontend Build Fails:**
```bash
# Clear cache and rebuild
rm -rf frontend/.next
rm -rf frontend/node_modules
npm ci
npm run build
```

**Backend Import Errors:**
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

### Performance Optimization

1. **Enable Compression**
   - Render: Automatic
   - Vercel: Automatic

2. **Database Indexing**
   ```sql
   CREATE INDEX idx_user_email ON users(email);
   CREATE INDEX idx_quiz_score ON quiz_results(score);
   ```

3. **API Response Caching**
   - Configure in frontend with React Query or SWR
   - Backend: Use Redis (if available on hosting)

---

## Security Checklist

- [ ] JWT_SECRET is strong and random
- [ ] Database credentials are secure
- [ ] API keys are not in git
- [ ] CORS_ORIGINS is restricted (not "*")
- [ ] HTTPS is enabled on both frontend and backend
- [ ] Environment-specific .env files are not committed
- [ ] Database backups are configured
- [ ] Error messages don't expose sensitive info
- [ ] Rate limiting is implemented (optional)
- [ ] Regular security updates for dependencies

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs
- **GitHub Actions**: https://github.com/features/actions

---

## Rollback Procedure

### If Production Breaks

**Frontend Rollback (Vercel):**
1. Go to Deployments
2. Select previous stable deployment
3. Click "Redeploy"

**Backend Rollback (Render):**
1. Go to Services
2. Find your service
3. Click Deploy History
4. Select previous version and redeploy

---

**Last Updated:** 2024
**Version:** 2.0
