import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your app
import sys
sys.path.insert(0, '/backend')

from main import app
from database import Base, get_db
from models import User

# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAPI:
    """Test suite for API endpoints"""

    def test_root_endpoint(self):
        """Test GET /"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "AI Personalized Learning Platform API"

    def test_health_check(self):
        """Test GET /api/health"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_get_subjects(self):
        """Test GET /api/subjects"""
        response = client.get("/api/subjects")
        assert response.status_code == 200
        data = response.json()
        assert "subjects" in data
        assert len(data["subjects"]) == 5

    def test_register_user(self):
        """Test POST /api/auth/register"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@test.com",
                "password": "testpass123",
                "name": "Test User"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@test.com"
        assert data["user"]["name"] == "Test User"

    def test_duplicate_registration(self):
        """Test duplicate registration fails"""
        # First registration
        client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@test.com",
                "password": "pass123",
                "name": "User 1"
            }
        )
        
        # Second registration with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@test.com",
                "password": "pass456",
                "name": "User 2"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_login_user(self):
        """Test POST /api/auth/login"""
        # Register first
        client.post(
            "/api/auth/register",
            json={
                "email": "login@test.com",
                "password": "loginpass123",
                "name": "Login Test"
            }
        )
        
        # Then login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "login@test.com",
                "password": "loginpass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "login@test.com"

    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "wrong@test.com",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401

    def test_quiz_generation(self):
        """Test GET /api/quiz/generate/{subject}/{topic}"""
        # Register and get token
        reg_response = client.post(
            "/api/auth/register",
            json={
                "email": "quiz@test.com",
                "password": "quizpass",
                "name": "Quiz Tester"
            }
        )
        token = reg_response.json()["access_token"]
        
        # Generate quiz
        response = client.get(
            "/api/quiz/generate/Math/Fractions?count=5",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Fractions"
        assert data["subject"] == "Math"
        assert len(data["questions"]) > 0

    def test_quiz_invalid_topic(self):
        """Test quiz generation with invalid topic"""
        # Register and get token
        reg_response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid@test.com",
                "password": "pass",
                "name": "Test"
            }
        )
        token = reg_response.json()["access_token"]
        
        # Try invalid topic
        response = client.get(
            "/api/quiz/generate/Math/InvalidTopic",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 404

    def test_tutor_topics(self):
        """Test GET /api/tutor/topics"""
        # Register and get token
        reg_response = client.post(
            "/api/auth/register",
            json={
                "email": "tutor@test.com",
                "password": "tutorpass",
                "name": "Tutor Test"
            }
        )
        token = reg_response.json()["access_token"]
        
        response = client.get(
            "/api/tutor/topics",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "topics" in data
        assert len(data["topics"]) > 0

    def test_tutor_explain_topic(self):
        """Test GET /api/tutor/explain/{topic}"""
        # Register and get token
        reg_response = client.post(
            "/api/auth/register",
            json={
                "email": "explain@test.com",
                "password": "pass",
                "name": "Test"
            }
        )
        token = reg_response.json()["access_token"]
        
        response = client.get(
            "/api/tutor/explain/fractions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "topic" in data
        assert "explanation" in data

    def test_dashboard_summary(self):
        """Test GET /api/knowledge-gap/dashboard-summary"""
        # Register and get token
        reg_response = client.post(
            "/api/auth/register",
            json={
                "email": "dashboard@test.com",
                "password": "pass",
                "name": "Dashboard Test"
            }
        )
        token = reg_response.json()["access_token"]
        
        response = client.get(
            "/api/knowledge-gap/dashboard-summary",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user_name" in data
        assert "total_quizzes_completed" in data
        assert "overall_accuracy" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
