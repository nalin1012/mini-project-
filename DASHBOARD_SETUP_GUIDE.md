# 📊 DASHBOARD SETUP VISUAL GUIDE

## Step-by-Step Screenshots & Instructions

---

## 🔴 RENDER BACKEND SETUP

### Step 1: Go to Render Dashboard
```
1. Visit: https://dashboard.render.com
2. Login with GitHub
3. You should see an empty dashboard
```

### Step 2: Create Web Service
```
Dashboard screen shows:
┌─────────────────────────────────────┐
│ Render                              │
│ New +    Services    Env Vars       │
├─────────────────────────────────────┤
│                                     │
│     Click: "New +" (top left)       │
│                                     │
│     Select: "Web Service"           │
│                                     │
│     Connect: "mini-project-"        │
│                                     │
└─────────────────────────────────────┘
```

### Step 3: Configure Service
```
Form shows:
┌─────────────────────────────────────┐
│ Create a new Web Service            │
├─────────────────────────────────────┤
│ Name: ai-learning-backend           │
│ Environment: Python 3               │
│ Region: Oregon                      │
│ Branch: main                        │
│ Runtime: Python 3.11                │
│ Root Directory: backend             │
│                                     │
│ Build Command:                      │
│ pip install -r requirements.txt     │
│                                     │
│ Start Command:                      │
│ uvicorn main:app --host 0.0.0.0 \  │
│ --port 8000                         │
│                                     │
│ [Create Web Service]                │
└─────────────────────────────────────┘
```

### Step 4: Add Environment Variables
```
After service created, click "Environment" tab:

┌─────────────────────────────────────────────────┐
│ Environment Variables                           │
├─────────────────────────────────────────────────┤
│                                                 │
│ [Add Environment Variable] button               │
│                                                 │
│ Click to add each variable:                     │
│                                                 │
│ 1. Name: ENVIRONMENT                           │
│    Value: production                           │
│    [Save]                                       │
│                                                 │
│ 2. Name: DATABASE_URL                          │
│    Value: postgresql://user:pass@host:5432/db  │
│    [Save]                                       │
│                                                 │
│ 3. Name: CORS_ORIGINS                          │
│    Value: https://ai-learning.vercel.app       │
│    [Save]                                       │
│                                                 │
│ (Continue for all variables...)                │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Step 5: Monitor Deployment
```
Click "Events" tab:

┌─────────────────────────────────────┐
│ Events                              │
├─────────────────────────────────────┤
│ ✓ Build started                     │
│ ✓ Cloning repository...             │
│ ✓ Installing dependencies...        │
│ ✓ Build succeeded                   │
│ ✓ Deployment live!                  │
│                                     │
│ Your URL:                           │
│ https://ai-learning-backend.        │
│ onrender.com                        │
└─────────────────────────────────────┘
```

### Step 6: Get Your Backend URL
```
Copy this URL from Render dashboard:
https://ai-learning-backend.onrender.com

You'll need this for:
1. Vercel environment variables
2. Local testing
3. CORS configuration
```

---

## 🟢 VERCEL FRONTEND SETUP

### Step 1: Go to Vercel Dashboard
```
1. Visit: https://vercel.com
2. Login with GitHub
3. Click "Add New..." (top)
```

### Step 2: Import Repository
```
┌─────────────────────────────────────┐
│ Add New                             │
├─────────────────────────────────────┤
│ Select: "Project"                   │
│ Click: "Continue with GitHub"       │
│ Search: "mini-project-"             │
│ Click: "Import"                     │
└─────────────────────────────────────┘
```

### Step 3: Configure Project
```
┌──────────────────────────────────────────┐
│ Configure Project                        │
├──────────────────────────────────────────┤
│ Project Name:    ai-learning             │
│ Framework:       Next.js                 │
│ Root Directory:  frontend                │
│                                          │
│ Build Settings:                          │
│ Build Command:   npm run build           │
│ Output Directory: .next                  │
│ Install Command: npm ci                  │
│                                          │
│ [Configure Production Environment]       │
│ (click to set environment variables)     │
└──────────────────────────────────────────┘
```

### Step 4: Add Environment Variables
```
When prompted for Environment Variables:

┌────────────────────────────────────────────┐
│ Environment Variables                      │
├────────────────────────────────────────────┤
│                                            │
│ Name: NEXT_PUBLIC_API_URL                  │
│ Value: https://ai-learning-backend.       │
│        onrender.com                        │
│ [Add]                                      │
│                                            │
│ Name: NEXT_PUBLIC_ENVIRONMENT              │
│ Value: production                          │
│ [Add]                                      │
│                                            │
│ Name: NEXT_PUBLIC_APP_NAME                 │
│ Value: AI Personalized Learning Platform   │
│ [Add]                                      │
│                                            │
└────────────────────────────────────────────┘
```

### Step 5: Deploy
```
Click "Deploy":

┌─────────────────────────────────────┐
│ Deploying...                        │
├─────────────────────────────────────┤
│ ✓ Build started                     │
│ ✓ Installing dependencies...        │
│ ✓ Building Next.js app...           │
│ ✓ Build succeeded                   │
│ ✓ Deployment complete!              │
│                                     │
│ Your URL:                           │
│ https://ai-learning.vercel.app      │
└─────────────────────────────────────┘
```

### Step 6: Get Your Frontend URL
```
Copy this URL from Vercel dashboard:
https://ai-learning.vercel.app

You'll need this for:
1. Render CORS_ORIGINS
2. User access
3. Marketing materials
```

---

## 🔵 GITHUB SECRETS SETUP

### Step 1: Go to Repository Settings
```
1. Go to: github.com/nalin1012/mini-project-
2. Click "Settings" (top right)
3. Click "Secrets and variables" (left sidebar)
4. Click "Actions"
```

### Step 2: Add Secrets Interface
```
┌────────────────────────────────────────────┐
│ GitHub Repository Secrets                  │
├────────────────────────────────────────────┤
│                                            │
│ [New repository secret] button (top right) │
│                                            │
│ Click to add each secret:                  │
│                                            │
└────────────────────────────────────────────┘
```

### Step 3: Add Each Secret
```
For RENDER_API_KEY:

┌────────────────────────────────────────────┐
│ New Secret                                 │
├────────────────────────────────────────────┤
│                                            │
│ Name: RENDER_API_KEY                       │
│ Secret: [paste API key from Render]        │
│                                            │
│ [Add secret]                               │
│                                            │
└────────────────────────────────────────────┘

Then repeat for:
- RENDER_BACKEND_PRODUCTION_SERVICE_ID
- VERCEL_TOKEN
- VERCEL_ORG_ID
- VERCEL_PROJECT_ID
```

### Step 4: Verify All Secrets Added
```
┌────────────────────────────────────────────┐
│ Repository Secrets                         │
├────────────────────────────────────────────┤
│ ✓ RENDER_API_KEY                           │
│ ✓ RENDER_BACKEND_PRODUCTION_SERVICE_ID     │
│ ✓ VERCEL_TOKEN                             │
│ ✓ VERCEL_ORG_ID                            │
│ ✓ VERCEL_PROJECT_ID                        │
│                                            │
│ All 5 secrets are set!                     │
└────────────────────────────────────────────┘
```

---

## 📋 COMPLETE DEPLOYMENT WORKFLOW

### Day 1: Initial Setup

```
MORNING:
├─ Create Render account
├─ Create backend service
├─ Add PostgreSQL database
├─ Set environment variables
└─ Wait for deployment (5-10 min)

AFTERNOON:
├─ Create Vercel account
├─ Import frontend project
├─ Set environment variables
└─ Wait for deployment (2-3 min)

EVENING:
├─ Update Render CORS with Vercel URL
├─ Test API endpoints
├─ Create GitHub secrets
└─ Verify everything works ✓
```

### Day 2: Testing

```
MORNING:
├─ Open frontend in browser
├─ Test registration
├─ Test login
├─ Test all features
└─ Check logs for errors

AFTERNOON:
├─ Monitor GitHub Actions
├─ Make small code change
├─ Push to main
├─ Verify auto-deployment
└─ Check both dashboards
```

### Day 3: Go Live

```
MORNING:
├─ Final security review
├─ Check all environment variables
├─ Verify HTTPS enabled
└─ Check error handling

AFTERNOON:
├─ Announce to users
├─ Monitor dashboards
├─ Handle user feedback
└─ All set! 🎉
```

---

## 🎯 QUICK ACCESS LINKS

**Always keep these bookmarked:**

```
Development:
├─ Frontend Local: http://localhost:3000
├─ Backend Local: http://localhost:8000
├─ Backend Docs: http://localhost:8000/api/docs
└─ GitHub Repo: github.com/nalin1012/mini-project-

Production:
├─ Frontend: https://ai-learning.vercel.app
├─ Backend: https://ai-learning-backend.onrender.com
├─ Backend Health: https://ai-learning-backend.onrender.com/api/health
└─ GitHub Repo: github.com/nalin1012/mini-project-

Dashboards:
├─ Render: dashboard.render.com
├─ Vercel: vercel.com
├─ GitHub: github.com/nalin1012/mini-project-/settings/secrets/actions
└─ GitHub Actions: github.com/nalin1012/mini-project-/actions
```

---

## ✅ SETUP COMPLETION CHECKLIST

### Before you start:
- [ ] Have GitHub account logged in
- [ ] Have Render account created
- [ ] Have Vercel account created
- [ ] Have environment variables ready (see reference guide)

### Backend Setup:
- [ ] Render service created
- [ ] PostgreSQL database created
- [ ] All environment variables set
- [ ] Deployment shows "live"
- [ ] Health check passes

### Frontend Setup:
- [ ] Vercel project imported
- [ ] All environment variables set
- [ ] Deployment shows "ready"
- [ ] Can access frontend URL

### Integration:
- [ ] Backend CORS updated with frontend URL
- [ ] Frontend can reach backend
- [ ] No console errors
- [ ] Can register/login

### GitHub Actions:
- [ ] All 5 secrets added
- [ ] Workflow file exists (`.github/workflows/ci-cd.yml`)
- [ ] Test push to main triggers deployment
- [ ] Deployment succeeds

### Final Verification:
- [ ] Open production frontend
- [ ] Test full user flow
- [ ] Check backend logs (Render)
- [ ] Check frontend logs (Vercel)
- [ ] All working perfectly ✓

---

## 🚀 WHAT'S NEXT?

After successful deployment:

1. **Monitor** dashboards weekly
2. **Update** dependencies monthly
3. **Backup** database regularly
4. **Scale** if needed (upgrade plans)
5. **Optimize** based on user feedback

---

**Congratulations on setting up production! 🎉**

Your AI Learning Platform is now:
- ✅ Live on the internet
- ✅ Automatically deploying on code changes
- ✅ Scalable for growth
- ✅ Secure with proper environment management
- ✅ Monitored for issues

**Share with your team!**
