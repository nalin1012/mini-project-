from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User, LearningProgress
from auth import get_current_user
from machine_learning.ml_model import analyze_student

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

@router.get("/analyze/{concept}")
def analyze(
    concept: str,
    correct: int = 2,
    total: int = 5,
    time_spent: int = 120,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze student performance and provide personalized recommendations
    Returns mastery score, knowledge gap status, and learning path suggestions
    """
    # Validate inputs
    if correct < 0 or total <= 0 or correct > total:
        raise HTTPException(
            status_code=400,
            detail="Invalid quiz parameters: correct must be 0-total, total > 0"
        )
    
    try:
        result = analyze_student(
            concept=concept,
            correct=correct,
            total=total,
            time_spent=time_spent
        )
        return result
    except Exception as e:
        # Fallback if ML model not available
        mastery = correct / total
        return {
            "mastery_score": mastery,
            "knowledge_gap": 1 if mastery < 0.6 else 0,
            "recommendation": f"{'Revise concept' if mastery < 0.6 else 'Move to next topic'}",
            "status": "calculated_without_ml"
        }

@router.get("/personalized/{user_id}")
def get_personalized_recommendations(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized learning recommendations based on user's performance"""
    # Only users can see their own recommendations
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    progress_records = db.query(LearningProgress).filter(
        LearningProgress.student_id == user_id
    ).all()
    
    recommendations = []
    
    for record in progress_records:
        if record.mastery_score < 0.6:
            recommendations.append({
                "concept": record.concept,
                "mastery_score": record.mastery_score,
                "recommendation": f"Focus on {record.concept}. Your current score is {record.mastery_score * 100:.0f}%. Practice more to improve.",
                "next_steps": ["Review fundamentals", "Practice 5 more questions", "Take another quiz"]
            })
        elif record.mastery_score < 0.8:
            recommendations.append({
                "concept": record.concept,
                "mastery_score": record.mastery_score,
                "recommendation": f"Good progress in {record.concept}! Keep practicing to master it.",
                "next_steps": ["Challenge harder problems", "Apply knowledge in new contexts"]
            })
    
    return {
        "user_id": user_id,
        "total_recommendations": len(recommendations),
        "recommendations": recommendations,
        "overall_advice": "Focus on your weak areas first, then consolidate strong areas."
    }
