from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.newsletter import Newsletter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/newsletter", tags=["Newsletter"])

class NewsletterSubscribe(BaseModel):
    email: EmailStr

class NewsletterResponse(BaseModel):
    id: int
    email: str
    subscribed_at: str
    is_active: bool
    
    class Config:
        from_attributes = True

@router.post("/subscribe", response_model=NewsletterResponse)
def subscribe_newsletter(sub_data: NewsletterSubscribe, db: Session = Depends(get_db)):
    # Check if already exists
    existing = db.query(Newsletter).filter(Newsletter.email == sub_data.email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.commit()
            db.refresh(existing)
        return existing
    
    db_newsletter = Newsletter(email=sub_data.email)
    db.add(db_newsletter)
    db.commit()
    db.refresh(db_newsletter)
    return db_newsletter

@router.post("/unsubscribe/{email}")
def unsubscribe_newsletter(email: str, db: Session = Depends(get_db)):
    newsletter = db.query(Newsletter).filter(Newsletter.email == email).first()
    if not newsletter:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    newsletter.is_active = False
    db.commit()
    return {"message": "Unsubscribed successfully"}

@router.get("/subscribers", response_model=List[NewsletterResponse])
def get_subscribers(db: Session = Depends(get_db)):
    return db.query(Newsletter).filter(Newsletter.is_active == True).all()
