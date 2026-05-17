from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from app.core.database import get_db
from app.core.dependencies import get_current_admin_user
from app.models.partner import Partner

router = APIRouter(prefix="/partners", tags=["Partners"])

class PartnerCreate(BaseModel):
    name: str
    website: HttpUrl | None = None
    logo_url: HttpUrl | None = None
    tier: str = "supporting"
    description: str | None = None
    partner_type: str = "sponsor"
    is_active: bool = True
    sort_order: int = 0

class PartnerResponse(PartnerCreate):
    id: int
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=list[PartnerResponse])
def list_partners(db: Session = Depends(get_db)):
    return db.query(Partner).filter(Partner.is_active == True).order_by(Partner.sort_order).all()

@router.post("/", response_model=PartnerResponse)
def create_partner(partner_data: PartnerCreate, current_user=Depends(get_current_admin_user), db: Session = Depends(get_db)):
    db_partner = Partner(**partner_data.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

@router.patch("/{partner_id}", response_model=PartnerResponse)
def update_partner(partner_id: int, partner_data: PartnerCreate, current_user=Depends(get_current_admin_user), db: Session = Depends(get_db)):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    for key, value in partner_data.dict().items():
        setattr(partner, key, value)
    db.commit()
    db.refresh(partner)
    return partner
