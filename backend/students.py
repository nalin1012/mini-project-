from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User
from auth import get_current_user

router = APIRouter(prefix="/api/tutor", tags=["tutor"])

class TutorMessage(BaseModel):
    message: str
    context: Optional[str] = None  # Topic context

class TutorResponse(BaseModel):
    response: str
    explanation: str
    examples: list
    tips: list

# Knowledge base for AI Tutor
TUTOR_KNOWLEDGE_BASE = {
    "fractions": {
        "keywords": ["fraction", "numerator", "denominator", "simplify", "add", "subtract"],
        "responses": {
            "What are fractions?": "Fractions represent parts of a whole. A fraction has two numbers: the numerator (top) and denominator (bottom). For example, 1/2 means 1 part out of 2 equal parts.",
            "How do I add fractions?": "To add fractions with the same denominator, add the numerators and keep the denominator. For example: 1/4 + 2/4 = 3/4. For different denominators, find the common denominator first.",
            "How do I simplify fractions?": "To simplify a fraction, divide both numerator and denominator by their greatest common divisor (GCD). For example: 6/9 = 2/3 (divide by 3).",
        },
        "examples": [
            "1/2 + 1/4 = 3/4",
            "6/9 simplified is 2/3",
            "1/3 + 1/3 = 2/3"
        ]
    },
    "algebra": {
        "keywords": ["equation", "solve", "variable", "linear", "expression"],
        "responses": {
            "What is algebra?": "Algebra uses symbols (usually letters) to represent unknown numbers and to describe relationships between quantities. We use variables like 'x' to stand for unknown values.",
            "How do I solve an equation?": "To solve an equation, isolate the variable on one side. Use inverse operations: if it's addition, subtract; if multiplication, divide. For example: x + 5 = 12 → x = 12 - 5 = 7",
            "What are variables?": "Variables are symbols (usually letters like x, y, z) that represent unknown or changing quantities. They let us write general rules instead of specific numbers.",
        },
        "examples": [
            "x + 5 = 12 → x = 7",
            "2x = 10 → x = 5",
            "3x - 2 = 10 → 3x = 12 → x = 4"
        ]
    },
    "loops": {
        "keywords": ["loop", "for", "while", "iteration", "repeat"],
        "responses": {
            "What are loops?": "Loops allow us to repeat a block of code multiple times. There are two main types: for loops (for a set number of times) and while loops (while a condition is true).",
            "How does a for loop work?": "A for loop repeats code for each item in a sequence. For example: for i in range(3): print(i) will print 0, 1, 2",
            "What is a while loop?": "A while loop repeats as long as a condition is true. For example: while i < 5: i += 1 will repeat until i equals 5. Be careful not to create infinite loops!",
        },
        "examples": [
            "for i in range(5): print(i)  # prints 0-4",
            "while x < 10: x += 1",
            "for item in list: process(item)"
        ]
    },
    "variables": {
        "keywords": ["variable", "assign", "data type", "name"],
        "responses": {
            "What are variables?": "Variables are containers that store data. In Python, you create a variable by assigning a value: x = 5",
            "How do I name variables?": "Variable names should be descriptive and start with a letter or underscore. Use lowercase with underscores for multi-word names: student_name = 'Ali'",
            "What are data types?": "Common data types are: integers (5), floats (5.5), strings ('hello'), and booleans (True/False).",
        },
        "examples": [
            "x = 5  # integer",
            "name = 'Ali'  # string",
            "price = 19.99  # float"
        ]
    },
    "functions": {
        "keywords": ["function", "define", "return", "parameter", "argument"],
        "responses": {
            "What are functions?": "Functions are reusable blocks of code that perform a specific task. You define them with 'def' and call them by name.",
            "How do I define a function?": "Use the def keyword: def greet(name): return 'Hello, ' + name",
            "What are parameters?": "Parameters are the inputs to a function. When you call the function, you provide arguments (values) for these parameters.",
        },
        "examples": [
            "def add(a, b): return a + b",
            "def greet(name): return f'Hello, {name}'",
            "def square(x): return x * x"
        ]
    }
}

def get_tutor_response(message: str, context: Optional[str] = None) -> TutorResponse:
    """
    Get AI tutor response based on user message
    Uses rule-based system (can be upgraded to LLM later)
    """
    message_lower = message.lower()
    
    # Determine topic from context or message
    topic = context.lower() if context else None
    
    # Search for matching topic
    if not topic:
        for t in TUTOR_KNOWLEDGE_BASE.keys():
            if t in message_lower:
                topic = t
                break
    
    # Default to general response if no topic found
    if not topic or topic not in TUTOR_KNOWLEDGE_BASE:
        return TutorResponse(
            response="I'm here to help! Ask me about Fractions, Algebra, Loops, Variables, or Functions.",
            explanation="Please specify a topic you'd like help with.",
            examples=["What are fractions?", "How do I solve equations?", "Explain loops"],
            tips=["Be specific about what you want to learn", "Ask follow-up questions", "Practice with examples"]
        )
    
    knowledge = TUTOR_KNOWLEDGE_BASE[topic]
    
    # Find specific response
    response_text = None
    for key, value in knowledge["responses"].items():
        if any(keyword in message_lower for keyword in key.lower().split()):
            response_text = value
            break
    
    # Default response for the topic if no specific match
    if not response_text:
        response_text = f"Great question about {topic}! Let me help you understand this concept better."
    
    return TutorResponse(
        response=response_text,
        explanation=f"This is a common question in {topic}. Understanding this will help you solve many problems.",
        examples=knowledge["examples"][:3],
        tips=[
            f"Practice with more {topic} problems",
            "Work through examples step by step",
            "Try solving similar problems on your own"
        ]
    )

@router.post("/ask", response_model=TutorResponse)
async def ask_tutor(
    tutor_msg: TutorMessage,
    current_user: User = Depends(get_current_user)
):
    """
    Ask the AI tutor a question
    """
    if not tutor_msg.message or len(tutor_msg.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    response = get_tutor_response(tutor_msg.message, tutor_msg.context)
    return response

@router.get("/topics")
async def get_available_topics(
    current_user: User = Depends(get_current_user)
):
    """Get list of topics the tutor can help with"""
    return {
        "topics": list(TUTOR_KNOWLEDGE_BASE.keys()),
        "description": "Ask me about any of these topics and I'll help you learn!",
        "example_questions": [
            "What are fractions?",
            "How do I solve equations?",
            "How do loops work?",
            "What are variables?",
            "How do I write functions?"
        ]
    }

@router.get("/explain/{topic}")
async def explain_topic(
    topic: str,
    current_user: User = Depends(get_current_user)
):
    """Get explanation for a specific topic"""
    topic_lower = topic.lower()
    
    if topic_lower not in TUTOR_KNOWLEDGE_BASE:
        raise HTTPException(
            status_code=404,
            detail=f"Topic '{topic}' not found. Available topics: {list(TUTOR_KNOWLEDGE_BASE.keys())}"
        )
    
    knowledge = TUTOR_KNOWLEDGE_BASE[topic_lower]
    
    # Get first response as main explanation
    main_response = list(knowledge["responses"].values())[0]
    
    return {
        "topic": topic,
        "explanation": main_response,
        "related_questions": list(knowledge["responses"].keys()),
        "examples": knowledge["examples"],
        "tips": [
            "Start with the basics",
            "Practice with these examples",
            "Ask me any follow-up questions"
        ]
    }

@router.post("/practice-hint/{topic}")
async def get_practice_hint(
    topic: str,
    current_user: User = Depends(get_current_user)
):
    """Get a hint for practicing a topic"""
    topic_lower = topic.lower()
    
    if topic_lower not in TUTOR_KNOWLEDGE_BASE:
        raise HTTPException(
            status_code=404,
            detail=f"Topic '{topic}' not found"
        )
    
    knowledge = TUTOR_KNOWLEDGE_BASE[topic_lower]
    
    return {
        "topic": topic,
        "hint": f"Let's practice {topic}! Try to solve this problem step by step.",
        "practice_example": knowledge["examples"][0] if knowledge["examples"] else "Practice available",
        "steps_to_solve": [
            "Read the problem carefully",
            "Identify what you know",
            "Plan your approach",
            "Solve step by step",
            "Check your answer"
        ]
    }
