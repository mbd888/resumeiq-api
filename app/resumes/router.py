"""API routes for resume management"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import os

from app.database import get_db
from app.auth.dependencies import get_current_active_user
from app.models.user import User
from app.resumes.service import ResumeService
from app.resumes import schemas
from app.config import settings

router = APIRouter()


@router.post("/upload", response_model=schemas.ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    position_applied: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a new resume"""
    service = ResumeService(db)
    resume = await service.create_resume(file, current_user, position_applied)
    return resume


@router.get("/{resume_id}", response_model=schemas.ResumeResponse)
async def get_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific resume"""
    service = ResumeService(db)
    return service.get_resume(resume_id, current_user)


@router.get("/", response_model=schemas.ResumeListResponse)
async def list_resumes(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    status: Optional[schemas.ResumeStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's resumes"""
    service = ResumeService(db)
    return service.list_resumes(current_user, page, per_page, status)


@router.put("/{resume_id}", response_model=schemas.ResumeResponse)
async def update_resume(
    resume_id: UUID,
    update_data: schemas.ResumeUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update resume metadata"""
    service = ResumeService(db)
    return service.update_resume(
        resume_id, 
        current_user, 
        update_data.model_dump(exclude_unset=True)
    )


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a resume"""
    service = ResumeService(db)
    service.delete_resume(resume_id, current_user)
    return {"message": "Resume deleted successfully"}


@router.get("/{resume_id}/download")
async def download_resume(
    resume_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download the original resume file"""
    service = ResumeService(db)
    resume = service.get_resume(resume_id, current_user)
    
    file_path = os.path.join(settings.UPLOAD_DIR, resume.file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=resume.filename,
        media_type='application/octet-stream'
    )
