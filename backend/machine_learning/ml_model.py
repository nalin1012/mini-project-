import pandas as pd
import random
import joblib

# Load trained model
model = joblib.load("machine_learning/knowledge_gap_model.pkl")

quiz_bank = {
    "Fractions":[
        "What is 1/2 + 1/4?",
        "Convert 0.5 into fraction",
        "Simplify 2/4"
    ],
    "Algebra":[
        "Solve x + 5 = 10",
        "Simplify 2x + 3x"
    ]
}

def analyze_student(concept, correct, total, time_spent):

    mastery = correct / total

    input_data = pd.DataFrame({
        "correct_answers":[correct],
        "total_questions":[total],
        "time_spent":[time_spent]
    })

    gap = model.predict(input_data)[0]

    recommendation = "Revise concept" if gap else "Move to next topic"

    quiz = random.sample(
        quiz_bank.get(concept, []),
        min(2, len(quiz_bank.get(concept, [])))
    )

    return {
        "mastery_score": round(mastery,2),
        "knowledge_gap": int(gap),
        "recommendation": recommendation,
        "quiz": quiz
    }