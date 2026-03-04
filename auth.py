from fastapi import Depends, HTTPException, APIRouter
from ..auth import create_access_token,verify_password,get_password_hash

router = APIRouter(prefix="/api/auth", tags=["auth"])
@router.post("/register")
async def register(email: str, password: str, name: str, db=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed= get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, name=name)
    db.add(user)
    db.commit()
    token=create_access_token({"sub": str(user.id)})
    db.refresh(user)
    return { "access_token": token,"token_type": "bearer" }


@router.post("/login")
async def login(email: str, password: str, db=Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token=create_access_token({"sub": str(user.id)})
    return { "access_token": token,"token_type": "bearer" }


