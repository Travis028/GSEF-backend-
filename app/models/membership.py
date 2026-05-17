from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from datetime import datetime
from app.models.base import BaseModel

class Membership(BaseModel):
    __tablename__ = "memberships"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tier = Column(String(50), default="free")  # free, professional, corporate
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
