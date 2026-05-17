from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey, JSON, Date, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class TicketType(BaseModel):
    __tablename__ = "ticket_types"
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default="KES")
    benefits = Column(JSON)
    quantity_available = Column(Integer)
    quantity_sold = Column(Integer, default=0)
    early_bird_price = Column(DECIMAL(10, 2))
    early_bird_deadline = Column(Date)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    
    # Relationships
    event = relationship("Event", back_populates="ticket_types")
    registrations = relationship("Registration", back_populates="ticket_type")
