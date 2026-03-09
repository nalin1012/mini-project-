from sqlalchemy import Column, Integer, String, DateTime, Float,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role=Column(String,default="student") #student or teacher or admin
    name=Column(String)

class LearningProgress(Base):
    __tablename__ = 'learning_progress'
    id = Column(Integer, primary_key=True)
    
    student_id = Column(Integer, ForeignKey('users.id'))
    concept = Column(String)
    score = Column(Float)  # percentage of course completed
    last_updated = Column(DateTime)
    sessions_completed = Column(Integer, default=0)
    student=relationship("User", back_populates="progress")

class LearningSession(Base):
    __tablename__ = 'learning_sessions'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'))
    concept = Column(String)
    duration_minutes = Column(Integer)
    quiz_score = Column(Float)  # score for the session's quiz
    created_at = Column(DateTime)