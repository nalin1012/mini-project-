from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Login History Schemas
class LoginHistoryResponse(BaseModel):
    id: int
    user_id: int
    login_time: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    login_method: str

    class Config:
        from_attributes = True

# User Management Schemas
class UserDetailResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool
    total_quizzes: int = 0
    overall_accuracy: float = 0.0

    class Config:
        from_attributes = True

class UsersListResponse(BaseModel):
    total: int
    users: List[UserDetailResponse]

# Admin Dashboard Schemas
class LoginStatsResponse(BaseModel):
    total_users: int
    active_today: int
    total_logins: int
    average_logins_per_user: float

class RecentLoginResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    login_time: datetime
    ip_address: Optional[str] = None
    login_method: str

class AdminDashboardResponse(BaseModel):
    total_users: int
    total_quizzes: int
    average_accuracy: float
    total_logins: int
    recent_logins: List[RecentLoginResponse]
    users: List[UserDetailResponse]
    login_stats: LoginStatsResponse

# Subject Schemas
class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: str = "BookOpen"

class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True

# Topic Schemas
class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None
    difficulty: str = "easy"

class TopicResponse(TopicBase):
    id: int
    subject_id: int

    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    options: List[str]
    correct_option: int
    difficulty: str = "medium"
    explanation: Optional[str] = None

class QuestionResponse(QuestionBase):
    id: int
    topic_id: int

    class Config:
        from_attributes = True

# Quiz Schemas
class QuizAnswerSubmit(BaseModel):
    topic: str  # Topic name like "Fractions", "Algebra"
    question_index: int  # Index in the question list
    selected_option: int  # Selected answer index
    time_taken: int = 0  # seconds

class QuizResultResponse(BaseModel):
    is_correct: bool
    explanation: str
    mastery_update: float

    class Config:
        from_attributes = True

# Learning Progress Schemas
class LearningProgressResponse(BaseModel):
    id: int
    student_id: int
    concept: str
    mastery_score: float
    sessions_completed: int
    correct_answers: int
    total_questions_attempted: int

    class Config:
        from_attributes = True

# Weak Area Schemas
class WeakAreaResponse(BaseModel):
    id: int
    student_id: int
    topic_id: int
    mastery_score: float
    total_attempts: int
    correct_attempts: int
    last_tested: datetime

    class Config:
        from_attributes = True

# Knowledge Gap Detection Response
class KnowledgeGapResponse(BaseModel):
    topic_name: str
    mastery_score: float
    weak_area: bool
    recommendation: str
    suggested_next_step: str

# Dashboard Stat
class DashboardStat(BaseModel):
    label: str
    value: str
    icon: str

# Dashboard Response
class DashboardResponse(BaseModel):
    user_name: str
    stats: List[DashboardStat]
    weak_areas: List[KnowledgeGapResponse]
    total_quizzes_completed: int
    overall_accuracy: float
