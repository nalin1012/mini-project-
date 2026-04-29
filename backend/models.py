from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="student")  # student, teacher, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    firebase_uid = Column(String, nullable=True, unique=True)  # Firebase UID
    points = Column(Integer, default=0)  # Gamification: total points
    streak = Column(Integer, default=0)  # Gamification: daily login streak
    
    # Relationships
    progress = relationship("LearningProgress", back_populates="student", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="student", cascade="all, delete-orphan")
    weak_areas = relationship("WeakArea", back_populates="student", cascade="all, delete-orphan")
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")

class LoginHistory(Base):
    __tablename__ = 'login_history'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    login_time = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    login_method = Column(String, default="password")  # password, firebase, oauth
    
    user = relationship("User", back_populates="login_history")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Math, Science, Programming, English, Aptitude
    description = Column(Text, nullable=True)
    icon = Column(String, default="BookOpen")

class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    name = Column(String, nullable=False)  # Fractions, Algebra, etc.
    description = Column(Text, nullable=True)
    difficulty = Column(String, default="easy")  # easy, medium, hard

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # ["option1", "option2", "option3", "option4"]
    correct_option = Column(Integer, nullable=False)  # 0-3
    difficulty = Column(String, default="medium")  # easy, medium, hard
    explanation = Column(Text, nullable=True)

class LearningProgress(Base):
    __tablename__ = 'learning_progress'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    concept = Column(String, nullable=False)
    mastery_score = Column(Float, default=0.0)  # 0-1
    last_updated = Column(DateTime, default=datetime.utcnow)
    sessions_completed = Column(Integer, default=0)
    total_questions_attempted = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    
    student = relationship("User", back_populates="progress")

class LearningSession(Base):
    __tablename__ = 'learning_sessions'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    duration_minutes = Column(Integer, default=0)
    questions_attempted = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    session_score = Column(Float, default=0.0)  # percentage
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizResult(Base):
    __tablename__ = 'quiz_results'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    selected_option = Column(Integer, nullable=False)  # 0-3
    is_correct = Column(Boolean, nullable=False)
    time_taken = Column(Integer, default=0)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("User", back_populates="quiz_results")

class WeakArea(Base):
    __tablename__ = 'weak_areas'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    mastery_score = Column(Float, default=0.0)  # 0-1, low = weak area
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    last_tested = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("User", back_populates="weak_areas")