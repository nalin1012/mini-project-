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

@router.post("/init-demo-progress")
async def init_demo_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initialize demo progress data for new users - creates sample progress for all subjects"""
    # Define demo progress data
    demo_data = {
        "Math": {"correct": 7, "total": 10, "sessions": 2},
        "Science": {"correct": 5, "total": 8, "sessions": 1},
        "Programming": {"correct": 9, "total": 10, "sessions": 3},
        "English": {"correct": 6, "total": 10, "sessions": 2},
        "Aptitude": {"correct": 4, "total": 8, "sessions": 1},
        "Study Skills": {"correct": 8, "total": 10, "sessions": 2},
        "Fractions": {"correct": 6, "total": 8, "sessions": 1},
        "Algebra": {"correct": 5, "total": 9, "sessions": 1},
    }
    
    created = []
    for topic, data in demo_data.items():
        existing = db.query(LearningProgress).filter(
            LearningProgress.student_id == current_user.id,
            LearningProgress.concept == topic
        ).first()
        
        if not existing:
            mastery = data["correct"] / data["total"]
            progress = LearningProgress(
                student_id=current_user.id,
                subject_id=1,
                concept=topic,
                mastery_score=mastery,
                total_questions_attempted=data["total"],
                correct_answers=data["correct"],
                sessions_completed=data["sessions"]
            )
            db.add(progress)
            created.append(topic)
    
    if created:
        db.commit()
    
    return {
        "status": "initialized",
        "created_topics": created,
        "message": f"Demo progress initialized for {len(created)} topics"
    }


@router.get("/progress/all")
async def get_all_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all progress records for the user - includes initialized entries for all subjects"""
    # Get all existing progress
    all_progress = db.query(LearningProgress).filter(
        LearningProgress.student_id == current_user.id
    ).all()
    
    # Create a map of existing progress by concept
    progress_map = {p.concept: p for p in all_progress}
    
    # Define all subjects that should be tracked
    all_subjects = [
        "Fractions", "Algebra", "Loops", "Variables", "Functions",
        "Motion", "Grammar", "Reasoning", "Geometry", "Statistics",
        "Math", "Science", "Programming", "English", "Aptitude", "Study Skills"
    ]
    
    # Build response including both existing and unstarted progress
    result = []
    for subject in all_subjects:
        if subject in progress_map:
            p = progress_map[subject]
            result.append({
                "topic": p.concept,
                "subject_id": p.subject_id or 1,
                "mastery_score": round(p.mastery_score, 2),
                "sessions_completed": p.sessions_completed,
                "total_questions": p.total_questions_attempted,
                "correct_answers": p.correct_answers,
                "status": "Mastered" if p.mastery_score >= 0.8 else "In Progress" if p.mastery_score > 0 else "Not started",
                "last_updated": str(p.last_updated) if p.last_updated else None
            })
        else:
            # Create unstarted entry
            result.append({
                "topic": subject,
                "subject_id": 1,
                "mastery_score": 0.0,
                "sessions_completed": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "status": "Not started",
                "last_updated": None
            })
    
    return result

@router.post("/track-answer/{topic}")
async def track_answer(
    topic: str,
    payload: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track a quiz answer for a specific topic"""
    is_correct = payload.get("is_correct", False)
    
    # Get or create progress
    progress = db.query(LearningProgress).filter(
        LearningProgress.student_id == current_user.id,
        LearningProgress.concept == topic
    ).first()
    
    if not progress:
        progress = LearningProgress(
            student_id=current_user.id,
            concept=topic,
            mastery_score=0.0,
            sessions_completed=1,
            total_questions_attempted=1,
            correct_answers=1 if is_correct else 0
        )
        db.add(progress)
    else:
        progress.total_questions_attempted += 1
        if is_correct:
            progress.correct_answers += 1
        # Recalculate mastery score
        progress.mastery_score = progress.correct_answers / progress.total_questions_attempted if progress.total_questions_attempted > 0 else 0
    
    db.commit()
    
    return {
        "topic": topic,
        "is_correct": is_correct,
        "new_mastery_score": round(progress.mastery_score, 2),
        "total_questions": progress.total_questions_attempted,
        "correct_answers": progress.correct_answers
    }

