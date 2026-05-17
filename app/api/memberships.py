from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.membership import Membership
from app.models.user import User
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter(prefix="/memberships", tags=["Memberships"])

class MembershipCreate(BaseModel):
    user_id: int
    tier: str = "free"  # free, professional, corporate

class MembershipResponse(BaseModel):
    id: int
    user_id: int
    tier: str
    start_date: str
    end_date: str
    is_active: bool
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[MembershipResponse])
def get_memberships(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Membership).offset(skip).limit(limit).all()

@router.get("/{membership_id}", response_model=MembershipResponse)
def get_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return membership

@router.post("/", response_model=MembershipResponse)
def create_membership(membership_data: MembershipCreate, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == membership_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Set end_date based on tier
    end_date = datetime.utcnow() + timedelta(days=365) if membership_data.tier != "free" else None
    
    db_membership = Membership(
        user_id=membership_data.user_id,
        tier=membership_data.tier,
        end_date=end_date
    )
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership

@router.patch("/{membership_id}")
def update_membership(membership_id: int, tier: str, db: Session = Depends(get_db)):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    
    membership.tier = tier
    if tier != "free":
        membership.end_date = datetime.utcnow() + timedelta(days=365)
    db.commit()
    db.refresh(membership)
    return membership
