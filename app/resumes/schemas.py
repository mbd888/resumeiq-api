"""Pydantic schemas for resume endpoints"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class ResumeStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ResumeBase(BaseModel):
    """Base resume schema"""
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    position_applied: Optional[str] = None


class ResumeCreate(ResumeBase):
    """Schema for resume creation"""
    pass


class ResumeUpdate(ResumeBase):
    """Schema for resume update"""
    status: Optional[ResumeStatus] = None


class ResumeResponse(ResumeBase):
    """Schema for resume response"""
    id: UUID
    user_id: UUID
    filename: str
    file_size: int
    file_type: str
    status: ResumeStatus
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    raw_text: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ResumeListResponse(BaseModel):
    """Schema for resume list response"""
    resumes: List[ResumeResponse]
    total: int
    page: int
    per_page: int


class ResumeAnalysisResponse(BaseModel):
    """Schema for resume analysis response"""
    resume_id: UUID
    extracted_skills: List[str]
    experience_years: Optional[float]
    experience_level: Optional[str]
    ats_score: Optional[int]
    contact_info: Dict[str, Any]
    analyzed_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
