from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool
import os
import logging

# SQLite database URL (can be changed to PostgreSQL later)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./learning_platform.db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./learning_platform.db")

# Convert postgresql:// to postgresql+psycopg:// for SQLAlchemy with psycopg3
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

logger = logging.getLogger(__name__)

# Configure engine options (pooling only where it applies)
engine_kwargs = {
    "connect_args": {"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    "pool_pre_ping": True,
    "echo": False,
}

if "postgresql" in DATABASE_URL:
    engine_kwargs.update(
        {
            "poolclass": QueuePool,
            "pool_size": 10,
            "max_overflow": 20,
        }
    )

engine = create_engine(DATABASE_URL, **engine_kwargs)

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
    logger.info("Database tables initialized successfully")
