from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, events, admin, users, speakers, gallery, reports, memberships, newsletter, schedule, sponsors, registrations, payments, feedback, partners, trainings, founders
from app.core.database import create_tables
from app.core.middleware import SimpleRateLimitMiddleware

app = FastAPI(title="GSEF API", version="1.0.0")

# Create database tables on startup
create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

app.include_router(auth.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(speakers.router, prefix="/api")
app.include_router(gallery.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(memberships.router, prefix="/api")
app.include_router(newsletter.router, prefix="/api")
app.include_router(schedule.router, prefix="/api")
app.include_router(sponsors.router, prefix="/api")
app.include_router(registrations.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(partners.router, prefix="/api")
app.include_router(trainings.router, prefix="/api")
app.include_router(founders.router, prefix="/api")

app.add_middleware(SimpleRateLimitMiddleware, max_requests=120, window_seconds=60)

@app.get("/")
def root():
    return {"message": "Welcome to GSEF API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
