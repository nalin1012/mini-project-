from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User, WeakArea, LearningProgress, Topic
from schemas import KnowledgeGapResponse
from auth import get_current_user

router = APIRouter(prefix="/api/knowledge-gap", tags=["knowledge-gap"])

# AI-based recommendations
CONCEPT_RECOMMENDATIONS = {
    "Fractions": "Practice equivalent fractions and fraction addition. Try solving real-world problems with fractions.",
    "Algebra": "Review linear equations. Start with simple one-step equations before moving to multi-step problems.",
    "Loops": "Understand loop iteration. Practice with for and while loops with different conditions.",
    "Variables": "Learn variable naming conventions and data types. Practice variable assignment.",
    "Functions": "Understand function definition and return statements. Practice writing reusable functions.",
}

@router.get("/dashboard-summary")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete dashboard summary for the user
    Includes performance metrics and personalized recommendations
    """
    try:
        # Get all learning progress for the user
        progress_list = db.query(LearningProgress).filter(
            LearningProgress.student_id == current_user.id
        ).all()
        
        total_quizzes = len(progress_list)
        total_questions = sum(p.total_questions_attempted for p in progress_list)
        correct_answers = sum(p.correct_answers for p in progress_list)
        
        overall_accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Get weak areas (mastery < 60%)
        weak_areas = []
        for progress in progress_list:
            if progress.mastery_score < 0.6:
                weak_areas.append({
                    "topic": progress.concept,
                    "mastery_score": round(progress.mastery_score, 2),
                    "recommendation": CONCEPT_RECOMMENDATIONS.get(
                        progress.concept,
                        f"Review {progress.concept} fundamentals and practice more problems."
                    ),
                    "suggested_resources": f"Practice {progress.concept} exercises"
                })
        
        return {
            "user_name": current_user.name,
            "total_quizzes_completed": total_quizzes,
            "total_questions_attempted": total_questions,
            "correct_answers": correct_answers,
            "overall_accuracy": round(overall_accuracy, 2),
            "points": current_user.points,
            "streak": current_user.streak,
            "weak_areas": weak_areas,
            "study_topics": [p.concept for p in progress_list]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard summary")

@router.get("/detect", response_model=List[KnowledgeGapResponse])
async def detect_knowledge_gaps(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Detect knowledge gaps based on quiz performance
    Returns topics where user has low mastery score
    """
    weak_areas = db.query(WeakArea).filter(
        WeakArea.student_id == current_user.id,
        WeakArea.mastery_score < 0.6  # Less than 60% is weak
    ).all()
    
    gaps = []
    for weak_area in weak_areas:
        # Get topic name (for demo, we'll use placeholder)
        topic_name = "Unknown Topic"
        for concept, _ in CONCEPT_RECOMMENDATIONS.items():
            if concept in str(weak_area.topic_id):
                topic_name = concept
                break
        
        # Find topic name from learning progress
        progress = db.query(LearningProgress).filter(
            LearningProgress.student_id == current_user.id,
            LearningProgress.mastery_score == weak_area.mastery_score
        ).first()
        
        if progress:
            topic_name = progress.concept
        
        gap = KnowledgeGapResponse(
            topic_name=topic_name,
            mastery_score=round(weak_area.mastery_score, 2),
            weak_area=True,
            recommendation=f"You are weak in {topic_name}. Practice recommended.",
            suggested_next_step=CONCEPT_RECOMMENDATIONS.get(
                topic_name,
                f"Review {topic_name} fundamentals and practice more problems."
            )
        )
        gaps.append(gap)
    
    return gaps

@router.get("/progress/{topic}")
async def get_topic_progress(
    topic: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's progress in a specific topic"""
    progress = db.query(LearningProgress).filter(
        LearningProgress.student_id == current_user.id,
        LearningProgress.concept == topic
    ).first()
    
    if not progress:
        return {
            "topic": topic,
            "mastery_score": 0.0,
            "sessions_completed": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "status": "Not started"
        }
    
    return {
        "topic": topic,
        "mastery_score": round(progress.mastery_score, 2),
        "sessions_completed": progress.sessions_completed,
        "total_questions": progress.total_questions_attempted,
        "correct_answers": progress.correct_answers,
        "status": "In Progress" if progress.mastery_score < 0.8 else "Mastered",
        "last_updated": progress.last_updated
    }

@router.get("/dashboard-summary")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard summary with knowledge gaps and stats
    """
    # Get all learning progress
    all_progress = db.query(LearningProgress).filter(
        LearningProgress.student_id == current_user.id
    ).all()
    
    # Calculate overall stats
    total_questions = sum(p.total_questions_attempted for p in all_progress)
    total_correct = sum(p.correct_answers for p in all_progress)
    overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    # Detect weak areas
    weak_areas = []
    for progress in all_progress:
        if progress.mastery_score < 0.6:
            weak_areas.append({
                "topic": progress.concept,
                "mastery_score": round(progress.mastery_score, 2),
                "recommendation": f"You need more practice in {progress.concept}.",
                "suggested_resources": CONCEPT_RECOMMENDATIONS.get(
                    progress.concept,
                    "Review the fundamentals and practice more problems."
                )
            })
    
    return {
        "user_name": current_user.name,
        "total_quizzes_completed": len(all_progress),
        "total_questions_attempted": total_questions,
        "correct_answers": total_correct,
        "overall_accuracy": round(overall_accuracy, 2),
        "weak_areas": weak_areas,
        "study_topics": [p.concept for p in all_progress],
        "recommendation": (
            "You're doing great! Keep practicing." 
            if overall_accuracy > 70 
            else "Focus on your weak areas to improve."
        )
    }

@router.post("/mark-mastered/{topic}")
async def mark_topic_mastered(
    topic: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a topic as mastered (90%+ accuracy)"""
    progress = db.query(LearningProgress).filter(
        LearningProgress.student_id == current_user.id,
        LearningProgress.concept == topic
    ).first()
    
    if not progress:
        return {"status": "error", "message": "Progress record not found"}
    
    if progress.mastery_score >= 0.9:
        return {
            "status": "success",
            "message": f"Great! You have mastered {topic}!",
            "topic": topic,
            "mastery_score": round(progress.mastery_score, 2)
        }
    else:
        return {
            "status": "warning",
            "message": f"You need {round((0.9 - progress.mastery_score) * 100, 1)}% more to master this topic.",
            "topic": topic,
            "current_score": round(progress.mastery_score, 2),
            "required_score": 0.9
        }
