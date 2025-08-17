"""Analysis models for resume analysis results and job matching"""

from sqlalchemy import Column, String, DateTime, Text, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Analysis(Base):
    """Stores the AI analysis results for a resume"""
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), unique=True, nullable=False)
    
    # Extracted information
    extracted_skills = Column(ARRAY(String), nullable=True)
    technical_skills = Column(ARRAY(String), nullable=True)
    soft_skills = Column(ARRAY(String), nullable=True)
    
    # Experience
    total_experience_years = Column(Float, nullable=True)
    experience_level = Column(String(50), nullable=True)  # Junior, Mid, Senior, Executive
    work_history = Column(JSONB, nullable=True)  # List of {company, position, duration, description}
    
    # Education
    education_level = Column(String(100), nullable=True)  # Bachelor's, Master's, PhD, etc.
    education_details = Column(JSONB, nullable=True)  # List of {degree, institution, year}
    
    # Contact information (extracted)
    contact_info = Column(JSONB, nullable=True)  # {email, phone, linkedin, github, etc.}
    
    # Scores
    ats_score = Column(Integer, nullable=True)  # 0-100
    completeness_score = Column(Integer, nullable=True)  # 0-100
    
    # Additional extracted data
    languages = Column(ARRAY(String), nullable=True)
    certifications = Column(JSONB, nullable=True)
    projects = Column(JSONB, nullable=True)
    achievements = Column(JSONB, nullable=True)
    
    # AI model outputs
    ner_entities = Column(JSONB, nullable=True)  # Raw NER output
    skills_confidence = Column(JSONB, nullable=True)  # Skill extraction confidence scores
    
    # Timestamps
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    resume = relationship("Resume", back_populates="analysis")


class JobMatch(Base):
    """Stores the matching results between a resume and job description"""
    __tablename__ = "job_matches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id"), nullable=False)
    
    # Match scores (0.0 to 1.0)
    overall_score = Column(Float, nullable=False)
    skills_match_score = Column(Float, nullable=True)
    experience_match_score = Column(Float, nullable=True)
    education_match_score = Column(Float, nullable=True)
    
    # Detailed matching
    matched_skills = Column(ARRAY(String), nullable=True)
    missing_skills = Column(ARRAY(String), nullable=True)
    matched_keywords = Column(ARRAY(String), nullable=True)
    
    # Match analysis
    strengths = Column(JSONB, nullable=True)  # List of strength points
    gaps = Column(JSONB, nullable=True)  # List of gap points
    recommendations = Column(Text, nullable=True)
    
    # Ranking
    rank = Column(Integer, nullable=True)  # Rank among all matches for this job
    
    # Timestamps
    matched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    resume = relationship("Resume", back_populates="job_matches")
    job_description = relationship("JobDescription", back_populates="job_matches")
