from sqlalchemy import Column, String, Text, JSON
from app.models.base import BaseModel

class Speaker(BaseModel):
    __tablename__ = "speakers"
    
    name = Column(String(200), nullable=False)
    title = Column(String(200))
    bio = Column(Text)
    image_url = Column(Text)
    company = Column(String(200))
    social_links = Column(JSON, default={})
