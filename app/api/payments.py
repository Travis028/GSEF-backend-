from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payment_service import init_mpesa_stk_push, create_stripe_payment_intent, verify_stripe_signature
from app.models.registration import Registration
from app.services.email_service import send_ticket_confirmation_email
from app.services.blockchain_service import record_ticket_audit
from app.models.user import User
from app.models.event import Event
from pydantic import BaseModel

router = APIRouter(prefix="/payments", tags=["Payments"])

class MPesaPaymentRequest(BaseModel):
    registration_id: int
    phone_number: str

class StripePaymentRequest(BaseModel):
    registration_id: int

@router.post("/mpesa/stk")
def mpesa_stk_push(request_data: MPesaPaymentRequest, db: Session = Depends(get_db)):
    registration = db.query(Registration).filter(Registration.id == request_data.registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    event = db.query(Event).filter(Event.id == registration.event_id).first()
    payment_data = init_mpesa_stk_push(
        phone_number=request_data.phone_number,
        amount=float(registration.amount_paid or 0),
        account_reference=registration.registration_code,
        transaction_desc=f"GSEF ticket purchase {event.title if event else registration.registration_code}"
    )
    return {"status": "initiated", "payment_data": payment_data}

@router.post("/stripe/create-intent")
def stripe_create_intent(request_data: StripePaymentRequest, db: Session = Depends(get_db)):
    registration = db.query(Registration).filter(Registration.id == request_data.registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    payment_intent = create_stripe_payment_intent(
        amount=float(registration.amount_paid or 0),
        currency=registration.currency,
        metadata={"registration_id": registration.id}
    )
    registration.payment_intent_id = payment_intent.get("id")
    db.commit()
    return {"status": "created", "payment_intent": payment_intent}

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    if not verify_stripe_signature(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    event = await request.json()
    if event.get("type") == "payment_intent.succeeded":
        payment_intent = event.get("data", {}).get("object", {})
        registration_id = int(payment_intent.get("metadata", {}).get("registration_id", 0))
        registration = db.query(Registration).filter(Registration.id == registration_id).first()
        if registration:
            registration.payment_status = "completed"
            db.commit()
            user = db.query(User).filter(User.id == registration.user_id).first()
            if user and user.email:
                send_ticket_confirmation_email(user.email, registration.registration_code, registration.qr_code, registration.event.title if registration.event else "GSEF event")
            record_ticket_audit(registration.id, "payment_completed", {"gateway": "stripe"})
    return {"status": "received"}

@router.post("/mpesa/callback")
async def mpesa_callback(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    callback_data = payload.get("Body", {}).get("stkCallback", {})
    merchant_request_id = callback_data.get("MerchantRequestID")
    result_code = callback_data.get("ResultCode")
    metadata = callback_data.get("CallbackMetadata", {}).get("Item", [])
    registration = db.query(Registration).filter(
        or_(
            Registration.registration_code == callback_data.get("CheckoutRequestID"),
            Registration.registration_code == merchant_request_id
        )
    ).first()
    if not registration:
        return {"status": "unknown registration", "payload": payload}
    if result_code == 0:
        registration.payment_status = "completed"
        db.commit()
        user = db.query(User).filter(User.id == registration.user_id).first()
        if user and user.email:
            send_ticket_confirmation_email(user.email, registration.registration_code, registration.qr_code, registration.event.title if registration.event else "GSEF event")
        record_ticket_audit(registration.id, "payment_completed", {"gateway": "mpesa"})
    else:
        registration.payment_status = "failed"
        db.commit()
    return {"status": "processed", "result_code": result_code}
