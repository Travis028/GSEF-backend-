from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_tables
from app.api import auth, events
import app.models.user
import app.models.event

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(events.router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "Welcome to GSEF API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
