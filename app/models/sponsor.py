from sqlalchemy import Column, String, Text
from app.models.base import BaseModel

class Sponsor(BaseModel):
    __tablename__ = "sponsors"
    
    name = Column(String(200), nullable=False)
    logo_url = Column(Text)
    website = Column(String(300))
    tier = Column(String(50))  # platinum, gold, silver
