from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse, EventDetailResponse

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", response_model=List[EventResponse])
def get_events(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, regex="^(upcoming|ongoing|completed)$"),
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    if status:
        query = query.filter(Event.status == status)
    if featured:
        query = query.filter(Event.is_featured == True)
    return query.offset(skip).limit(limit).all()

@router.get("/upcoming", response_model=List[EventResponse])
def get_upcoming_events(db: Session = Depends(get_db)):
    from datetime import date
    return db.query(Event).filter(Event.start_date >= date.today()).order_by(Event.start_date).limit(6).all()

@router.get("/featured", response_model=List[EventResponse])
def get_featured_events(db: Session = Depends(get_db)):
    return db.query(Event).filter(Event.is_featured == True).limit(3).all()

@router.get("/{event_id}", response_model=EventDetailResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/", response_model=EventResponse)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', event_data.title.lower()).strip('-')
    db_event = Event(slug=slug, **event_data.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
