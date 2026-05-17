import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime
from typing import Any
from app.core.config import settings
from app.models.registration import Registration


def _serialize_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sign_payload(payload: bytes) -> str:
    signature = hmac.new(settings.QR_SECRET_KEY.encode("utf-8"), payload, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")


def create_qr_token(registration: Registration) -> str:
    payload = {
        "registration_id": registration.id,
        "user_id": registration.user_id,
        "event_id": registration.event_id,
        "ticket_type_id": registration.ticket_type_id,
        "registration_code": registration.registration_code,
        "amount_paid": str(registration.amount_paid) if registration.amount_paid is not None else None,
        "currency": registration.currency,
        "payment_status": registration.payment_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "nonce": secrets.token_urlsafe(16),
    }
    signature = _sign_payload(_serialize_payload(payload))
    payload["signature"] = signature
    token = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    return token


def decode_qr_token(token: str) -> dict[str, Any]:
    try:
        decoded = base64.urlsafe_b64decode(token.encode("utf-8"))
        payload = json.loads(decoded.decode("utf-8"))
        signature = payload.pop("signature", None)
        if not signature:
            raise ValueError("Missing QR signature")
        expected = _sign_payload(_serialize_payload(payload))
        if not hmac.compare_digest(signature, expected):
            raise ValueError("Invalid QR signature")
        return payload
    except (ValueError, json.JSONDecodeError, base64.binascii.Error):
        raise ValueError("Invalid QR code payload")


def refresh_qr_code(registration: Registration) -> str:
    registration.qr_code = create_qr_token(registration)
    return registration.qr_code


def mark_as_checked_in(registration: Registration) -> None:
    registration.checked_in = True
    registration.checked_in_time = datetime.utcnow()
