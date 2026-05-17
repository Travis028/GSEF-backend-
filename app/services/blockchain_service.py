import json
from app.core.config import settings
from app.models.blockchain_audit import BlockchainAudit
from app.core.database import SessionLocal


def log_audit_event(event_name: str, payload: dict, network: str = "local", tx_hash: str | None = None) -> BlockchainAudit:
    db = SessionLocal()
    try:
        audit = BlockchainAudit(
            event_name=event_name,
            payload=json.dumps(payload, default=str),
            network=network,
            blockchain_tx_hash=tx_hash,
            status="completed" if tx_hash else "pending"
        )
        db.add(audit)
        db.commit()
        db.refresh(audit)
        return audit
    finally:
        db.close()


def record_ticket_audit(registration_id: int, action: str, metadata: dict) -> BlockchainAudit:
    payload = {"registration_id": registration_id, "action": action, "metadata": metadata}
    return log_audit_event("ticket_verification", payload, network=settings.BLOCKCHAIN_NETWORK)
