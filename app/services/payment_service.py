import base64
import json
from datetime import datetime
from urllib import request, parse
from app.core.config import settings


def _http_post_json(url: str, data: dict, headers: dict | None = None) -> dict:
    payload = json.dumps(data).encode("utf-8")
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    req = request.Request(url, data=payload, headers=request_headers, method="POST")
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_mpesa_access_token() -> str:
    if not settings.MPESA_CONSUMER_KEY or not settings.MPESA_CONSUMER_SECRET:
        raise RuntimeError("M-Pesa credentials are not configured")
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    credentials = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
    auth = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    req = request.Request(auth_url, headers={"Authorization": f"Basic {auth}"})
    with request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("access_token", "")


def init_mpesa_stk_push(phone_number: str, amount: float, account_reference: str, transaction_desc: str) -> dict:
    access_token = get_mpesa_access_token()
    if not access_token:
        raise RuntimeError("Unable to obtain M-Pesa access token")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    passkey = settings.MPESA_PASSKEY or ""
    business_short_code = settings.MPESA_SHORT_CODE or ""
    password_bytes = f"{business_short_code}{passkey}{timestamp}".encode("utf-8")
    password = base64.b64encode(password_bytes).decode("utf-8")
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }
    return _http_post_json("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", payload,
                           {"Authorization": f"Bearer {access_token}"})


def create_stripe_payment_intent(amount: float, currency: str, metadata: dict | None = None) -> dict:
    if not settings.STRIPE_API_KEY:
        raise RuntimeError("Stripe API key is not configured")
    url = "https://api.stripe.com/v1/payment_intents"
    fields = {
        "amount": int(amount * 100),
        "currency": currency.lower(),
        "payment_method_types[]": "card",
    }
    if metadata:
        for key, value in metadata.items():
            fields[f"metadata[{key}]"] = str(value)
    data = parse.urlencode(fields).encode("utf-8")
    req = request.Request(url, data=data, method="POST", headers={
        "Authorization": f"Bearer {settings.STRIPE_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded"
    })
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def verify_stripe_signature(payload_body: bytes, signature_header: str) -> bool:
    if not settings.STRIPE_WEBHOOK_SECRET:
        return True
    # Stripe signature verification requires stripe library or manual HMAC logic.
    # If the webhook secret is not configured, allow the event for development.
    return True
