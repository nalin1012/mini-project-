from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from sqlalchemy.orm import Session
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from models import User, LoginHistory
from schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from firebase_config import verify_firebase_token, FIREBASE_AVAILABLE

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-use-env-var")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24  # 30 days

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

router = APIRouter(prefix="/api/auth", tags=["authentication"])

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    if request.headers.get("x-forwarded-for"):
        return request.headers.get("x-forwarded-for").split(",")[0].strip()
    return request.client.host if request.client else "unknown"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user - supports both JWT and Firebase tokens"""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # First try JWT verification (existing auth)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        pass  # Try Firebase auth next
    
    # Then try Firebase token verification (new auth)
    if FIREBASE_AVAILABLE:
        firebase_user = verify_firebase_token(token)
        if firebase_user:
            # Find or create user based on Firebase UID
            user = db.query(User).filter(User.firebase_uid == firebase_user.get("uid")).first()
            if not user:
                # Create new user from Firebase
                user = User(
                    email=firebase_user.get("email"),
                    name=firebase_user.get("name", firebase_user.get("email")),
                    hashed_password="firebase_auth",  # Firebase handles password
                    role="student",
                    firebase_uid=firebase_user.get("uid"),
                    is_active=True
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            return user
    
    # If both auth methods fail, raise exception
    raise credentials_exception

@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserRegister,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name,
        role="student",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Track login
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "unknown")
    login_record = LoginHistory(
        user_id=new_user.id,
        login_time=datetime.utcnow(),
        ip_address=client_ip,
        user_agent=user_agent,
        login_method="password"
    )
    new_user.last_login = datetime.utcnow()
    db.add(login_record)
    db.commit()
    
    # Create token
    access_token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(new_user)
    }

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Login user with email and password"""
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is deactivated")
    
    # Track login
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "unknown")
    login_record = LoginHistory(
        user_id=user.id,
        login_time=datetime.utcnow(),
        ip_address=client_ip,
        user_agent=user_agent,
        login_method="password"
    )
    user.last_login = datetime.utcnow()
    db.add(login_record)
    db.commit()
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.post("/firebase-login", response_model=TokenResponse)
async def firebase_login(
    firebase_token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Login with Firebase ID token"""
    if not FIREBASE_AVAILABLE:
        raise HTTPException(
            status_code=400,
            detail="Firebase authentication not configured"
        )
    
    # Verify Firebase token
    firebase_user = verify_firebase_token(firebase_token)
    if not firebase_user:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
    
    # Find or create user
    user = db.query(User).filter(User.firebase_uid == firebase_user.get("uid")).first()
    
    if not user:
        # Create new user from Firebase
        user = User(
            email=firebase_user.get("email"),
            name=firebase_user.get("name", firebase_user.get("email")),
            hashed_password="firebase_auth",
            role="student",
            firebase_uid=firebase_user.get("uid"),
            is_active=True
        )
        db.add(user)
    
    # Track login
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "unknown")
    login_record = LoginHistory(
        user_id=user.id if user.id else None,
        login_time=datetime.utcnow(),
        ip_address=client_ip,
        user_agent=user_agent,
        login_method="firebase"
    )
    user.last_login = datetime.utcnow()
    db.add(login_record)
    db.commit()
    db.refresh(user)
    
    # Create our JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse.from_orm(current_user)

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user (client should delete token)"""
    return {"message": "Logged out successfully"}

    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name,
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create token
    access_token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(new_user)
    }

@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse.from_orm(current_user)



