import random

# Quiz bank - knowledge gap recommendations
quiz_bank = {
    "Fractions":[
        "What is 1/2 + 1/4?",
        "Convert 0.5 into fraction",
        "Simplify 2/4"
    ],
    "Algebra":[
        "Solve x + 5 = 10",
        "Simplify 2x + 3x"
    ],
    "Geometry": [
        "What is the area of a circle with radius 5?",
        "Calculate the perimeter of a rectangle"
    ],
    "Statistics": [
        "What is the mean of 2, 4, 6, 8?",
        "Calculate the median of 1, 3, 5, 7, 9"
    ]
}

def analyze_student(concept, correct, total, time_spent):
    """
    Analyze student performance and provide recommendations.
    Simple rule-based system without ML model.
    """
    # Calculate mastery score
    mastery = correct / total if total > 0 else 0
    
    # Determine if there's a knowledge gap (threshold: 70%)
    has_gap = mastery < 0.7
    
    # Create recommendation based on performance
    if mastery >= 0.9:
        recommendation = "Excellent! Move to advanced topics"
        gap_score = 0
    elif mastery >= 0.7:
        recommendation = "Good progress! Review a few more topics"
        gap_score = 1
    elif mastery >= 0.5:
        recommendation = "Revise this concept with more practice"
        gap_score = 2
    else:
        recommendation = "Need significant practice on this concept"
        gap_score = 3
    
    # Get recommended quiz questions
    quiz = random.sample(
        quiz_bank.get(concept, ["No quiz available for this topic"]),
        min(2, len(quiz_bank.get(concept, [])))
    )
    
    return {
        "mastery_score": round(mastery, 2),
        "knowledge_gap": gap_score,
        "recommendation": recommendation,
        "quiz": quiz
    }