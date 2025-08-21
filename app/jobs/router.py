"""API routes for job management"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.auth.dependencies import get_current_active_user, get_current_recruiter
from app.models.user import User
from app.jobs.service import JobService
from app.jobs import schemas

router = APIRouter()


@router.post("/", response_model=schemas.JobResponse)
async def create_job(
    job_data: schemas.JobCreate,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Create a new job posting (recruiters only)"""
    service = JobService(db)
    job = service.create_job(job_data.model_dump(), current_user)
    return job


@router.get("/{job_id}", response_model=schemas.JobResponse)
async def get_job(
    job_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific job posting"""
    service = JobService(db)
    return service.get_job(job_id)


@router.get("/", response_model=schemas.JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    active_only: bool = Query(True),
    my_jobs_only: bool = Query(False),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List job postings"""
    service = JobService(db)
    
    user_id = None
    if my_jobs_only and current_user:
        user_id = current_user.id
    
    return service.list_jobs(page, per_page, active_only, user_id)


@router.put("/{job_id}", response_model=schemas.JobResponse)
async def update_job(
    job_id: UUID,
    update_data: schemas.JobUpdate,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Update a job posting"""
    service = JobService(db)
    return service.update_job(
        job_id,
        current_user,
        update_data.model_dump(exclude_unset=True)
    )


@router.delete("/{job_id}")
async def delete_job(
    job_id: UUID,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """Delete a job posting"""
    service = JobService(db)
    service.delete_job(job_id, current_user)
    return {"message": "Job deleted successfully"}


@router.post("/{job_id}/match", response_model=schemas.JobMatchResponse)
async def match_resumes_to_job(
    job_id: UUID,
    match_request: schemas.JobMatchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Match resumes to a job posting"""
    service = JobService(db)
    result = await service.match_resumes_to_job(
        job_id,
        match_request.resume_ids,
        current_user
    )
    return result