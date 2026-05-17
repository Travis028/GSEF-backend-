from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.gallery import Gallery
from pydantic import BaseModel
from app.services.storage_service import save_upload_file

router = APIRouter(prefix="/gallery", tags=["Gallery"])

class GalleryCreate(BaseModel):
    event_id: int
    image_url: str
    caption: str = None

class GalleryResponse(BaseModel):
    id: int
    event_id: int
    image_url: str
    caption: str
    uploaded_at: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[GalleryResponse])
def get_gallery(event_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(Gallery)
    if event_id:
        query = query.filter(Gallery.event_id == event_id)
    return query.offset(skip).limit(limit).all()

@router.get("/{gallery_id}", response_model=GalleryResponse)
def get_gallery_item(gallery_id: int, db: Session = Depends(get_db)):
    item = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    return item

@router.post("/upload", response_model=GalleryResponse)
def upload_gallery_item(
    event_id: int = Form(...),
    caption: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_url = save_upload_file(file, subfolder="gallery")
    db_gallery = Gallery(event_id=event_id, image_url=image_url, caption=caption)
    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)
    return db_gallery

@router.post("/", response_model=GalleryResponse)
def create_gallery_item(gallery_data: GalleryCreate, db: Session = Depends(get_db)):
    db_gallery = Gallery(**gallery_data.dict())
    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)
    return db_gallery
