from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time, datetime
from decimal import Decimal

class EventBase(BaseModel):
    title: str
    short_description: Optional[str] = None
    description: Optional[str] = None
    start_date: date
    end_date: date
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    venue: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    max_attendees: Optional[int] = None
    is_featured: bool = False

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    slug: str
    current_attendees: int
    banner_image: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class EventDetailResponse(EventResponse):
    ticket_types: List["TicketTypeResponse"] = []
    schedule: List["ScheduleResponse"] = []
