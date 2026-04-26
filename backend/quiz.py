from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import (
    Question, Topic, QuizResult, LearningProgress, User, WeakArea, Subject
)
from schemas import QuestionResponse, QuizAnswerSubmit, QuizResultResponse
from auth import get_current_user

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

# Comprehensive Quiz Bank - Structured by Topic and Difficulty
QUIZ_BANK = {
    "Fractions": {
        "easy": [
            {"question": "What is 1/2 + 1/4?", "options": ["3/4", "2/4", "1/6", "5/4"], "correct": 0, "explanation": "1/2 = 2/4, so 2/4 + 1/4 = 3/4", "subject": "Math"},
            {"question": "Simplify 6/9", "options": ["2/3", "1/3", "3/6", "6/9"], "correct": 0, "explanation": "GCD of 6 and 9 is 3. 6÷3=2, 9÷3=3. So 6/9 = 2/3", "subject": "Math"},
            {"question": "What is 2/3 - 1/3?", "options": ["1/3", "3/3", "1/6", "1/2"], "correct": 0, "explanation": "2/3 - 1/3 = 1/3 (same denominator)", "subject": "Math"},
        ],
        "medium": [
            {"question": "Convert 0.75 to a fraction", "options": ["3/4", "2/3", "7/10", "4/5"], "correct": 0, "explanation": "0.75 = 75/100 = 3/4", "subject": "Math"},
            {"question": "What is 5/6 + 1/3?", "options": ["7/6", "6/9", "5/3", "1/2"], "correct": 0, "explanation": "5/6 + 2/6 = 7/6", "subject": "Math"},
        ],
        "hard": [
            {"question": "Simplify (3/4 × 8/9) ÷ (2/3)", "options": ["1", "2/3", "4/3", "1/2"], "correct": 0, "explanation": "3/4 × 8/9 = 2/3. Then 2/3 ÷ 2/3 = 1", "subject": "Math"},
        ]
    },
    "Algebra": {
        "easy": [
            {"question": "Solve: x + 5 = 12", "options": ["x = 7", "x = 17", "x = 2", "x = 12"], "correct": 0, "explanation": "x = 12 - 5 = 7", "subject": "Math"},
            {"question": "Simplify: 2x + 3x", "options": ["5x", "6x", "2x", "3x"], "correct": 0, "explanation": "2x + 3x = 5x", "subject": "Math"},
        ],
        "medium": [
            {"question": "Solve: 3x - 2 = 10", "options": ["x = 4", "x = 3", "x = 5", "x = 2"], "correct": 0, "explanation": "3x = 12, so x = 4", "subject": "Math"},
            {"question": "Solve: 2(x + 3) = 14", "options": ["x = 4", "x = 5", "x = 7", "x = 8"], "correct": 0, "explanation": "x + 3 = 7, so x = 4", "subject": "Math"},
        ],
        "hard": [
            {"question": "Solve: 2x² + 3x - 2 = 0", "options": ["x = 1/2 or x = -2", "x = 1 or x = 2", "x = -1", "x = 0"], "correct": 0, "explanation": "Quadratic: (2x-1)(x+2) = 0", "subject": "Math"},
        ]
    },
    "Loops": {
        "easy": [
            {"question": "Output of: for i in range(3): print(i)", "options": ["0 1 2", "1 2 3", "0 1", "1 2"], "correct": 0, "explanation": "range(3) = [0, 1, 2]", "subject": "Programming"},
            {"question": "Times executed: for i in range(5): pass", "options": ["5", "4", "6", "0"], "correct": 0, "explanation": "5 iterations", "subject": "Programming"},
        ],
        "medium": [
            {"question": "Output: for i in range(1, 4): print(i)", "options": ["1 2 3", "0 1 2 3", "1 2", "0 1 2"], "correct": 0, "explanation": "range(1,4) = [1, 2, 3]", "subject": "Programming"},
        ],
        "hard": [
            {"question": "Sum: for i in range(1, 5): total += i", "options": ["10", "15", "14", "20"], "correct": 0, "explanation": "1+2+3+4 = 10", "subject": "Programming"},
        ]
    },
    "Variables": {
        "easy": [
            {"question": "Correct way to declare in Python", "options": ["x = 5", "var x = 5", "declare x = 5", "int x = 5"], "correct": 0, "explanation": "Python: x = 5", "subject": "Programming"},
            {"question": "Value of x after: x = 5; x = x + 3", "options": ["8", "5", "3", "0"], "correct": 0, "explanation": "5 + 3 = 8", "subject": "Programming"},
        ],
        "medium": [
            {"question": "Type of: x = '5'", "options": ["String", "Integer", "Float", "Boolean"], "correct": 0, "explanation": "Quotes make it a string", "subject": "Programming"},
        ],
    },
    "Functions": {
        "easy": [
            {"question": "What does return do?", "options": ["Exits and provides value", "Starts loop", "Defines variable", "Prints"], "correct": 0, "explanation": "Return ends function and sends value", "subject": "Programming"},
        ],
        "medium": [
            {"question": "Output: def add(a,b): return a+b; print(add(3,4))", "options": ["7", "3", "4", "34"], "correct": 0, "explanation": "3 + 4 = 7", "subject": "Programming"},
        ],
    },
    "Motion": {
        "easy": [
            {"question": "What is velocity?", "options": ["Speed with direction", "Distance/time", "Acceleration", "Force"], "correct": 0, "explanation": "Vector quantity", "subject": "Science"},
            {"question": "Speed = 100m in 10s?", "options": ["10 m/s", "1 m/s", "100 m/s", "1000 m/s"], "correct": 0, "explanation": "100/10 = 10 m/s", "subject": "Science"},
        ],
        "medium": [
            {"question": "What is acceleration?", "options": ["Change in velocity/time", "Change distance", "Speed", "Force"], "correct": 0, "explanation": "Rate of velocity change", "subject": "Science"},
        ],
    },
    "Grammar": {
        "easy": [
            {"question": "Correct sentence", "options": ["She go to school", "She goes to school", "She going", "She gone"], "correct": 1, "explanation": "Third person singular", "subject": "English"},
        ],
        "medium": [
            {"question": "Noun in: 'quick brown fox'", "options": ["quick", "brown", "fox", "The"], "correct": 2, "explanation": "fox is the noun", "subject": "English"},
        ],
    },
    "Reasoning": {
        "easy": [
            {"question": "Pattern: 2, 4, 6, 8, ?", "options": ["10", "9", "12", "16"], "correct": 0, "explanation": "+2 each time", "subject": "Aptitude"},
        ],
        "medium": [
            {"question": "Cats are animals, Fluffy is cat, then?", "options": ["Fluffy is animal", "Animals are cats", "Fluffy not animal", "Cats not animals"], "correct": 0, "explanation": "Logical deduction", "subject": "Aptitude"},
        ],
    }
}

@router.get("/topics")
async def get_all_topics():
    """Get list of all available topics"""
    topics = [{"name": topic, "difficulties": list(difficulties.keys())} for topic, difficulties in QUIZ_BANK.items()]
    return {"topics": topics}

@router.get("/generate/{topic}")
async def generate_quiz(
    topic: str,
    count: int = 5,
    difficulty: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate adaptive quiz questions"""
    if topic not in QUIZ_BANK:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' not found")
    
    topic_questions = QUIZ_BANK[topic]
    
    # Determine difficulty
    if difficulty is None:
        user_perf = db.query(LearningProgress).filter(
            LearningProgress.student_id == current_user.id,
            LearningProgress.concept == topic
        ).first()
        difficulty = "hard" if user_perf and user_perf.mastery_score > 0.8 else ("medium" if user_perf and user_perf.mastery_score > 0.6 else "easy")
    elif difficulty not in ["easy", "medium", "hard"]:
        raise HTTPException(status_code=400, detail="Invalid difficulty")
    
    questions_list = topic_questions.get(difficulty, topic_questions.get("easy", []))
    if not questions_list:
        raise HTTPException(status_code=500, detail="No questions available")
    
    selected = random.sample(questions_list, min(count, len(questions_list)))
    quiz = [{"question": q["question"], "options": q["options"], "difficulty": difficulty} for q in selected]
    
    return {"topic": topic, "difficulty": difficulty, "total_questions": len(quiz), "questions": quiz}

@router.get("/generate/{subject}/{topic}")
async def generate_quiz_old(
    subject: str,
    topic: str,
    count: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Legacy endpoint - redirect to new endpoint"""
    return await generate_quiz(topic, count, None, current_user, db)

@router.post("/submit-answer")
async def submit_quiz_answer(
    answer: QuizAnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answer and get feedback"""
    topic_key = answer.topic
    question_index = answer.question_index
    selected_option = answer.selected_option
    
    if topic_key not in QUIZ_BANK:
        raise HTTPException(status_code=400, detail=f"Invalid topic: {topic_key}")
    
    # Get all questions from all difficulties
    topic_questions = QUIZ_BANK[topic_key]
    all_questions = []
    for diff in ["easy", "medium", "hard"]:
        all_questions.extend(topic_questions.get(diff, []))
    
    if question_index >= len(all_questions):
        raise HTTPException(status_code=400, detail="Invalid question index")
    
    question_data = all_questions[question_index]
    is_correct = selected_option == question_data["correct"]
    
    # Store quiz result
    quiz_result = QuizResult(
        student_id=current_user.id,
        question_id=question_index,
        topic_id=1,
        selected_option=selected_option,
        is_correct=is_correct,
        time_taken=answer.time_taken
    )
    db.add(quiz_result)
    
    # Update learning progress
    progress = db.query(LearningProgress).filter(
        LearningProgress.student_id == current_user.id,
        LearningProgress.concept == topic_key
    ).first()
    
    if not progress:
        progress = LearningProgress(
            student_id=current_user.id,
            subject_id=1,
            concept=topic_key,
            mastery_score=0.0,
            total_questions_attempted=0,
            correct_answers=0,
            sessions_completed=0
        )
        db.add(progress)
    
    progress.total_questions_attempted += 1
    if is_correct:
        progress.correct_answers += 1
    
    progress.mastery_score = progress.correct_answers / max(progress.total_questions_attempted, 1)
    progress.sessions_completed += 1
    
    # Detect knowledge gap
    if progress.mastery_score < 0.6:
        weak_area = db.query(WeakArea).filter(
            WeakArea.student_id == current_user.id,
            WeakArea.topic_id == 1
        ).first()
        
        if not weak_area:
            weak_area = WeakArea(student_id=current_user.id, topic_id=1, mastery_score=progress.mastery_score)
            db.add(weak_area)
        else:
            weak_area.mastery_score = progress.mastery_score
    
    db.commit()
    
    return {
        "is_correct": is_correct,
        "explanation": question_data.get("explanation", ""),
        "correct_option": question_data["correct"],
        "selected_option": selected_option,
        "mastery_update": round(progress.mastery_score * 100, 2),
        "message": "✓ Correct! Great job!" if is_correct else "✗ Incorrect. Review the concept."
    }

@router.get("/stats")
async def get_quiz_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's quiz statistics"""
    total_results = db.query(QuizResult).filter(QuizResult.student_id == current_user.id).count()
    correct_results = db.query(QuizResult).filter(QuizResult.student_id == current_user.id, QuizResult.is_correct == True).count()
    accuracy = (correct_results / total_results * 100) if total_results > 0 else 0
    
    return {
        "total_quizzes": total_results,
        "correct_answers": correct_results,
        "accuracy_percentage": round(accuracy, 2)
    }
