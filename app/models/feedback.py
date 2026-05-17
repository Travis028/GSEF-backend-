from sqlalchemy import Column, String, Text, Boolean, DateTime
from app.models.base import BaseModel

class Feedback(BaseModel):
    __tablename__ = "feedback"

    feedback_type = Column(String(50), nullable=False)
    category = Column(String(100), nullable=True)
    message = Column(Text, nullable=False)
    name = Column(String(150), nullable=True)
    email = Column(String(255), nullable=True)
    status = Column(String(50), default="pending")
    is_public = Column(Boolean, default=False)
    responded_at = Column(DateTime)
