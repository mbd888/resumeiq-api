"""Resume model for storing uploaded resumes and their metadata"""

from sqlalchemy import Column, String, DateTime, Text, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class ResumeStatus(str, enum.Enum):
    """Resume processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # File information
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    file_type = Column(String(50), nullable=False)  # pdf, docx, txt
    
    # Content
    raw_text = Column(Text, nullable=True)
    parsed_data = Column(JSONB, nullable=True)  # Structured extracted data
    
    # Metadata
    candidate_name = Column(String(255), nullable=True)
    candidate_email = Column(String(255), nullable=True)
    candidate_phone = Column(String(50), nullable=True)
    position_applied = Column(String(255), nullable=True)
    
    # Status tracking
    status = Column(Enum(ResumeStatus), default=ResumeStatus.PENDING, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    analysis = relationship("Analysis", back_populates="resume", uselist=False, cascade="all, delete-orphan")
    job_matches = relationship("JobMatch", back_populates="resume", cascade="all, delete-orphan")