import json
from urllib import request, parse
from app.core.config import settings


def send_email(to_email: str, subject: str, html_content: str, plain_text: str = None) -> dict:
    if not settings.SENDGRID_API_KEY:
        return {
            "status": "skipped",
            "message": "SendGrid API key not configured. Email was not sent.",
            "to": to_email,
        }
    payload = {
        "personalizations": [{
            "to": [{"email": to_email}],
            "subject": subject,
        }],
        "from": {"email": settings.EMAIL_DEFAULT_FROM},
        "content": [
            {"type": "text/plain", "value": plain_text or subject},
            {"type": "text/html", "value": html_content},
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        "https://api.sendgrid.com/v3/mail/send",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=30) as resp:
        return {"status": resp.status, "message": "Email request sent", "to": to_email}


def send_ticket_confirmation_email(email: str, registration_code: str, qr_code: str, event_title: str) -> dict:
    subject = f"Your GSEF ticket for {event_title}" 
    html_content = (
        f"<p>Thank you for registering for {event_title}.</p>"
        f"<p>Your registration code is <strong>{registration_code}</strong>.</p>"
        f"<p>Present the QR code below at arrival:</p>"
        f"<pre style='word-wrap: break-word; white-space: pre-wrap;'>{qr_code}</pre>"
    )
    plain_text = (
        f"Thank you for registering for {event_title}.\n"
        f"Registration code: {registration_code}\n"
        f"QR code payload: {qr_code}\n"
    )
    return send_email(email, subject, html_content, plain_text)
