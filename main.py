from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/api/progress/{student_id}")
def get_progress(student_id: int, db: Session = Depends(get_db)):
    progress = db.query(models.LearningProgress).filter(
        models.LearningProgress.student_id == student_id
    ).all()
    return [{"concept": p.concept, "progress": p.progress} for p in progress]
