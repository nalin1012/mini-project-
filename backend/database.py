from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool
import os

# SQLite database URL (can be changed to PostgreSQL later)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./learning_platform.db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./learning_platform.db")

# Configure connection pooling for better performance
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    poolclass=QueuePool if "postgresql" in DATABASE_URL else None,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def init_db():
    """Create all database tables (only if they don't exist)"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables initialized successfully")
