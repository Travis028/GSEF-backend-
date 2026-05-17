from sqlalchemy import Column, String, Time, ForeignKey, Integer
from app.models.base import BaseModel

class Schedule(BaseModel):
    __tablename__ = "schedule"
    
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    speaker_id = Column(Integer, ForeignKey("speakers.id"))
    title = Column(String(300), nullable=False)
    session_type = Column(String(50))  # keynote, panel, workshop
    start_time = Column(Time)
    end_time = Column(Time)
    room = Column(String(100))
