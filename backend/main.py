from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
import logging
from dotenv import load_dotenv

# Configure logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Get environment variables
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Parse CORS origins from environment variable
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
cors_origins = [url.strip() for url in cors_origins_str.split(",")]

logger.info(f"Environment: {ENVIRONMENT}")
logger.info(f"Allowed CORS origins: {cors_origins}")

# Import routers
from auth import router as auth_router
from quiz import router as quiz_router
from progress import router as progress_router
from students import router as tutor_router
from recommendations import router as recommendation_router
from users import router as users_router
from admin import router as admin_router
from firebase_service import router as firebase_router
from tutor import router as tutor_chat_router
from chapters import router as chapters_router
from notes import router as notes_router
from database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="AI Personalized Learning Platform API",
    description="Backend API for AI-driven adaptive learning system with knowledge gap detection",
    version="2.0",
    docs_url="/api/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/api/redoc" if ENVIRONMENT == "development" else None
)

# CORS middleware - enable frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Initialize database
@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialized successfully")

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(quiz_router)
app.include_router(progress_router)
app.include_router(tutor_router)
app.include_router(recommendation_router)
app.include_router(firebase_router)
app.include_router(tutor_chat_router)
app.include_router(chapters_router)
app.include_router(notes_router)

@app.get("/")
def home():
    """Root endpoint"""
    return {
        "message": "AI Personalized Learning Platform API",
        "version": "2.0",
        "docs": "/api/docs",
        "status": "running"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Learning Platform API"
    }

@app.get("/api/subjects")
def get_subjects():
    """Get available subjects"""
    return {
        "subjects": [
            {"name": "Math", "icon": "Calculator", "description": "Build strong foundations in algebra and reasoning."},
            {"name": "Science", "icon": "FlaskConical", "description": "Explore physics, chemistry, and biology."},
            {"name": "Programming", "icon": "Code2", "description": "Learn modern coding skills."},
            {"name": "English", "icon": "Languages", "description": "Boost comprehension and writing."},
            {"name": "Aptitude", "icon": "Brain", "description": "Sharpen logic and reasoning."},
        ]
    }

@app.get("/api/subjects/{subject}/overview")
def get_subject_overview(subject: str):
    """Get detailed overview of a specific subject with topics and content"""
    try:
        from subject_content import get_subject_content, get_topic_content
        
        subject_data = get_subject_content(subject)
        
        return {
            "subject": subject,
            "overview": subject_data.get("overview", ""),
            "topics": subject_data.get("topics", []),
            "content_available": bool(subject_data.get("content", {})),
            "num_topics": len(subject_data.get("content", {}))
        }
    except Exception as e:
        logger.error(f"Error getting subject overview: {e}")
        return {
            "subject": subject,
            "overview": f"Learning material for {subject}",
            "topics": [],
            "content_available": False,
            "error": str(e)
        }

@app.get("/api/subjects/{subject}/topics/{topic}")
def get_subject_topic(subject: str, topic: str):
    """Get detailed content for a specific topic in a subject"""
    try:
        from subject_content import get_topic_content
        
        content = get_topic_content(subject, topic)
        
        return {
            "subject": subject,
            "topic": topic,
            "explanation": content.get("explanation", ""),
            "keyPoints": content.get("key_points", []),
            "formulas": content.get("formulas", []),
            "realLife": content.get("real_life", ""),
            "flashcards": content.get("flashcards", [])
        }
    except Exception as e:
        logger.error(f"Error getting topic content: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)