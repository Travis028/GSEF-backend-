from sqlalchemy import Column, String, Text, Boolean, Integer
from app.models.base import BaseModel

class Partner(BaseModel):
    __tablename__ = "partners"

    name = Column(String(255), nullable=False)
    website = Column(String(500))
    logo_url = Column(String(500))
    tier = Column(String(50), default="supporting")
    description = Column(Text)
    partner_type = Column(String(50), default="sponsor")
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
