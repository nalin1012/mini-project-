from machine_learning.ml_model import analyze_student

from fastapi import APIRouter
from machine_learning.ml_model import analyze_student

router = APIRouter(prefix="/api/recommendations")

@router.get("/analyze")

def analyze():

    result = analyze_student(
        concept="Fractions",
        correct=2,
        total=5,
        time_spent=120
    )

    return result