# ⚡ Quick Reference - Admin Dashboard

## 🚀 QUICK START

```bash
# 1. Setup admin user and database
python setup_admin.py

# 2. Terminal 1 - Backend
cd backend
python main.py

# 3. Terminal 2 - Frontend  
cd frontend
npm run dev

# 4. Visit in browser
http://localhost:3000
```

---

## 👤 TEST CREDENTIALS

**Admin Account:**
- Email: `admin@test.com`
- Password: `admin123`

**Student Account:**
- Email: `john_doe@test.com`
- Password: `password123`

---

## 📍 KEY URLs

| Page | URL | Description |
|------|-----|-------------|
| Admin Dashboard | `http://localhost:3000/admin` | Main admin panel |
| Login | `http://localhost:3000/login` | User login |
| Register | `http://localhost:3000/register` | New account |
| Dashboard | `http://localhost:3000/dashboard` | User dashboard |
| Backend API | `http://localhost:8001` | API server |
| API Docs | `http://localhost:8001/api/docs` | Swagger UI |

---

## 📊 ADMIN DASHBOARD FEATURES

### Dashboard Statistics
- Total registered users
- Total quizzes taken
- Platform average accuracy
- Total login count
- Active users today
- Average logins per user

### User Management Table
- **Search**: Filter by name or email
- **Pagination**: Navigate through user list
- **Columns**: ID, Name, Email, Created At, Last Login, Status
- **Status**: Active/Inactive indicator

### Login History Timeline
- Recent login activity
- User names and emails
- Login timestamps
- IP addresses
- Login method (password/firebase/oauth)

---

## 🔌 API ENDPOINTS

### List Users (with search & pagination)
```bash
GET /api/admin/users?search=john&skip=0&limit=10
Authorization: Bearer <token>
```

### Get Login History
```bash
GET /api/admin/logins?skip=0&limit=50
Authorization: Bearer <token>
```

### Main Dashboard Stats
```bash
GET /api/admin/dashboard
Authorization: Bearer <token>
```

---

## 🎨 UI COMPONENTS

### AdminUserTable
- Location: `components/admin-user-table.tsx`
- Features: Search, pagination, sorting, status display
- Usage: Imported in `/admin` page

### LoginHistory
- Location: `components/login-history.tsx`
- Features: Timeline view, IP display, timestamps
- Usage: Available for reuse anywhere

### Admin Page
- Location: `app/admin/page.tsx`
- Features: Full dashboard with stats and tables
- Auth: Admin-only access

---

## ✨ FEATURES AT A GLANCE

| Feature | Status | Notes |
|---------|--------|-------|
| User Registration | ✅ | Validation + auto-login |
| User Login | ✅ | Login tracking enabled |
| Admin Dashboard | ✅ | Full statistics |
| User Search | ✅ | Real-time filter |
| Pagination | ✅ | 10 per page |
| Login History | ✅ | IP + timestamp tracking |
| Error Messages | ✅ | User-friendly |
| Network Errors | ✅ | Graceful handling |
| Dark Theme | ✅ | Glassmorphism design |
| Responsive Design | ✅ | Mobile-friendly |

---

## 🔐 SECURITY NOTES

✅ Admin role required for `/admin` route
✅ JWT token validation on all endpoints
✅ Passwords hashed with bcrypt
✅ Input validation with Pydantic
✅ IP addresses logged for all logins
✅ User agents tracked
✅ CORS protection enabled

---

## 🐛 TROUBLESHOOTING

### "Cannot GET /admin"
→ Make sure you're logged in as admin
→ Check `http://localhost:3000/login` first

### "Access denied. Admin privileges required"
→ Log in with admin account (admin@test.com)
→ Regular users cannot access `/admin`

### "Failed to fetch" on admin page
→ Backend not running on port 8001
→ Run: `cd backend && python main.py`
→ Check `.env.local` has correct API URL

### Users not showing in table
→ Register new users first
→ Refresh the page
→ Check browser console for errors

### No login history
→ Log in as a user (creates a history entry)
→ Go to admin dashboard
→ Check "Login History" section

---

## 📝 FORM VALIDATION

### Registration Form
```
Name:     min 2 characters, required
Email:    valid email format, must not exist
Password: min 6 characters, required
```

### Login Form
```
Email:    valid email format, required
Password: any length, required
```

---

## 🎯 ADMIN WORKFLOW

1. **Login as Admin**
   - Email: admin@test.com
   - Password: admin123

2. **View Dashboard**
   - See platform statistics
   - Monitor user growth
   - Track login activity

3. **Manage Users**
   - Search for specific users
   - View user details
   - See when users were active

4. **Monitor Activity**
   - Check recent logins
   - View IP addresses
   - Track login methods

---

## 💾 DATABASE

### User Table
```
id, email, name, hashed_password, role, 
created_at, last_login, is_active, firebase_uid
```

### LoginHistory Table
```
id, user_id, login_time, ip_address, 
user_agent, login_method
```

---

## 🔄 API RESPONSE FORMAT

### Success Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@test.com",
    "name": "User Name",
    "role": "admin",
    "created_at": "2024-01-20T10:30:00",
    "last_login": "2024-01-20T14:20:00"
  }
}
```

### Error Response
```json
{
  "detail": "Email already registered" 
  // or other error message
}
```

---

## 🎓 LEARNING RESOURCES

### Files to Review
1. `backend/admin.py` - API endpoints
2. `backend/schemas.py` - Validation
3. `frontend/components/admin-user-table.tsx` - User table
4. `frontend/components/login-history.tsx` - History timeline
5. `frontend/app/admin/page.tsx` - Dashboard page

### Key Concepts
- FastAPI routing and dependencies
- Pydantic validation
- SQLAlchemy ORM queries
- JWT authentication
- React hooks (useState, useEffect)
- TypeScript interfaces
- Tailwind CSS styling

---

## ✅ CHECKLIST BEFORE GOING LIVE

- [ ] Backend running on port 8001
- [ ] Frontend running on port 3000
- [ ] Can register new users
- [ ] Can login with credentials
- [ ] Admin dashboard shows statistics
- [ ] Can search users
- [ ] Can see login history
- [ ] Error messages are clear
- [ ] No console errors
- [ ] Mobile layout works
- [ ] Dark theme consistent

---

## 🎊 YOU'RE ALL SET!

Your Admin Dashboard is ready to use. 

**Start by:**
1. Running `python setup_admin.py`
2. Starting both servers
3. Logging in as admin
4. Visiting `/admin` to see the dashboard

Enjoy! 🚀
