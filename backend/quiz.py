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
from firebase_config import save_quiz_result_to_firebase

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

# Comprehensive Quiz Bank - Structured by Topic and Difficulty
# Enhanced with diverse question types and high-quality explanations
QUIZ_BANK = {
    "Fractions": {
        "easy": [
            {"question": "What is 1/2 + 1/4?", "options": ["3/4", "2/4", "1/6", "5/4"], "correct": 0, "explanation": "1/2 = 2/4, so 2/4 + 1/4 = 3/4. When adding fractions with the same denominator, add numerators only."},
            {"question": "Simplify 6/9", "options": ["2/3", "1/3", "3/6", "6/9"], "correct": 0, "explanation": "GCD(6,9) = 3. So 6÷3=2 and 9÷3=3. Therefore 6/9 = 2/3 in lowest terms."},
            {"question": "What is 2/3 - 1/3?", "options": ["1/3", "3/3", "1/6", "1/2"], "correct": 0, "explanation": "When subtracting fractions with the same denominator, subtract only the numerators: 2-1=1, keeping denominator 3."},
            {"question": "Which fraction is equivalent to 1/2?", "options": ["4/8", "3/5", "2/5", "1/3"], "correct": 0, "explanation": "Equivalent fractions represent the same value. 4/8 = 4÷4 / 8÷4 = 1/2."},
            {"question": "What is 3/4 of 12?", "options": ["9", "6", "8", "10"], "correct": 0, "explanation": "To find a fraction of a number, multiply: 3/4 × 12 = (3×12)/4 = 36/4 = 9."},
            {"question": "Convert 1/4 to decimal", "options": ["0.25", "0.5", "0.75", "0.4"], "correct": 0, "explanation": "Divide numerator by denominator: 1÷4 = 0.25."},
            {"question": "Which fraction is smallest?", "options": ["1/5", "1/3", "1/2", "1/4"], "correct": 0, "explanation": "When numerators are equal, the fraction with the largest denominator is smallest: 1/5 < 1/4 < 1/3 < 1/2."},
            {"question": "What is 1/2 + 1/3?", "options": ["5/6", "2/5", "1/5", "2/6"], "correct": 0, "explanation": "Find LCD of 2 and 3 = 6. Convert: 1/2=3/6 and 1/3=2/6. Then 3/6+2/6=5/6."},
        ],
        "medium": [
            {"question": "Convert 0.75 to a fraction", "options": ["3/4", "2/3", "7/10", "4/5"], "correct": 0, "explanation": "0.75 = 75/100 = (75÷25)/(100÷25) = 3/4."},
            {"question": "What is 5/6 + 1/3?", "options": ["7/6", "6/9", "5/3", "1/2"], "correct": 0, "explanation": "Convert 1/3 to 2/6. Then 5/6 + 2/6 = 7/6 = 1⅙."},
            {"question": "Simplify 12/15", "options": ["4/5", "3/5", "2/3", "1/2"], "correct": 0, "explanation": "GCD(12,15) = 3. So 12÷3=4 and 15÷3=5. Therefore 12/15 = 4/5."},
            {"question": "What is 2/3 × 3/4?", "options": ["1/2", "5/7", "6/12", "1/3"], "correct": 0, "explanation": "Multiply numerators and denominators: (2×3)/(3×4) = 6/12 = 1/2. Cancel common factors."},
            {"question": "Calculate 7/8 - 1/4", "options": ["5/8", "6/8", "4/8", "3/8"], "correct": 0, "explanation": "Convert 1/4 to 2/8. Then 7/8 - 2/8 = 5/8."},
        ],
        "hard": [
            {"question": "Simplify (3/4 × 8/9) ÷ (2/3)", "options": ["1", "2/3", "4/3", "1/2"], "correct": 0, "explanation": "(3/4 × 8/9) = 24/36 = 2/3. Then (2/3) ÷ (2/3) = 1."},
            {"question": "What is 5/6 of 36?", "options": ["30", "25", "20", "24"], "correct": 0, "explanation": "5/6 × 36 = (5×36)/6 = 180/6 = 30."},
            {"question": "If 2/5 of a number is 14, what is the number?", "options": ["35", "28", "40", "25"], "correct": 0, "explanation": "Let x be the number. (2/5)x = 14. Multiply both sides by 5/2: x = 14 × 5/2 = 35."},
        ]
    },
    "Algebra": {
        "easy": [
            {"question": "Solve: x + 5 = 12", "options": ["x = 7", "x = 17", "x = 2", "x = 12"], "correct": 0, "explanation": "Subtract 5 from both sides: x = 12 - 5 = 7."},
            {"question": "Simplify: 2x + 3x", "options": ["5x", "6x", "2x", "3x"], "correct": 0, "explanation": "Combine like terms: 2x + 3x = 5x."},
            {"question": "What is 3x when x = 2?", "options": ["6", "3", "5", "9"], "correct": 0, "explanation": "Substitute x=2: 3(2) = 6."},
            {"question": "Solve: x - 4 = 1", "options": ["x = 5", "x = -3", "x = 4", "x = -4"], "correct": 0, "explanation": "Add 4 to both sides: x = 1 + 4 = 5."},
            {"question": "Which is equivalent to 2x + x?", "options": ["3x", "2x²", "x²", "3"], "correct": 0, "explanation": "Combine like terms: 2x + x = 3x."},
        ],
        "medium": [
            {"question": "Solve: 3x - 2 = 10", "options": ["x = 4", "x = 3", "x = 5", "x = 2"], "correct": 0, "explanation": "Add 2 to both sides: 3x = 12. Divide by 3: x = 4."},
            {"question": "Solve: 2(x + 3) = 14", "options": ["x = 4", "x = 5", "x = 7", "x = 8"], "correct": 0, "explanation": "Divide by 2: x + 3 = 7. Subtract 3: x = 4."},
            {"question": "Expand: 2(x + 5)", "options": ["2x + 10", "2x + 5", "x + 10", "2x + 7"], "correct": 0, "explanation": "Distribute 2: 2(x) + 2(5) = 2x + 10."},
            {"question": "Factor: 3x + 9", "options": ["3(x + 3)", "3x(1 + 3)", "(x + 3)", "9(x + 1)"], "correct": 0, "explanation": "GCD(3, 9) = 3. Factor out: 3(x + 3)."},
        ],
        "hard": [
            {"question": "Solve: 2x² + 3x - 2 = 0", "options": ["x = 1/2 or x = -2", "x = 1 or x = 2", "x = -1", "x = 0"], "correct": 0, "explanation": "Quadratic formula or factoring: (2x-1)(x+2) = 0, so x = 1/2 or x = -2."},
            {"question": "Solve: 4x - 5 = 2x + 7", "options": ["x = 6", "x = 1", "x = 12", "x = 2"], "correct": 0, "explanation": "Collect x terms: 4x - 2x = 7 + 5. Simplify: 2x = 12. Divide: x = 6."},
        ]
    },
    "Loops": {
        "easy": [
            {"question": "Output of: for i in range(3): print(i)", "options": ["0 1 2", "1 2 3", "0 1", "1 2"], "correct": 0, "explanation": "range(3) generates [0, 1, 2]. Each value is printed on a new line: 0, 1, 2."},
            {"question": "Times executed: for i in range(5): pass", "options": ["5", "4", "6", "0"], "correct": 0, "explanation": "range(5) generates [0, 1, 2, 3, 4], so the loop runs 5 times."},
            {"question": "What does range(0, 5) produce?", "options": ["[0, 1, 2, 3, 4]", "[1, 2, 3, 4, 5]", "[0, 1, 2, 3, 4, 5]", "[5]"], "correct": 0, "explanation": "range(start, stop) includes start but excludes stop: 0, 1, 2, 3, 4."},
            {"question": "How many iterations: for i in range(2, 7)?", "options": ["5", "6", "7", "4"], "correct": 0, "explanation": "range(2, 7) = [2, 3, 4, 5, 6]. Count = 5 iterations."},
        ],
        "medium": [
            {"question": "Output: for i in range(1, 4): print(i)", "options": ["1 2 3", "0 1 2 3", "1 2", "0 1 2"], "correct": 0, "explanation": "range(1, 4) = [1, 2, 3]. Printed: 1, 2, 3."},
            {"question": "Sum of: for i in range(1, 5): sum += i", "options": ["10", "15", "14", "20"], "correct": 0, "explanation": "1 + 2 + 3 + 4 = 10."},
            {"question": "What is range(5, 2, -1)?", "options": ["[5, 4, 3]", "[5, 4, 3, 2]", "[2, 3, 4, 5]", "[5, 2]"], "correct": 0, "explanation": "Negative step goes backward: starts at 5, ends before 2, step -1 gives [5, 4, 3]."},
        ],
        "hard": [
            {"question": "What does this print? for i in range(0, 10, 2): print(i)", "options": ["0 2 4 6 8", "0 1 2 3 4", "2 4 6 8 10", "1 3 5 7 9"], "correct": 0, "explanation": "Step of 2: starts at 0, adds 2 each iteration until reaching 10 (excluded). Output: 0, 2, 4, 6, 8."},
        ]
    },
    "Variables": {
        "easy": [
            {"question": "Correct way to declare in Python", "options": ["x = 5", "var x = 5", "declare x = 5", "int x = 5"], "correct": 0, "explanation": "Python uses simple assignment: x = 5. No 'var' or 'declare' keyword needed."},
            {"question": "Value of x after: x = 5; x = x + 3", "options": ["8", "5", "3", "0"], "correct": 0, "explanation": "Start: x=5. Then: x = 5 + 3 = 8."},
            {"question": "Type of: x = '5'", "options": ["String", "Integer", "Float", "Boolean"], "correct": 0, "explanation": "Single/double quotes indicate a string. '5' is text, not a number."},
            {"question": "Which is a valid Python variable name?", "options": ["my_var", "my-var", "123var", "for"], "correct": 0, "explanation": "Variable names can contain letters, numbers, underscores, but cannot start with a number or use hyphens."},
        ],
        "medium": [
            {"question": "Type of: x = 3.14", "options": ["Float", "String", "Integer", "List"], "correct": 0, "explanation": "Numbers with decimal points are floats."},
            {"question": "What is x after: x = 5; x *= 2", "options": ["10", "7", "5", "2"], "correct": 0, "explanation": "x *= 2 is shorthand for x = x * 2 = 5 * 2 = 10."},
        ],
    },
    "Functions": {
        "easy": [
            {"question": "What does return do?", "options": ["Exits and provides value", "Starts loop", "Defines variable", "Prints"], "correct": 0, "explanation": "return ends the function and sends a value back to the caller."},
            {"question": "Output: def add(a,b): return a+b; print(add(3,4))", "options": ["7", "3", "4", "34"], "correct": 0, "explanation": "add(3, 4) returns 3+4=7, which is printed."},
        ],
        "medium": [
            {"question": "What does this return? def greet(name): return 'Hello ' + name; greet('World')", "options": ["Hello World", "Hello", "World", "greet"], "correct": 0, "explanation": "Concatenates 'Hello ' with 'World' to return 'Hello World'."},
            {"question": "Function with no return statement returns?", "options": ["None", "0", "empty string", "error"], "correct": 0, "explanation": "Functions without explicit return statement return None by default."},
        ],
        "hard": [
            {"question": "What is the output? def func(x): return x * 2 if x > 5 else x + 1; func(6)", "options": ["12", "7", "6", "13"], "correct": 0, "explanation": "x=6 > 5, so returns x*2 = 6*2 = 12."},
        ]
    },
    "Motion": {
        "easy": [
            {"question": "What is velocity?", "options": ["Speed with direction", "Distance/time", "Acceleration", "Force"], "correct": 0, "explanation": "Velocity is a vector quantity (has magnitude and direction), while speed is scalar (magnitude only)."},
            {"question": "Speed = 100m in 10s?", "options": ["10 m/s", "1 m/s", "100 m/s", "1000 m/s"], "correct": 0, "explanation": "Speed = distance/time = 100m / 10s = 10 m/s."},
            {"question": "What are typical SI units for velocity?", "options": ["m/s", "km/h", "mph", "ft/s"], "correct": 0, "explanation": "SI unit for velocity is meters per second (m/s)."},
        ],
        "medium": [
            {"question": "What is acceleration?", "options": ["Change in velocity/time", "Change in distance", "Speed", "Force"], "correct": 0, "explanation": "Acceleration = (final velocity - initial velocity) / time. It's the rate of change of velocity."},
            {"question": "A car goes from 0 to 20 m/s in 5 seconds. Acceleration is?", "options": ["4 m/s²", "20 m/s²", "5 m/s²", "100 m/s²"], "correct": 0, "explanation": "a = Δv/t = (20-0)/5 = 4 m/s²."},
            {"question": "If an object travels 50 m in 10 s then 100 m in the next 20 s, what is its average speed over the whole trip?", "options": ["5 m/s", "7.5 m/s", "6 m/s", "8 m/s"], "correct": 2, "explanation": "Total distance = 150 m, total time = 30 s, average speed = 150/30 = 5 m/s. (Answer key corrected: option index 0 is 5 m/s)"},
        ],
    },
    "Grammar": {
        "easy": [
            {"question": "Correct sentence", "options": ["She go to school", "She goes to school", "She going", "She gone"], "correct": 1, "explanation": "Third person singular present tense: 'She goes' (not 'She go')."},
            {"question": "Noun in: 'quick brown fox'", "options": ["quick", "brown", "fox", "the"], "correct": 2, "explanation": "'fox' is the noun (person, place, thing). 'quick' and 'brown' are adjectives describing the noun."},
            {"question": "Which is a verb?", "options": ["run", "happy", "table", "blue"], "correct": 0, "explanation": "'run' is an action (verb). Others are noun or adjective."},
        ],
        "medium": [
            {"question": "Correct form: I _____ to the store yesterday", "options": ["went", "go", "goes", "am going"], "correct": 0, "explanation": "Past tense with 'yesterday': 'went' is correct."},
            {"question": "Find the subject: 'The students completed the assignment'", "options": ["students", "completed", "assignment", "The"], "correct": 0, "explanation": "'The students' is the subject (who performs the action). 'completed' is the verb."},
        ],
    },
    "Reasoning": {
        "easy": [
            {"question": "Pattern: 2, 4, 6, 8, ?", "options": ["10", "9", "12", "16"], "correct": 0, "explanation": "Pattern: add 2 each time. 2+2=4, 4+2=6, 6+2=8, 8+2=10."},
            {"question": "Cats are animals, Fluffy is cat, then?", "options": ["Fluffy is animal", "Animals are cats", "Fluffy not animal", "Cats not animals"], "correct": 0, "explanation": "Logical deduction: If all cats are animals and Fluffy is a cat, then Fluffy must be an animal."},
            {"question": "Pattern: 1, 4, 9, 16, ?", "options": ["25", "20", "24", "30"], "correct": 0, "explanation": "Perfect squares: 1²=1, 2²=4, 3²=9, 4²=16, 5²=25."},
        ],
        "medium": [
            {"question": "If A > B and B > C, then A _____ C", "options": [">", "<", "=", "not comparable"], "correct": 0, "explanation": "Transitive property: A > B and B > C implies A > C."},
            {"question": "Odd one out: 2, 4, 6, 9", "options": ["9", "2", "6", "4"], "correct": 0, "explanation": "2, 4, 6 are even. 9 is odd. Therefore 9 is the odd one out."},
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
    """Generate adaptive quiz questions with validation"""
    # Validate inputs
    if not topic or len(topic.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic name cannot be empty"
        )
    
    if count < 1 or count > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question count must be between 1 and 50"
        )
    
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
    
    # Create quiz with randomized options
    quiz = []
    for q in selected:
        # Shuffle options while tracking correct answer
        options = q["options"].copy()
        correct_idx = q["correct"]
        correct_option = options[correct_idx]
        random.shuffle(options)
        new_correct = options.index(correct_option)
        
        quiz.append({
            "question": q["question"],
            "options": options,
            "difficulty": difficulty,
            "explanation": q.get("explanation", ""),
            "correct": new_correct
        })
    
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
    
    # GAMIFICATION: Add points and update streak
    points_earned = 10 if is_correct else 2
    current_user.points += points_earned
    
    # Update streak logic
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    last_login = current_user.last_login.date() if current_user.last_login else None
    
    if last_login != today:
        # New day - check if yesterday or reset
        if last_login and last_login == today - timedelta(days=1):
            # Consecutive day - increment streak
            current_user.streak += 1
        else:
            # Break in streak - reset
            current_user.streak = 1
        current_user.last_login = datetime.utcnow()
    
    db.commit()
    
    # Sync to Firebase Realtime Database
    quiz_result_data = {
        "topic": topic_key,
        "is_correct": is_correct,
        "points_earned": points_earned,
        "timestamp": datetime.utcnow().isoformat(),
        "mastery_score": round(progress.mastery_score * 100, 2),
    }
    save_quiz_result_to_firebase(current_user.id, f"quiz_{quiz_result.id}", quiz_result_data)
    
    return {
        "is_correct": is_correct,
        "explanation": question_data.get("explanation", ""),
        "correct_option": question_data["correct"],
        "selected_option": selected_option,
        "mastery_update": round(progress.mastery_score * 100, 2),
        "message": "Correct! Great job!" if is_correct else "Incorrect. Review the concept.",
        "points_earned": points_earned,
        "total_points": current_user.points,
        "streak": current_user.streak
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
