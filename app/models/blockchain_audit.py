from sqlalchemy import Column, String, Text, DateTime
from app.models.base import BaseModel

class BlockchainAudit(BaseModel):
    __tablename__ = "blockchain_audit"

    event_name = Column(String(100), nullable=False)
    payload = Column(Text, nullable=False)
    blockchain_tx_hash = Column(String(255), nullable=True)
    network = Column(String(100), default="local")
    status = Column(String(50), default="pending")
