from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.report import Report
from pydantic import BaseModel
from app.services.storage_service import save_upload_file

router = APIRouter(prefix="/reports", tags=["Reports"])

class ReportCreate(BaseModel):
    title: str
    description: str = None
    file_url: str = None

class ReportResponse(BaseModel):
    id: int
    title: str
    description: str
    file_url: str
    published_date: str
    download_count: int
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ReportResponse])
def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Report).offset(skip).limit(limit).all()

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/upload", response_model=ReportResponse)
def upload_report(
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_url = save_upload_file(file, subfolder="reports")
    db_report = Report(title=title, description=description, file_url=file_url)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.post("/", response_model=ReportResponse)
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    db_report = Report(**report_data.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/{report_id}/download")
def download_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.download_count += 1
    db.commit()
    return {"url": report.file_url, "downloads": report.download_count}
