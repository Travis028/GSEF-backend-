from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.speaker import Speaker
from pydantic import BaseModel

router = APIRouter(prefix="/speakers", tags=["Speakers"])

class SpeakerCreate(BaseModel):
    name: str
    title: str = None
    bio: str = None
    image_url: str = None
    company: str = None
    social_links: dict = {}

class SpeakerResponse(BaseModel):
    id: int
    name: str
    title: str
    bio: str
    image_url: str
    company: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[SpeakerResponse])
def get_speakers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Speaker).offset(skip).limit(limit).all()

@router.get("/{speaker_id}", response_model=SpeakerResponse)
def get_speaker(speaker_id: int, db: Session = Depends(get_db)):
    speaker = db.query(Speaker).filter(Speaker.id == speaker_id).first()
    if not speaker:
        raise HTTPException(status_code=404, detail="Speaker not found")
    return speaker

@router.post("/", response_model=SpeakerResponse)
def create_speaker(speaker_data: SpeakerCreate, db: Session = Depends(get_db)):
    db_speaker = Speaker(**speaker_data.dict())
    db.add(db_speaker)
    db.commit()
    db.refresh(db_speaker)
    return db_speaker
