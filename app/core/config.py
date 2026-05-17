from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "GSEF API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./gsef.db"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    QR_SECRET_KEY: str = "your-qr-signing-secret-change-in-production"
    EMAIL_DEFAULT_FROM: str = "no-reply@gsef.co.ke"
    SENDGRID_API_KEY: Optional[str] = None
    STRIPE_API_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    MPESA_CONSUMER_KEY: Optional[str] = None
    MPESA_CONSUMER_SECRET: Optional[str] = None
    MPESA_SHORT_CODE: Optional[str] = None
    MPESA_PASSKEY: Optional[str] = None
    MPESA_CALLBACK_URL: str = "https://example.com/api/payments/mpesa/callback"
    BLOCKCHAIN_NETWORK: str = "local"
    
    class Config:
        env_file = ".env"

settings = Settings()
