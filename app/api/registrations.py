from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
import secrets
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin_user
from app.models.registration import Registration
from app.models.ticket_type import TicketType
from app.models.event import Event
from app.services.ticket_service import create_qr_token, decode_qr_token, mark_as_checked_in
from app.services.payment_service import init_mpesa_stk_push, create_stripe_payment_intent
from app.services.email_service import send_ticket_confirmation_email
from app.services.blockchain_service import record_ticket_audit
from app.models.user import User
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/registrations", tags=["Registrations"])

class RegistrationPurchaseRequest(BaseModel):
    event_id: int
    ticket_type_id: int
    payment_method: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    special_requirements: Optional[str] = None

class RegistrationPurchaseResponse(BaseModel):
    registration_id: int
    payment_status: str
    payment_method: str
    qr_code: str
    payment_data: dict | None = None

class QRVerifyRequest(BaseModel):
    qr_code: str

class QRVerifyResponse(BaseModel):
    registration_id: int
    event_id: int
    ticket_type_id: int
    payment_status: str
    checked_in: bool
    valid: bool
    message: str

class CheckInRequest(BaseModel):
    qr_code: Optional[str] = None
    registration_id: Optional[int] = None

class CheckInResponse(BaseModel):
    registration_id: int
    checked_in: bool
    message: str

@router.post("/purchase", response_model=RegistrationPurchaseResponse)
def purchase_registration(
    purchase: RegistrationPurchaseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ticket_type = db.query(TicketType).filter(TicketType.id == purchase.ticket_type_id).first()
    event = db.query(Event).filter(Event.id == purchase.event_id).first()
    if not event or not ticket_type or ticket_type.event_id != event.id:
        raise HTTPException(status_code=404, detail="Event or ticket type not found")
    if not ticket_type.is_active:
        raise HTTPException(status_code=400, detail="Ticket type is not active")

    amount = float(ticket_type.price)
    registration = Registration(
        user_id=current_user.id,
        event_id=event.id,
        ticket_type_id=ticket_type.id,
        registration_code=f"GSEF-{secrets.token_hex(4).upper()}",
        amount_paid=Decimal(amount),
        currency=ticket_type.currency,
        payment_status="pending",
        payment_method=purchase.payment_method,
        special_requirements=purchase.special_requirements,
    )
    registration.qr_code = ""
    db.add(registration)
    db.commit()
    db.refresh(registration)

    registration.qr_code = create_qr_token(registration)
    db.commit()
    db.refresh(registration)

    payment_data = None
    try:
        if purchase.payment_method.lower() == "mpesa":
            phone_number = purchase.phone or current_user.phone
            if not phone_number:
                raise HTTPException(status_code=400, detail="Phone number is required for M-Pesa checkout")
            payment_data = init_mpesa_stk_push(
                phone_number=phone_number,
                amount=amount,
                account_reference=registration.registration_code,
                transaction_desc=f"GSEF ticket purchase {event.title}"
            )
        elif purchase.payment_method.lower() == "stripe":
            payment_data = create_stripe_payment_intent(
                amount=amount,
                currency=ticket_type.currency,
                metadata={
                    "registration_id": registration.id,
                    "user_id": current_user.id,
                    "event_id": event.id,
                }
            )
            registration.payment_intent_id = payment_data.get("id")
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Unsupported payment method")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return RegistrationPurchaseResponse(
        registration_id=registration.id,
        payment_status=registration.payment_status,
        payment_method=registration.payment_method,
        qr_code=registration.qr_code,
        payment_data=payment_data,
    )

@router.post("/verify", response_model=QRVerifyResponse)
def verify_registration(payload: QRVerifyRequest, db: Session = Depends(get_db)):
    try:
        decoded = decode_qr_token(payload.qr_code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    registration = db.query(Registration).filter(Registration.id == decoded.get("registration_id")).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    if registration.qr_code != payload.qr_code:
        raise HTTPException(status_code=400, detail="QR code mismatch")
    valid = registration.payment_status == "completed"
    message = "Valid ticket" if valid else "Payment not completed"
    return QRVerifyResponse(
        registration_id=registration.id,
        event_id=registration.event_id,
        ticket_type_id=registration.ticket_type_id,
        payment_status=registration.payment_status,
        checked_in=registration.checked_in,
        valid=valid,
        message=message,
    )

@router.patch("/{registration_id}/check-in", response_model=CheckInResponse)
def check_in_registration(
    registration_id: int,
    request_data: CheckInRequest,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    if registration.checked_in:
        raise HTTPException(status_code=400, detail="Ticket already checked in")
    mark_as_checked_in(registration)
    registration.payment_status = "completed"
    db.commit()
    record_ticket_audit(registration.id, "check_in", {"user": current_user.id})
    return CheckInResponse(registration_id=registration.id, checked_in=registration.checked_in, message="Ticket checked in successfully")

@router.post("/{registration_id}/resend-email")
def resend_ticket_email(registration_id: int, db: Session = Depends(get_db)):
    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    user = db.query(User).filter(User.id == registration.user_id).first()
    if not user or not user.email:
        raise HTTPException(status_code=404, detail="User email not found")

    send_ticket_confirmation_email(user.email, registration.registration_code, registration.qr_code, registration.event.title if registration.event else "GSEF event")
    return {"status": "sent", "email": user.email}
