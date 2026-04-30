# 🎯 QUICK REFERENCE - ENVIRONMENT VARIABLES

## Copy-Paste Ready Templates

---

## 📝 BACKEND LOCAL DEVELOPMENT

**File: `backend/.env`**

```bash
ENVIRONMENT=development
DATABASE_URL=sqlite:///./learning_platform.db
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000
FRONTEND_URL=http://localhost:3000
JWT_SECRET=dev-secret-key-123
GOOGLE_API_KEY=AIzaSyDKw80_EeRTPbLLBoJYs_micDwp30wIoOI
FIREBASE_DATABASE_URL=https://driven-learning-platform-default-rtdb.asia-southeast1.firebasedatabase.app
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=INFO
```

**How to use:**
1. Open `backend/.env` in VS Code
2. Replace with above content
3. Save the file
4. Run: `cd backend && uvicorn main:app --reload`

---

## 📝 FRONTEND LOCAL DEVELOPMENT

**File: `frontend/.env.local`**

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_APP_NAME=AI Personalized Learning Platform
```

**How to use:**
1. Open `frontend/.env.local` in VS Code
2. Replace with above content
3. Save the file
4. Run: `cd frontend && npm run dev`

---

## 🚀 BACKEND PRODUCTION (RENDER)

**Where to set:** Render Dashboard → Your Service → Environment Variables

| Variable | Value | Example |
|----------|-------|---------|
| ENVIRONMENT | production | production |
| DATABASE_URL | PostgreSQL URL | postgresql://user:pass@host:5432/db |
| CORS_ORIGINS | Your frontend domain | https://ai-learning.vercel.app |
| FRONTEND_URL | Your frontend domain | https://ai-learning.vercel.app |
| JWT_SECRET | Strong random secret | Ab12Cd34Ef56Gh78Ij90Kl12Mn34Op56... |
| GOOGLE_API_KEY | Your Google API key | AIzaSyDKw80_EeRTPbLLBoJYs_micDwp... |
| FIREBASE_DATABASE_URL | Firebase URL | https://project.firebaseio.com |
| SERVER_HOST | 0.0.0.0 | 0.0.0.0 |
| SERVER_PORT | 8000 | 8000 |
| LOG_LEVEL | WARNING | WARNING |

**Complete Example for Render:**
```
ENVIRONMENT=production
DATABASE_URL=postgresql://learning_user:Abc123Def456@dpg-abc123.onrender.com:5432/learning_db
CORS_ORIGINS=https://ai-learning.vercel.app
FRONTEND_URL=https://ai-learning.vercel.app
JWT_SECRET=XYz789Uvw012Qrs345Txy678Uvm901Nop234
GOOGLE_API_KEY=AIzaSyDKw80_EeRTPbLLBoJYs_micDwp30wIoOI
FIREBASE_DATABASE_URL=https://driven-learning-platform-default-rtdb.asia-southeast1.firebasedatabase.app
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
LOG_LEVEL=WARNING
```

### Step-by-Step to Add Render Variables:

1. Go to: https://dashboard.render.com
2. Click your service "ai-learning-backend"
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. For each variable above:
   - Name: `ENVIRONMENT`
   - Value: `production`
   - Click "Save"
6. Service auto-redeploys

---

## 🎨 FRONTEND PRODUCTION (VERCEL)

**Where to set:** Vercel Dashboard → Your Project → Settings → Environment Variables

| Variable | Value | Example |
|----------|-------|---------|
| NEXT_PUBLIC_API_URL | Backend Render URL | https://ai-learning-backend.onrender.com |
| NEXT_PUBLIC_ENVIRONMENT | production | production |
| NEXT_PUBLIC_APP_NAME | App name | AI Personalized Learning Platform |

**Complete Example for Vercel:**
```
NEXT_PUBLIC_API_URL=https://ai-learning-backend.onrender.com
NEXT_PUBLIC_ENVIRONMENT=production
NEXT_PUBLIC_APP_NAME=AI Personalized Learning Platform
```

### Step-by-Step to Add Vercel Variables:

1. Go to: https://vercel.com
2. Click your project "ai-learning"
3. Go to "Settings"
4. Click "Environment Variables"
5. For each variable:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://ai-learning-backend.onrender.com`
   - Click "Save"
6. Click "Redeploy" to use new variables

---

## 🔐 GITHUB SECRETS

**Where to set:** GitHub → Settings → Secrets and variables → Actions

### All Secrets Needed:

```
Name: RENDER_API_KEY
Value: [Get from Render Account Settings → API Keys]

Name: RENDER_BACKEND_PRODUCTION_SERVICE_ID
Value: srv-abc123xyz [from your Render service URL]

Name: VERCEL_TOKEN
Value: [Get from Vercel Account Settings → Tokens]

Name: VERCEL_ORG_ID
Value: [Your Vercel organization ID]

Name: VERCEL_PROJECT_ID
Value: [Your Vercel project ID]
```

### Step-by-Step to Add GitHub Secrets:

1. Go to: https://github.com/nalin1012/mini-project-/settings/secrets/actions
2. Click "New repository secret"
3. For each secret:
   - Name: `RENDER_API_KEY`
   - Secret: [paste value]
   - Click "Add secret"
4. Repeat for all 5 secrets

---

## 🔑 HOW TO GET EACH VALUE

### JWT_SECRET (Generate Strong Secret)

**Windows PowerShell:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**macOS/Linux Terminal:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Output looks like:**
```
Ab12Cd34Ef56Gh78Ij90Kl12Mn34Op56Qr78St90
```

### DATABASE_URL (PostgreSQL from Render)

1. Go to https://dashboard.render.com
2. Click "PostgreSQL" (left sidebar)
3. Click your database
4. Copy "Internal Database URL"
5. Format: `postgresql://user:password@host:5432/database`

### RENDER_API_KEY

1. Go to https://dashboard.render.com
2. Click your username (bottom left)
3. Click "Account" → "API Keys"
4. Create new token
5. Copy the token

### RENDER_BACKEND_PRODUCTION_SERVICE_ID

1. Go to https://dashboard.render.com
2. Click your backend service
3. Look at URL bar: `render.com/services/srv-abc123xyz`
4. Copy `srv-abc123xyz` part

### VERCEL_TOKEN

1. Go to https://vercel.com
2. Click your profile (top right) → "Settings"
3. Click "Tokens"
4. Create new token
5. Copy token

### VERCEL_ORG_ID

1. Go to https://vercel.com/account/organizations
2. Click your organization
3. URL shows: `vercel.com/teams/org-id-here`
4. Copy the org-id part

### VERCEL_PROJECT_ID

1. Go to https://vercel.com
2. Click your project
3. Go to "Settings" → "General"
4. Find "Project ID"
5. Copy the ID

---

## ✅ VERIFICATION CHECKLIST

### Before Going to Production:

- [ ] Backend `.env` created with all variables
- [ ] Frontend `.env.local` created with API URL pointing to localhost
- [ ] Local development works (can register, login, use app)
- [ ] Render service created and environment variables set
- [ ] Vercel project created and environment variables set
- [ ] Backend URL verified working (`/api/health` responds)
- [ ] GitHub secrets added (5 total)
- [ ] GitHub Actions workflow visible and configured
- [ ] First git push triggers deployment
- [ ] Frontend loads without errors
- [ ] CORS errors are gone
- [ ] Can register and login in production
- [ ] All features working (quiz, tutor, progress)

---

## 🔄 ENVIRONMENT VARIABLE FLOW

```
┌─────────────────────────────────────────────────────────────┐
│  LOCAL DEVELOPMENT                                          │
│  ┌──────────────┐          ┌──────────────┐               │
│  │ backend/.env │          │ frontend/    │               │
│  │              │          │ .env.local   │               │
│  │ DATABASE_URL │          │              │               │
│  │ =sqlite      │          │ API_URL=     │               │
│  │ CORS=:3000   │          │ :8000        │               │
│  └──────────────┘          └──────────────┘               │
│         ↓                          ↓                        │
│  localhost:8000            localhost:3000                  │
└─────────────────────────────────────────────────────────────┘
              ↓                    ↓
              │                    │
    git push origin main           │
              ↓                    ↓
┌─────────────────────────────────────────────────────────────┐
│  GITHUB → ACTIONS PIPELINE                                  │
│  Test & Build                                               │
│  ↓                                                           │
│  Deploy                                                     │
└─────────────────────────────────────────────────────────────┘
              ↓                    ↓
    ┌─────────────────┐    ┌─────────────────┐
    │    RENDER       │    │    VERCEL       │
    │   Dashboard     │    │   Dashboard     │
    │                 │    │                 │
    │ Environment:    │    │ Environment:    │
    │ - DATABASE_URL  │    │ - API_URL=      │
    │ - CORS_ORIGINS  │    │   render.com    │
    │ - JWT_SECRET    │    │ - ENVIRONMENT   │
    │ - API_KEYS      │    │   =production   │
    └─────────────────┘    └─────────────────┘
              ↓                    ↓
        Render.com          Vercel.app (production)
```

---

## 🚨 COMMON MISTAKES TO AVOID

❌ **WRONG:**
```bash
# Putting secrets in frontend
NEXT_PUBLIC_JWT_SECRET=secret123  # Exposed to browser!
```

✅ **CORRECT:**
```bash
# Secrets only in backend
# .env file (not in git)
JWT_SECRET=secret123
```

---

❌ **WRONG:**
```bash
# Hardcoded API URL in code
const API_URL = "https://specific-backend.com"
```

✅ **CORRECT:**
```bash
# Use environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL
```

---

❌ **WRONG:**
```bash
# Same JWT secret everywhere
JWT_SECRET=dev-secret-123  # Used in all environments!
```

✅ **CORRECT:**
```bash
# Different secrets per environment
# Local: any string
# Production: strong random secret
JWT_SECRET=Abc123Def456Ghi789Jkl012Mno345Pqr678Stu901
```

---

❌ **WRONG:**
```bash
# Forgot to set CORS
CORS_ORIGINS=*  # Allows anyone to access
```

✅ **CORRECT:**
```bash
# Restrict to your frontend
CORS_ORIGINS=https://ai-learning.vercel.app
```

---

## 📞 QUICK TROUBLESHOOTING

| Problem | Check | Solution |
|---------|-------|----------|
| CORS error | Frontend API URL | Matches `NEXT_PUBLIC_API_URL` |
| 401 error | JWT Secret | Same on backend and in code |
| Database error | DATABASE_URL | Correct PostgreSQL connection string |
| Blank screen | Console errors (F12) | Check error messages |
| Deployment fails | GitHub logs | Check build error in Actions |

---

**Save this file for quick reference!** 📌
