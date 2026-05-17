from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import authenticate_user, create_access_token, create_user, create_email_verification_token, verify_email_token
from app.services.email_service import send_email
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, user_data)
    verification_token = create_email_verification_token(user.id)
    verify_url = f"/api/auth/verify-email?token={verification_token}"
    send_email(
        user.email,
        "Verify your GSEF account",
        f"<p>Please verify your email by visiting <a href='{verify_url}'>this link</a>.</p>",
        f"Please verify your email by visiting {verify_url}"
    )
    return user

@router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user_id = verify_email_token(token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email_verified = True
    db.commit()
    return {"status": "verified", "email": user.email}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
