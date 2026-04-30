# 📋 Production Deployment Checklist

## Pre-Deployment Verification

### Code Quality
- [ ] All tests pass: `npm run build` (frontend) and `pytest` (backend)
- [ ] Linter passes: `npm run lint` (frontend)
- [ ] No console errors or warnings
- [ ] Code reviewed and approved
- [ ] All secrets removed from code

### Environment Variables
- [ ] Backend: All required env vars configured in `.env` and Render
- [ ] Frontend: `NEXT_PUBLIC_API_URL` points to correct backend
- [ ] Production secrets are strong and random
- [ ] `.env` files are in `.gitignore`
- [ ] `.env.example` files are complete but don't have real secrets

### Database
- [ ] Database migrations run successfully
- [ ] Database backups are enabled
- [ ] Database user has limited permissions
- [ ] Connection string is correct

### API Integration
- [ ] Backend health check passes: `/api/health`
- [ ] CORS configuration allows frontend domain
- [ ] API endpoints tested with actual requests
- [ ] Error handling works for all error codes

### Frontend
- [ ] Build completes without errors: `npm run build`
- [ ] No hardcoded URLs (use environment variables)
- [ ] API calls use centralized config
- [ ] Error boundaries implemented
- [ ] Loading states show correctly

### Backend
- [ ] All imports work correctly
- [ ] Database connection established
- [ ] External API keys are configured
- [ ] Logging is working
- [ ] Health check endpoint responds

---

## Deployment Steps

### 1. Backend (Render)
- [ ] Push code to GitHub main branch
- [ ] Go to Render Dashboard
- [ ] Verify build and deployment
- [ ] Check logs for errors
- [ ] Test API endpoints
- [ ] Record backend URL

### 2. Frontend (Vercel)
- [ ] Push code to GitHub main branch
- [ ] Go to Vercel Dashboard
- [ ] Verify build and deployment
- [ ] Check logs for errors
- [ ] Set environment variables
- [ ] Record frontend URL

### 3. Post-Deployment
- [ ] Update CORS_ORIGINS in backend with frontend URL
- [ ] Test full user flow end-to-end
- [ ] Verify database connectivity
- [ ] Check error logging
- [ ] Monitor performance metrics

---

## End-to-End Testing

### User Registration & Login
- [ ] Can register new account
- [ ] Email validation works
- [ ] Password strength validation works
- [ ] Can login with correct credentials
- [ ] Cannot login with wrong credentials
- [ ] Token is stored in localStorage

### Learning Flow
- [ ] Dashboard loads correctly
- [ ] Can view available subjects
- [ ] Can select a subject
- [ ] Learning content loads
- [ ] Quiz loads and functions
- [ ] Can submit quiz answers
- [ ] Results display correctly
- [ ] Progress updates in database

### Chat Tutor
- [ ] Chat interface loads
- [ ] Can send messages
- [ ] Can receive AI responses
- [ ] Chat history persists
- [ ] Can clear chat history

### Admin Panel
- [ ] Admin login works
- [ ] Can view user list
- [ ] Can view analytics
- [ ] Can manage content

### Error Scenarios
- [ ] Network timeout shows error message
- [ ] Invalid API response handled gracefully
- [ ] 401 error redirects to login
- [ ] 500 error shows friendly message
- [ ] Offline mode shows offline indicator

---

## Performance Checks

### Frontend
- [ ] Page load time < 3 seconds
- [ ] API response time < 1 second
- [ ] Bundle size is optimized
- [ ] No memory leaks
- [ ] Mobile responsive

### Backend
- [ ] Average response time < 500ms
- [ ] Database queries are optimized
- [ ] No N+1 query problems
- [ ] Caching is working (if implemented)
- [ ] Rate limiting is working (if implemented)

---

## Monitoring Setup

- [ ] Error tracking enabled (Sentry/similar)
- [ ] Performance monitoring enabled
- [ ] Uptime monitoring enabled
- [ ] Database backup schedule verified
- [ ] Log aggregation working

---

## Security Verification

- [ ] HTTPS enabled on both frontend and backend
- [ ] Cookies are HttpOnly and Secure
- [ ] CORS properly restricted
- [ ] JWT secret is strong (minimum 32 characters)
- [ ] No sensitive data in logs
- [ ] API rate limiting configured (if needed)
- [ ] Input validation implemented
- [ ] SQL injection prevention working

---

## Documentation

- [ ] README.md is complete and accurate
- [ ] DEPLOYMENT.md is accessible
- [ ] API documentation is available (FastAPI docs at /api/docs)
- [ ] Architecture diagram updated
- [ ] Troubleshooting guide is complete

---

## Team Communication

- [ ] Team informed of deployment
- [ ] Support team briefed on changes
- [ ] Status page updated (if applicable)
- [ ] Change log updated

---

## Post-Deployment (24 hours)

- [ ] Monitor error rates and logs
- [ ] Check performance metrics
- [ ] Verify user reports
- [ ] Monitor database size/growth
- [ ] Test backup/restore process

---

## Rollback Plan (Just in Case)

**If critical issues occur:**
1. Immediately identify the issue
2. Revert to previous stable deployment
3. Post-mortem analysis
4. Fix the issue in develop branch
5. Test thoroughly before re-deploying

**Rollback Commands:**

```bash
# Frontend: Use Vercel deployment history
# Backend: Use Render deployment history
```

---

**Deployment Date:** _______________
**Deployed By:** _______________
**Approval:** _______________
**Status:** ⬜ Not Started | 🟨 In Progress | 🟩 Complete
