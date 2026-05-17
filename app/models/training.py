from sqlalchemy import Column, String, Text, Integer, DECIMAL, Date, Boolean, ForeignKey
from app.models.base import BaseModel

class Training(BaseModel):
    __tablename__ = "trainings"

    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), default=0)
    currency = Column(String(3), default="KES")
    capacity = Column(Integer, default=0)
    location = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date)
    facilitator = Column(String(255))
    prerequisites = Column(Text)
    is_published = Column(Boolean, default=False)
    registration_url = Column(String(500))
