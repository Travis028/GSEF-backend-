from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.sponsor import Sponsor
from pydantic import BaseModel

router = APIRouter(prefix="/sponsors", tags=["Sponsors"])

class SponsorCreate(BaseModel):
    name: str
    logo_url: str = None
    website: str = None
    tier: str = None

class SponsorResponse(BaseModel):
    id: int
    name: str
    logo_url: str
    website: str
    tier: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[SponsorResponse])
def get_sponsors(tier: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Sponsor)
    if tier:
        query = query.filter(Sponsor.tier == tier)
    return query.offset(skip).limit(limit).all()

@router.get("/{sponsor_id}", response_model=SponsorResponse)
def get_sponsor(sponsor_id: int, db: Session = Depends(get_db)):
    sponsor = db.query(Sponsor).filter(Sponsor.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail="Sponsor not found")
    return sponsor

@router.post("/", response_model=SponsorResponse)
def create_sponsor(sponsor_data: SponsorCreate, db: Session = Depends(get_db)):
    db_sponsor = Sponsor(**sponsor_data.dict())
    db.add(db_sponsor)
    db.commit()
    db.refresh(db_sponsor)
    return db_sponsor
