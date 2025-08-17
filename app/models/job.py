"""Job description model for job postings and requirements"""

from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Job details
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    
    # Requirements
    required_skills = Column(ARRAY(String), nullable=True)
    preferred_skills = Column(ARRAY(String), nullable=True)
    experience_required = Column(String(50), nullable=True)  # "Entry", "Mid", "Senior", "Executive"
    education_required = Column(String(100), nullable=True)
    
    # Compensation
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(3), default="USD", nullable=True)
    
    # Additional data
    benefits = Column(JSONB, nullable=True)
    job_metadata = Column(JSONB, nullable=True)  # Any additional structured data
    
    # Status
    is_active = Column(String(20), default="active", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    job_matches = relationship("JobMatch", back_populates="job_description", cascade="all, delete-orphan")
