from sqlalchemy import Column, String, Text, Date, ForeignKey, Integer
from app.models.base import BaseModel

class Gallery(BaseModel):
    __tablename__ = "gallery"
    
    event_id = Column(Integer, ForeignKey("events.id"))
    image_url = Column(Text, nullable=False)
    caption = Column(String(500))
    uploaded_at = Column(Date)
