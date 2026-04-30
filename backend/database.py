from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
import os
import logging
import time
import re

logger = logging.getLogger(__name__)

# ============================================
# DATABASE URL CONFIGURATION & VALIDATION
# ============================================

def validate_and_prepare_database_url(url: str) -> tuple[str, bool]:
    """
    Validate and prepare database URL with proper error handling
    Returns: (validated_url, is_postgresql)
    """
    if not url or url.strip() == "":
        logger.warning("DATABASE_URL is empty, using SQLite fallback")
        return "sqlite:///./learning_platform.db", False
    
    url = url.strip()
    
    # Check for malformed URLs (contains placeholder words)
    if "host" in url.lower() or "password" in url.lower() or "user" in url.lower():
        if url.count("://") == 0 or "@" not in url:
            logger.error(f"DATABASE_URL appears to be a template, not a real connection string")
            logger.info("Using SQLite fallback. Please set a real DATABASE_URL in Render environment variables")
            return "sqlite:///./learning_platform.db", False
        
        # Additional check: if the host is literally "host" or a placeholder
        # Extract host part (after @ and before :)
        host_match = re.search(r'@([^:/]+)', url)
        if host_match:
            host_part = host_match.group(1).lower()
            if host_part in ['host', 'localhost', 'your-host', 'db', 'database']:
                logger.error(f"DATABASE_URL host '{host_part}' appears to be a placeholder, not a real hostname")
                logger.info("Using SQLite fallback. Please set a real DATABASE_URL in Render environment variables")
                return "sqlite:///./learning_platform.db", False
    
    # Check if PostgreSQL URL
    is_postgresql = "postgresql" in url
    
    if is_postgresql:
        # Validate PostgreSQL URL format
        if "@" not in url or "/" not in url:
            logger.error("Invalid PostgreSQL URL format. Should be: postgresql://user:password@host:port/dbname")
            return "sqlite:///./learning_platform.db", False
        
        # Convert postgresql:// to postgresql+psycopg:// for SQLAlchemy with psycopg3
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        
        logger.info("Using PostgreSQL database")
        return url, True
    
    elif "sqlite" in url:
        logger.info("Using SQLite database")
        return url, False
    
    else:
        logger.warning(f"Unknown database type, using SQLite fallback")
        return "sqlite:///./learning_platform.db", False


# Get and validate DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./learning_platform.db")
DATABASE_URL, IS_POSTGRESQL = validate_and_prepare_database_url(DATABASE_URL)

logger.info(f"Database type: {'PostgreSQL' if IS_POSTGRESQL else 'SQLite'}")

# ============================================
# SQLALCHEMY ENGINE CONFIGURATION
# ============================================

try:
    engine_kwargs = {
        "pool_pre_ping": True,
        "echo": False,
        "future": True,
    }
    
    if "sqlite" in DATABASE_URL:
        # SQLite configuration
        engine_kwargs.update({
            "connect_args": {"check_same_thread": False},
            "poolclass": NullPool,  # SQLite doesn't benefit from connection pooling
        })
    elif IS_POSTGRESQL:
        # PostgreSQL configuration with proper pooling
        engine_kwargs.update({
            "poolclass": QueuePool,
            "pool_size": 5,
            "max_overflow": 10,
            "pool_recycle": 3600,  # Recycle connections every hour
            "pool_pre_ping": True,  # Test connections before using
            "connect_args": {
                "connect_timeout": 10,
            }
        })
    
    engine = create_engine(DATABASE_URL, **engine_kwargs)
    
    # Test connection immediately
    logger.info("Testing database connection...")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("[SUCCESS] Database connection successful!")
    
except Exception as e:
    logger.error(f"[ERROR] Failed to connect to database: {str(e)}")
    logger.error(f"Database URL type: {'PostgreSQL' if IS_POSTGRESQL else 'SQLite'}")
    
    # Create a fallback SQLite engine
    logger.warning("[WARNING] Creating fallback SQLite database...")
    DATABASE_URL = "sqlite:///./learning_platform.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
    )
    IS_POSTGRESQL = False

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()

def init_db():
    """Create all database tables (idempotent - safe to call multiple times)"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("[SUCCESS] Database tables initialized successfully")
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.close()
        logger.info("[SUCCESS] Database is ready for use")
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to initialize database: {str(e)}")
        raise
