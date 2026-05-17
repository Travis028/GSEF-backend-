from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(50))
    company = Column(String(200))
    position = Column(String(200))
    country = Column(String(100))
    profile_image = Column(String(500))
    role = Column(String(50), default="attendee")
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    registrations = relationship("Registration", back_populates="user", cascade="all, delete-orphan")
    events_created = relationship("Event", foreign_keys="Event.created_by")
