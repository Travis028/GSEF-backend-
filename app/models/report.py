from sqlalchemy import Column, String, Text, Date, Integer
from app.models.base import BaseModel

class Report(BaseModel):
    __tablename__ = "reports"
    
    title = Column(String(300), nullable=False)
    description = Column(Text)
    file_url = Column(Text)
    published_date = Column(Date)
    download_count = Column(Integer, default=0)
