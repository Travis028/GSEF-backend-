from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel

class Registration(BaseModel):
    __tablename__ = "registrations"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    ticket_type_id = Column(Integer, ForeignKey("ticket_types.id"), nullable=False)
    registration_code = Column(String(50), unique=True, nullable=False)
    qr_code = Column(Text)
    amount_paid = Column(DECIMAL(10, 2))
    currency = Column(String(3), default="KES")
    payment_status = Column(String(50), default="pending")
    payment_method = Column(String(50))
    payment_intent_id = Column(String(255))
    checked_in = Column(Boolean, default=False)
    checked_in_time = Column(DateTime)
    special_requirements = Column(Text)
    registered_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
    ticket_type = relationship("TicketType", back_populates="registrations")
