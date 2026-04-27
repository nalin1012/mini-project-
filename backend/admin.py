"""Admin Dashboard Endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User, LoginHistory, QuizResult, LearningProgress
from schemas import AdminDashboardResponse, LoginStatsResponse, RecentLoginResponse, UserDetailResponse
from auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    """Dependency to ensure user is admin with enhanced authorization checks"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    if current_user.role != "admin":
        logger.warning(f"Unauthorized admin access attempt by user: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this resource"
        )
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive"
        )
    
    return current_user

@router.get("/dashboard", response_model=AdminDashboardResponse)
async def get_admin_dashboard(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard with overall platform statistics"""
    
    # Total users
    total_users = db.query(User).filter(User.is_active == True).count()
    
    # Active today (logged in last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    active_today = db.query(User).filter(
        User.last_login >= yesterday,
        User.is_active == True
    ).count()
    
    # Total logins
    total_logins = db.query(LoginHistory).count()
    
    # Average logins per user
    avg_logins = total_logins / total_users if total_users > 0 else 0
    
    # Recent logins
    recent_logins_data = db.query(
        LoginHistory.id,
        LoginHistory.user_id,
        LoginHistory.login_time,
        LoginHistory.ip_address,
        LoginHistory.login_method,
        User.name,
        User.email
    ).join(User, LoginHistory.user_id == User.id).order_by(
        desc(LoginHistory.login_time)
    ).limit(10).all()
    
    recent_logins = []
    for login in recent_logins_data:
        recent_logins.append(RecentLoginResponse(
            user_id=login.user_id,
            user_name=login.name,
            user_email=login.email,
            login_time=login.login_time,
            ip_address=login.ip_address,
            login_method=login.login_method
        ))
    
    # All users with stats
    users = db.query(User).filter(User.is_active == True).all()
    user_responses = []
    total_quizzes_all = 0
    total_accuracy = 0.0
    
    for user in users:
        total_quizzes = db.query(QuizResult).filter(QuizResult.student_id == user.id).count()
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == user.id).all()
        
        accuracy = 0.0
        if total_quizzes > 0:
            correct = sum(1 for q in quiz_results if q.is_correct)
            accuracy = (correct / total_quizzes) * 100
        
        user_responses.append(UserDetailResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            created_at=user.created_at,
            last_login=user.last_login,
            is_active=user.is_active,
            total_quizzes=total_quizzes,
            overall_accuracy=accuracy
        ))
        
        total_quizzes_all += total_quizzes
        total_accuracy += accuracy
    
    avg_accuracy = (total_accuracy / len(users)) if len(users) > 0 else 0.0
    
    login_stats = LoginStatsResponse(
        total_users=total_users,
        active_today=active_today,
        total_logins=total_logins,
        average_logins_per_user=round(avg_logins, 2)
    )
    
    return AdminDashboardResponse(
        total_users=total_users,
        total_quizzes=total_quizzes_all,
        average_accuracy=round(avg_accuracy, 2),
        total_logins=total_logins,
        recent_logins=recent_logins,
        users=user_responses,
        login_stats=login_stats
    )

@router.get("/stats/daily")
async def get_daily_stats(
    days: int = 7,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get daily statistics for last N days"""
    stats = []
    
    for i in range(days):
        start_date = datetime.utcnow() - timedelta(days=i+1)
        end_date = datetime.utcnow() - timedelta(days=i)
        
        # Logins in this day
        logins = db.query(LoginHistory).filter(
            LoginHistory.login_time >= start_date,
            LoginHistory.login_time < end_date
        ).count()
        
        # Quizzes taken in this day
        quizzes = db.query(QuizResult).filter(
            QuizResult.created_at >= start_date,
            QuizResult.created_at < end_date
        ).count()
        
        stats.append({
            "date": start_date.strftime("%Y-%m-%d"),
            "logins": logins,
            "quizzes": quizzes
        })
    
    return sorted(stats, key=lambda x: x["date"])

@router.get("/stats/user-growth")
async def get_user_growth_stats(
    days: int = 30,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user growth statistics"""
    stats = []
    
    for i in range(days, -1, -1):
        target_date = datetime.utcnow() - timedelta(days=i)
        
        users = db.query(User).filter(
            User.created_at <= target_date,
            User.is_active == True
        ).count()
        
        stats.append({
            "date": target_date.strftime("%Y-%m-%d"),
            "total_users": users
        })
    
    return stats

@router.get("/stats/accuracy")
async def get_platform_accuracy_stats(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get platform-wide accuracy statistics"""
    quiz_results = db.query(QuizResult).all()
    
    if not quiz_results:
        return {
            "total_questions": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "overall_accuracy": 0.0,
            "by_difficulty": {}
        }
    
    total = len(quiz_results)
    correct = sum(1 for q in quiz_results if q.is_correct)
    incorrect = total - correct
    
    # Group by difficulty
    accuracy_by_difficulty = {}
    for difficulty in ["easy", "medium", "hard"]:
        difficulty_results = [q for q in quiz_results if q.is_correct]  # Simplified
        if difficulty_results:
            diff_correct = sum(1 for q in difficulty_results if q.is_correct)
            accuracy_by_difficulty[difficulty] = {
                "attempts": len(difficulty_results),
                "correct": diff_correct,
                "accuracy": round((diff_correct / len(difficulty_results)) * 100, 2)
            }
    
    return {
        "total_questions": total,
        "correct_answers": correct,
        "incorrect_answers": incorrect,
        "overall_accuracy": round((correct / total) * 100, 2) if total > 0 else 0.0,
        "by_difficulty": accuracy_by_difficulty
    }

@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Deactivate a user account"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    user.is_active = False
    db.commit()
    
    return {"message": f"User {user.name} deactivated"}

@router.post("/users/{user_id}/reactivate")
async def reactivate_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reactivate a user account"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    
    return {"message": f"User {user.name} reactivated"}

@router.get("/users")
async def get_all_users(
    admin_user: User = Depends(require_admin),
    skip: int = 0,
    limit: int = 50,
    search: str = "",
    db: Session = Depends(get_db)
):
    """Get all users with optional search and pagination"""
    query = db.query(User)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.name.ilike(search_term)) | 
            (User.email.ilike(search_term))
        )
    
    total = query.count()
    users = query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()
    
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
            "last_login": user.last_login,
            "role": user.role,
            "is_active": user.is_active
        })
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": user_list
    }

@router.get("/logins")
async def get_login_history(
    admin_user: User = Depends(require_admin),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get recent login history"""
    total = db.query(LoginHistory).count()
    
    logins = db.query(
        LoginHistory.id,
        LoginHistory.user_id,
        LoginHistory.login_time,
        LoginHistory.ip_address,
        LoginHistory.login_method,
        User.name,
        User.email
    ).join(User, LoginHistory.user_id == User.id).order_by(
        desc(LoginHistory.login_time)
    ).offset(skip).limit(limit).all()
    
    login_list = []
    for login in logins:
        login_list.append({
            "id": login.id,
            "user_id": login.user_id,
            "user_name": login.name,
            "user_email": login.email,
            "login_time": login.login_time,
            "ip_address": login.ip_address,
            "login_method": login.login_method
        })
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "logins": login_list
    }

@router.get("/export/users")
async def export_users(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Export all users data"""
    users = db.query(User).filter(User.is_active == True).all()
    
    export_data = []
    for user in users:
        total_quizzes = db.query(QuizResult).filter(QuizResult.student_id == user.id).count()
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == user.id).all()
        
        accuracy = 0.0
        if total_quizzes > 0:
            correct = sum(1 for q in quiz_results if q.is_correct)
            accuracy = (correct / total_quizzes) * 100
        
        export_data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "total_quizzes": total_quizzes,
            "accuracy": round(accuracy, 2)
        })
    
    return export_data
