"""Firebase Realtime Database Service"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User, LearningProgress, QuizResult
from auth import get_current_user
from firebase_config import (
    save_user_progress_to_firebase,
    get_user_progress_from_firebase,
    get_user_quiz_results_from_firebase,
    save_user_stats_snapshot_to_firebase,
    FIREBASE_AVAILABLE
)

router = APIRouter(prefix="/api/firebase", tags=["firebase"])

@router.post("/sync-progress")
async def sync_progress_to_firebase(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync user's learning progress to Firebase"""
    if not FIREBASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Firebase not configured"
        )
    
    try:
        # Get user's progress from PostgreSQL
        progress_list = db.query(LearningProgress).filter(
            LearningProgress.student_id == current_user.id
        ).all()
        
        progress_data = {
            "user_id": current_user.id,
            "user_name": current_user.name,
            "email": current_user.email,
            "points": current_user.points,
            "streak": current_user.streak,
            "last_updated": datetime.utcnow().isoformat(),
            "topics": {}
        }
        
        for progress in progress_list:
            progress_data["topics"][progress.concept] = {
                "mastery_score": round(progress.mastery_score * 100, 2),
                "total_questions": progress.total_questions_attempted,
                "correct_answers": progress.correct_answers,
                "sessions_completed": progress.sessions_completed,
            }
        
        # Save to Firebase
        success = save_user_progress_to_firebase(current_user.id, progress_data)
        
        if success:
            return {
                "message": "Progress synced to Firebase successfully",
                "topics_synced": len(progress_list)
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to sync progress to Firebase"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error syncing progress: {str(e)}"
        )

@router.get("/progress")
async def get_firebase_progress(
    current_user: User = Depends(get_current_user),
):
    """Get user's progress from Firebase"""
    if not FIREBASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Firebase not configured"
        )
    
    try:
        progress_data = get_user_progress_from_firebase(current_user.id)
        
        if progress_data:
            return progress_data
        else:
            return {
                "message": "No progress data found in Firebase",
                "user_id": current_user.id
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving progress: {str(e)}"
        )

@router.get("/quiz-results")
async def get_firebase_quiz_results(
    current_user: User = Depends(get_current_user),
):
    """Get user's quiz results from Firebase"""
    if not FIREBASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Firebase not configured"
        )
    
    try:
        quiz_results = get_user_quiz_results_from_firebase(current_user.id)
        
        return {
            "user_id": current_user.id,
            "quiz_results": quiz_results or {},
            "total_quizzes": len(quiz_results) if quiz_results else 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving quiz results: {str(e)}"
        )

@router.post("/stats-snapshot")
async def create_stats_snapshot(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a real-time snapshot of user stats in Firebase"""
    if not FIREBASE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Firebase not configured"
        )
    
    try:
        total_quizzes = db.query(QuizResult).filter(
            QuizResult.student_id == current_user.id
        ).count()
        
        correct_answers = db.query(QuizResult).filter(
            QuizResult.student_id == current_user.id,
            QuizResult.is_correct.is_(True)
        ).count()
        
        accuracy = (correct_answers / total_quizzes * 100) if total_quizzes > 0 else 0
        
        stats = {
            "user_id": current_user.id,
            "user_name": current_user.name,
            "total_quizzes": total_quizzes,
            "correct_answers": correct_answers,
            "accuracy_percentage": round(accuracy, 2),
            "points": current_user.points,
            "streak": current_user.streak,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Save stats to a dedicated Firebase node (do not overwrite progress)
        success = save_user_stats_snapshot_to_firebase(current_user.id, stats)
        
        if success:
            return stats
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to create stats snapshot"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating stats snapshot: {str(e)}"
        )
