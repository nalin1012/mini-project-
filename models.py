from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)

class LearningProgress(Base):
    __tablename__ = "learning_progress"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    concept = Column(String)
    progress = Column(Float)
    last_updated = Column(DateTime, default=datetime.now)