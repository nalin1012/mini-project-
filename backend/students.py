from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User
from auth import get_current_user

# Knowledge base for tutor responses
KNOWLEDGE_BASE = {
    "fractions": {
        "response": "Fractions represent parts of a whole. A fraction has a numerator (top number) and denominator (bottom number).",
        "explanation": "A fraction like 3/4 means 3 parts out of 4 equal parts. The numerator tells you how many parts you have, and the denominator tells you how many parts make up the whole. For example, if you cut a pizza into 8 slices and eat 3, you've eaten 3/8 of the pizza.",
        "examples": ["Adding fractions: 1/2 + 1/4 = 3/4", "Converting to decimals: 1/2 = 0.5", "Simplifying: 4/8 = 1/2"]
    },
    "algebra": {
        "response": "Algebra is a branch of mathematics that uses letters (like x and y) to represent unknown numbers in equations.",
        "explanation": "Algebra helps you solve problems where some information is missing. Instead of just working with numbers, you use variables to represent unknowns and write equations to find their values. For example, if x + 5 = 12, then x = 7.",
        "examples": ["Solving equations: 2x + 3 = 11 (answer: x = 4)", "Writing expressions for real situations", "Using variables to find missing values"]
    },
    "geometry": {
        "response": "Geometry is the study of shapes, sizes, and properties of space and figures.",
        "explanation": "Geometry deals with points, lines, angles, and shapes like triangles, circles, and squares. It helps us understand the physical world around us and solve real problems about distance, area, and volume.",
        "examples": ["Finding the area of a rectangle: length × width", "Using Pythagorean theorem: a² + b² = c²", "Calculating circumference of a circle: 2πr"]
    },
    "calculus": {
        "response": "Calculus is the mathematics of change. It includes derivatives and integrals to study rates of change and accumulation.",
        "explanation": "Calculus helps us understand how things change over time. Derivatives measure rates of change (like speed or growth rate), while integrals measure accumulation (like total distance or area under a curve). It's used in physics, engineering, and economics.",
        "examples": ["Finding derivative of f(x) = 2x²", "Calculating area under a curve using integration", "Finding maximum/minimum values of functions"]
    },
    "science": {
        "response": "Science is the systematic study of the natural world through observation and experimentation.",
        "explanation": "Science helps us understand how things work by testing ideas and gathering evidence. Main branches include physics, chemistry, and biology. The scientific method involves making observations, forming hypotheses, conducting experiments, and drawing conclusions.",
        "examples": ["Understanding how plants grow through photosynthesis", "Learning why objects fall (gravity)", "Studying how medicines work in the body"]
    },
    "physics": {
        "response": "Physics is the study of matter, energy, and forces, and how they interact.",
        "explanation": "Physics explains how the universe works at all scales, from tiny atoms to massive galaxies. It includes mechanics (motion and forces), thermodynamics (heat and temperature), waves, electricity, magnetism, and modern physics.",
        "examples": ["Newton's laws of motion", "Conservation of energy", "Speed, velocity, and acceleration calculations"]
    },
    "chemistry": {
        "response": "Chemistry is the study of substances, their reactions, and the bonds between atoms.",
        "explanation": "Chemistry explains what things are made of and how they change through reactions. It covers atoms, molecules, chemical bonding, and reactions like combustion, oxidation, and synthesis.",
        "examples": ["Understanding water (H₂O) as hydrogen and oxygen bonded together", "Combustion reactions: burning fuel produces heat and CO₂", "Acid-base reactions: mixing vinegar and baking soda"]
    },
    "biology": {
        "response": "Biology is the study of living organisms and life processes.",
        "explanation": "Biology helps us understand how living things work, grow, and interact with each other and their environment. It includes cell biology, genetics, ecology, evolution, and human anatomy.",
        "examples": ["Understanding how cells reproduce through mitosis", "Learning about DNA and heredity", "Studying ecosystems and food chains"]
    },
    "evolution": {
        "response": "Evolution is the process by which organisms change and adapt over time through natural selection.",
        "explanation": "Evolution explains how all life on Earth is connected and how species change over millions of years. It's based on the idea that organisms with traits better suited to their environment are more likely to survive and reproduce, passing those traits to offspring.",
        "examples": ["Darwin's finches adapting beak shapes to different food sources", "Peppered moths changing color during industrial revolution", "Humans and primates sharing common ancestors"]
    },
    "english": {
        "response": "English is the study of language, literature, and communication skills.",
        "explanation": "English develops reading, writing, and speaking skills. It includes grammar, vocabulary, poetry, novels, essays, and literary analysis. Good communication skills are essential for success in school and career.",
        "examples": ["Writing persuasive essays with strong arguments", "Analyzing themes and symbolism in literature", "Learning grammar rules for clear writing"]
    },
    "history": {
        "response": "History is the study of past events and how they shaped our world.",
        "explanation": "History helps us understand how societies evolved and why things are the way they are today. It teaches us about different cultures, important events, and influential people throughout time.",
        "examples": ["Ancient Egyptian civilization and pyramids", "The Industrial Revolution and its impact", "World wars and their consequences"]
    },
    "math": {
        "response": "Mathematics is the study of numbers, quantities, and patterns.",
        "explanation": "Math helps us understand relationships between quantities and solve real-world problems. It includes arithmetic, algebra, geometry, calculus, and statistics.",
        "examples": ["Calculating interest on savings", "Designing structures using geometry", "Analyzing data trends with statistics"]
    }
}


router = APIRouter(prefix="/api/tutor", tags=["tutor"])

class TutorRequest(BaseModel):
    message: str
    context: str | None = None

class TutorResponse(BaseModel):
    response: str
    explanation: str
    examples: list[str]

@router.post("/ask", response_model=TutorResponse)
async def ask_tutor(
    request: TutorRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI Tutor endpoint - provides interactive learning explanations and examples
    """
    
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide a question"
        )
    
    question = request.message.lower().strip()
    context = (request.context or "").lower() if request.context else ""
    search_text = f"{question} {context}"
    
    # Find best matching topic from knowledge base
    matched_topic = None
    best_score = 0
    
    for topic in KNOWLEDGE_BASE.keys():
        if topic in search_text:
            score = len(topic)
            if score > best_score:
                best_score = score
                matched_topic = topic
    
    # Provide response from knowledge base
    if matched_topic:
        data = KNOWLEDGE_BASE[matched_topic]
        
        # Make response more interactive based on question type
        response = data["response"]
        
        # Detect question type and customize response
        if "why" in question or "how" in question:
            response = f"Great question! {response}"
        elif "what" in question or "define" in question or "explain" in question:
            response = f"Excellent! Let me explain: {response}"
        elif "calculate" in question or "solve" in question:
            response = f"Perfect! To solve this: {response}"
        else:
            response = f"I love your curiosity! {response}"
        
        return TutorResponse(
            response=response,
            explanation=data["explanation"],
            examples=data["examples"]
        )
    
    # Enhanced generic response with interactive prompts
    # Try to extract keywords from the question
    question_words = question.split()
    keywords = [w for w in question_words if len(w) > 3]
    keyword_phrase = " and ".join(keywords[:2]) if keywords else "that concept"
    
    return TutorResponse(
        response=f"Interesting! I can help you learn about {keyword_phrase}.",
        explanation=f"Your question about '{question[:50]}' is a great topic to explore. To understand this better:\n\n1️⃣ Start with the basics - what do you already know about it?\n2️⃣ Break it into smaller parts\n3️⃣ Connect it to real-world examples you know\n4️⃣ Practice with problems or examples\n\nWhat specific part would you like to dive deeper into?",
        examples=[
            "💡 Ask me to explain one specific concept",
            "📝 Ask for real-world examples or applications",
            "🎯 Ask for practice problems or step-by-step solutions"
        ]
    )
