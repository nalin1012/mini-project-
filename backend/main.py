from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import routers
from recommendations import router as recommendation_router

app = FastAPI(
    title="AI Personalized Learning Platform API",
    description="Backend API for AI-driven adaptive learning system",
    version="1.0"
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(recommendation_router)

@app.get("/")
def home():
    return {
        "message": "AI Personalized Learning Platform API is running"
    }