from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.founder import Founder

router = APIRouter(prefix="/founders", tags=["Founders"])

class FounderCreate(BaseModel):
    name: str
    title: str | None = None
    bio: str | None = None
    photo_url: HttpUrl | None = None
    expertise: str | None = None
    linkedin_url: HttpUrl | None = None
    twitter_url: HttpUrl | None = None
    company: str | None = None

class FounderResponse(FounderCreate):
    id: int
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=list[FounderResponse])
def list_founders(db: Session = Depends(get_db)):
    return db.query(Founder).order_by(Founder.created_at.desc()).all()

@router.post("/", response_model=FounderResponse)
def create_founder(founder_data: FounderCreate, current_user=Depends(get_current_admin_user), db: Session = Depends(get_db)):
    db_founder = Founder(**founder_data.dict())
    db.add(db_founder)
    db.commit()
    db.refresh(db_founder)
    return db_founder

@router.patch("/{founder_id}", response_model=FounderResponse)
def update_founder(founder_id: int, founder_data: FounderCreate, current_user=Depends(get_current_admin_user), db: Session = Depends(get_db)):
    founder = db.query(Founder).filter(Founder.id == founder_id).first()
    if not founder:
        raise HTTPException(status_code=404, detail="Founder not found")
    for key, value in founder_data.dict().items():
        setattr(founder, key, value)
    db.commit()
    db.refresh(founder)
    return founder
