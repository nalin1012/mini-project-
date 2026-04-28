from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import routers
from auth import router as auth_router
from quiz import router as quiz_router
from progress import router as progress_router
from students import router as tutor_router
from recommendations import router as recommendation_router
from users import router as users_router
from admin import router as admin_router
from firebase_service import router as firebase_router
from database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="AI Personalized Learning Platform API",
    description="Backend API for AI-driven adaptive learning system with knowledge gap detection",
    version="2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware - enable frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(quiz_router)
app.include_router(progress_router)
app.include_router(tutor_router)
app.include_router(recommendation_router)
app.include_router(firebase_router)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)