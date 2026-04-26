"""User Management Endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User, LoginHistory, QuizResult
from schemas import UserDetailResponse, UsersListResponse, LoginHistoryResponse
from auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    if request.headers.get("x-forwarded-for"):
        return request.headers.get("x-forwarded-for").split(",")[0].strip()
    return request.client.host if request.client else "unknown"

@router.get("/", response_model=UsersListResponse)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all users (admin only).
    Returns paginated list of users with their stats.
    """
    # Check if user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view users list"
        )
    
    # Get total count
    total = db.query(User).filter(User.is_active == True).count()
    
    # Get paginated users
    users = db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    # Build user responses with stats
    user_responses = []
    for user in users:
        # Get quiz stats
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
    
    return UsersListResponse(total=total, users=user_responses)

@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific user's details (admin or self)"""
    # Check permissions
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get quiz stats
    total_quizzes = db.query(QuizResult).filter(QuizResult.student_id == user.id).count()
    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == user.id).all()
    
    accuracy = 0.0
    if total_quizzes > 0:
        correct = sum(1 for q in quiz_results if q.is_correct)
        accuracy = (correct / total_quizzes) * 100
    
    return UserDetailResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        created_at=user.created_at,
        last_login=user.last_login,
        is_active=user.is_active,
        total_quizzes=total_quizzes,
        overall_accuracy=accuracy
    )

@router.get("/{user_id}/login-history", response_model=List[LoginHistoryResponse])
async def get_user_login_history(
    user_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get login history for a user (admin or self)"""
    # Check permissions
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own login history"
        )
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get login history
    history = db.query(LoginHistory).filter(
        LoginHistory.user_id == user_id
    ).order_by(desc(LoginHistory.login_time)).limit(limit).all()
    
    return [LoginHistoryResponse.from_orm(h) for h in history]

@router.post("/{user_id}/track-login")
async def track_login(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Track user login (called from auth endpoint)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get client info
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Create login record
    login_record = LoginHistory(
        user_id=user_id,
        login_time=datetime.utcnow(),
        ip_address=client_ip,
        user_agent=user_agent,
        login_method="password"
    )
    
    # Update last_login on user
    user.last_login = datetime.utcnow()
    
    db.add(login_record)
    db.commit()
    
    return {"message": "Login tracked successfully"}

@router.patch("/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user role (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change user roles"
        )
    
    if new_role not in ["student", "teacher", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = new_role
    db.commit()
    
    return {"message": f"User role updated to {new_role}"}

@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: int,
    is_active: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deactivate/reactivate user (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change user status"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = is_active
    db.commit()
    
    status_str = "activated" if is_active else "deactivated"
    return {"message": f"User {status_str}"}
