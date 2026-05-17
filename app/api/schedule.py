from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.schedule import Schedule
from pydantic import BaseModel
from datetime import time

router = APIRouter(prefix="/schedule", tags=["Schedule"])

class ScheduleCreate(BaseModel):
    event_id: int
    speaker_id: int = None
    title: str
    session_type: str = None  # keynote, panel, workshop
    start_time: time = None
    end_time: time = None
    room: str = None

class ScheduleResponse(BaseModel):
    id: int
    event_id: int
    speaker_id: int
    title: str
    session_type: str
    start_time: time
    end_time: time
    room: str
    
    class Config:
        from_attributes = True

@router.get("/event/{event_id}", response_model=List[ScheduleResponse])
def get_event_schedule(event_id: int, db: Session = Depends(get_db)):
    return db.query(Schedule).filter(Schedule.event_id == event_id).all()

@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule_item(schedule_id: int, db: Session = Depends(get_db)):
    item = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return item

@router.post("/", response_model=ScheduleResponse)
def create_schedule(schedule_data: ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = Schedule(**schedule_data.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule
