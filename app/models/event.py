from sqlalchemy import Column, Integer, String, Text, Date, Time, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Event(BaseModel):
    __tablename__ = "events"
    
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    short_description = Column(String(500))
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    venue = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    max_attendees = Column(Integer)
    current_attendees = Column(Integer, default=0)
    banner_image = Column(Text)
    status = Column(String(50), default="upcoming")
    is_featured = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    ticket_types = relationship("TicketType", back_populates="event", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="event")
