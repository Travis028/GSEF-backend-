from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.feedback import Feedback

router = APIRouter(prefix="/feedback", tags=["Feedback"])

class FeedbackCreate(BaseModel):
    feedback_type: str
    message: str
    name: str | None = None
    email: EmailStr | None = None
    category: str | None = None

class FeedbackResponse(BaseModel):
    id: int
    feedback_type: str
    category: str | None
    message: str
    name: str | None
    email: str | None
    status: str
    is_public: bool
    created_at: str

    class Config:
        from_attributes = True

@router.post("/", response_model=FeedbackResponse)
def submit_feedback(feedback_data: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = Feedback(**feedback_data.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/", response_model=list[FeedbackResponse])
def list_feedback(status: str | None = None, public_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Feedback)
    if status:
        query = query.filter(Feedback.status == status)
    if public_only:
        query = query.filter(Feedback.is_public == True)
    return query.order_by(Feedback.created_at.desc()).all()

@router.patch("/{feedback_id}/publish")
def publish_feedback(feedback_id: int, current_user=Depends(get_current_admin_user), db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    feedback.is_public = True
    feedback.status = "published"
    db.commit()
    return {"status": "published", "feedback_id": feedback.id}
