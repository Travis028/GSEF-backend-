from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from app.models.base import BaseModel

class Newsletter(BaseModel):
    __tablename__ = "newsletter"
    
    email = Column(String(255), unique=True, nullable=False)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
