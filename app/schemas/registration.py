from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class RegistrationCreate(BaseModel):
    event_id: int
    ticket_type_id: int
    special_requirements: Optional[str] = None
    dietary_restrictions: Optional[str] = None

class RegistrationResponse(BaseModel):
    id: int
    registration_code: str
    qr_code: Optional[str] = None
    amount_paid: Decimal
    payment_status: str
    checked_in: bool
    registered_at: datetime
    event_id: int
    ticket_type_id: int

    class Config:
        from_attributes = True
