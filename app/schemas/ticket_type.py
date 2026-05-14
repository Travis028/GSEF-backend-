from pydantic import BaseModel
from typing import Optional, Dict
from decimal import Decimal

class TicketTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    benefits: Optional[Dict] = None
    quantity_available: Optional[int] = None
    early_bird_price: Optional[Decimal] = None

class TicketTypeCreate(TicketTypeBase):
    event_id: int

class TicketTypeResponse(TicketTypeBase):
    id: int
    event_id: int
    quantity_sold: int
    is_active: bool

    class Config:
        from_attributes = True
