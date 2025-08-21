"""Pydantic schemas for job endpoints"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class JobBase(BaseModel):
    """Base job schema"""
    title: str = Field(..., min_length=1, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., min_length=10)
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: str = "USD"


class JobCreate(JobBase):
    """Schema for job creation"""
    pass


class JobUpdate(BaseModel):
    """Schema for job update"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary_currency: Optional[str] = None
    is_active: Optional[str] = None


class JobResponse(JobBase):
    """Schema for job response"""
    id: UUID
    user_id: UUID
    is_active: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class JobListResponse(BaseModel):
    """Schema for job list response"""
    jobs: List[JobResponse]
    total: int
    page: int
    per_page: int


class JobMatchRequest(BaseModel):
    """Schema for job matching request"""
    resume_ids: List[UUID]


class JobMatchResponse(BaseModel):
    """Schema for job match response"""
    job_id: UUID
    matches: List[Dict[str, Any]]
