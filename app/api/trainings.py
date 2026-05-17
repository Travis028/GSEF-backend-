from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from datetime import date
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.training import Training

router = APIRouter(prefix="/trainings", tags=["Trainings"])

class TrainingCreate(BaseModel):
    title: str
    description: str | None = None
    price: float = 0
    currency: str = "KES"
    capacity: int = 0
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    facilitator: str | None = None
    prerequisites: str | None = None
    is_published: bool = False
    registration_url: str | None = None

class TrainingResponse(TrainingCreate):
    id: int
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=list[TrainingResponse])
def list_trainings(published_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(Training)
    if published_only:
        query = query.filter(Training.is_published == True)
    return query.order_by(Training.start_date).all()

@router.post("/", response_model=TrainingResponse)
def create_training(training_data: TrainingCreate, current_user=Depends(get_current_admin_user), db: Session = Depends(get_db)):
    db_training = Training(**training_data.dict())
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

@router.patch("/{training_id}", response_model=TrainingResponse)
def update_training(training_id: int, training_data: TrainingCreate, current_user=Depends(get_current_admin_user), db: Session = Depends(get_db)):
    training = db.query(Training).filter(Training.id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    for key, value in training_data.dict().items():
        setattr(training, key, value)
    db.commit()
    db.refresh(training)
    return training
