# 🎯 CRITICAL RENDER DEPLOYMENT SETUP GUIDE

## ⚠️ THE DEPLOYMENT ERROR YOU'RE SEEING

```
OperationalError: failed to resolve host 'host'
```

**Root Cause:** DATABASE_URL environment variable is NOT set on Render

**Why it happens:** The render.yaml file doesn't automatically set DATABASE_URL - you MUST do it manually in the Render dashboard.

---

## 📋 STEP-BY-STEP RENDER DEPLOYMENT

### STEP 1: Create PostgreSQL Database on Render (5 minutes)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in details:
   - **Name:** `learning-platform-db`
   - **Database:** `learning_db`
   - **User:** `learning_user`
   - **Region:** Select your region
   - **Plan:** Free (or paid if you want more power)
4. Click **"Create Database"**
5. **WAIT** for database to be created (usually 1-2 minutes)
6. Once created, you'll see a screen with connection details

### STEP 2: Copy Database URL (2 minutes)

1. In Render PostgreSQL dashboard, look for **"Internal Database URL"**
2. It looks like:
   ```
   postgresql://learning_user:password123@dpg-abc123.onrender.com:5432/learning_db
   ```
3. **COPY THIS URL** (you'll need it in the next step)

### STEP 3: Create Web Service on Render (5 minutes)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. **Connect to GitHub:**
   - Select your **mini-project-** repository
   - Branch: `main`
4. **Configure Web Service:**
   - **Name:** `ai-learning-backend`
   - **Runtime:** `Python 3`
   - **Region:** Same as database above
   - **Plan:** Free (or paid)
5. **Build Command:** (should be pre-filled)
   ```
   pip install --upgrade pip && pip install -r requirements.txt
   ```
6. **Start Command:** (should be pre-filled)
   ```
   cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   OR
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
7. **Root Directory:** `backend`
8. Click **"Create Web Service"**

### STEP 4: Add Environment Variables (5 minutes) ⚠️ CRITICAL

1. Your web service will start deploying (don't worry if it fails)
2. In the service dashboard, scroll down to **"Environment"**
3. Click **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `ENVIRONMENT` | `production` |
| `DATABASE_URL` | **(PASTE THE URL FROM STEP 2)** |
| `JWT_SECRET` | Generate new: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `GOOGLE_API_KEY` | Your Google API key |
| `FIREBASE_DATABASE_URL` | Your Firebase URL |
| `CORS_ORIGINS` | `https://your-frontend.vercel.app` |
| `FRONTEND_URL` | `https://your-frontend.vercel.app` |
| `SERVER_HOST` | `0.0.0.0` |
| `SERVER_PORT` | `8000` |
| `LOG_LEVEL` | `INFO` |

**STEP-BY-STEP FOR EACH VARIABLE:**

1. Click **"Add Environment Variable"**
2. **Name:** Enter the key (e.g., `DATABASE_URL`)
3. **Value:** Enter the value (e.g., paste the PostgreSQL URL)
4. Click **"Save"**
5. Repeat for all 10 variables

### STEP 5: Trigger Deployment (2 minutes)

1. After adding all environment variables, click **"Manual Deploy"**
2. Select **"Deploy latest commit"**
3. Wait for deployment to complete
4. You should see **"Deployment successful"** ✅

### STEP 6: Test Backend is Working (2 minutes)

1. In Render dashboard, copy your service **URL** (e.g., `https://ai-learning-backend.onrender.com`)
2. Open in browser: `https://ai-learning-backend.onrender.com/api/health`
3. Should return:
   ```json
   {"status":"healthy","service":"Learning Platform API"}
   ```
4. If you see this, backend is **WORKING!** ✅

---

## 🚨 TROUBLESHOOTING

### If deployment fails with "OperationalError: failed to resolve host 'host'"

**Solution:**
1. Go to Render dashboard
2. Check **Environment Variables** section
3. Make sure `DATABASE_URL` is set and not empty
4. Make sure it starts with `postgresql://`
5. Click **"Manual Deploy"** again

### If you see "ModuleNotFoundError: No module named 'psycopg'"

**This is already fixed!** Just redeploy:
1. Click **"Manual Deploy"**
2. Select **"Deploy latest commit"**

### If backend works but frontend can't connect

**Check CORS:**
1. In Render, go to Environment Variables
2. Make sure `CORS_ORIGINS` includes your frontend URL
3. Make sure `FRONTEND_URL` matches your frontend domain
4. Save and redeploy

---

## ✅ VERIFICATION CHECKLIST

Before saying deployment is complete:

- [ ] PostgreSQL database created on Render
- [ ] Web Service created and connected to GitHub
- [ ] All 10 environment variables set in Render dashboard
- [ ] DATABASE_URL starts with `postgresql://` and is not empty
- [ ] JWT_SECRET is a long random string (not the default)
- [ ] Manual Deploy completed successfully
- [ ] Backend URL accessible (`/api/health` returns success)
- [ ] No errors in Render logs

---

## 📊 YOUR BACKEND WILL WORK WHEN

- ✅ Render shows **"Live"** status (green dot)
- ✅ `/api/health` endpoint responds
- ✅ Logs show **"Database tables initialized successfully"**
- ✅ No errors in Render console

---

## 🎉 NEXT STEPS AFTER BACKEND IS DEPLOYED

1. Copy your backend URL from Render (e.g., `https://ai-learning-backend.onrender.com`)
2. Go to Frontend deployment (Vercel)
3. Set `NEXT_PUBLIC_API_URL` to your backend URL
4. Vercel will auto-redeploy
5. Test frontend + backend together

---

## 💡 TIPS

- **Save your DATABASE_URL** - you'll need it again if you add more services
- **Keep JWT_SECRET secret** - never share it
- **Use environment variables** - never hardcode secrets
- **Test with /api/health** - if it works, the backend is ready
- **Check logs** - Render logs show detailed error messages

---

## ❓ COMMON QUESTIONS

**Q: What if I already created a service?**
A: You can still update it! Go to the service → Environment → add the variables

**Q: Can I use the free plan?**
A: Yes, but be aware of free tier limits. See Render pricing for details

**Q: How long does deployment take?**
A: Usually 2-5 minutes from clicking "Manual Deploy"

**Q: What if DATABASE_URL is wrong?**
A: Just update it in Environment Variables and redeploy

**Q: Do I need to redeploy after updating env vars?**
A: Yes, click "Manual Deploy" → "Deploy latest commit"

---

## 🚀 YOU GOT THIS!

Follow these steps exactly and your backend will be deployed successfully. The error you're seeing is just because DATABASE_URL wasn't set - once you add it, everything will work!

**Questions? Check the logs in Render dashboard for detailed error messages.**
