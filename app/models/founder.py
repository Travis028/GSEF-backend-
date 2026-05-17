from sqlalchemy import Column, String, Text
from app.models.base import BaseModel

class Founder(BaseModel):
    __tablename__ = "founders"

    name = Column(String(255), nullable=False)
    title = Column(String(255))
    bio = Column(Text)
    photo_url = Column(String(500))
    expertise = Column(String(500))
    linkedin_url = Column(String(500))
    twitter_url = Column(String(500))
    company = Column(String(255))
