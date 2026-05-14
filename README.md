# GSEF Backend

FastAPI backend for the Global Somali Entrepreneurship Forum platform.

## Tech Stack
- Python + FastAPI
- SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- JWT Authentication (python-jose + passlib)

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your values

# Run the server
uvicorn app.main:app --reload --port 8080
```

## API Docs
Once running, visit: http://localhost:8080/docs

## Project Structure
```
app/
├── api/          # Route handlers (auth, events)
├── core/         # Config and database setup
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
└── services/     # Business logic
```
