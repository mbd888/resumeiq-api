"""API endpoints for AI-powered resume analysis"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.database import get_db
from app.models.resume import Resume
from app.models.analysis import Analysis
from app.auth.dependencies import get_current_active_user
from app.models.user import User
from app.resumes.analyzer import ResumeAnalyzer

router = APIRouter()
analyzer = ResumeAnalyzer()

@router.post("/analyze/{resume_id}")
async def analyze_resume(
    resume_id: str,
    job_description: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Analyze a resume using AI models
    """
    # Get resume from database
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if not resume.raw_text:
        raise HTTPException(status_code=400, detail="Resume text not available")
    
    # Perform analysis
    analysis_results = await analyzer.analyze_resume(
        resume.raw_text,
        job_description
    )
    
    # Save analysis to database
    analysis = Analysis(
        resume_id=resume.id,
        extracted_skills=analysis_results.get("all_skills", []),
        technical_skills=analysis_results.get("technical_skills", []),
        soft_skills=analysis_results.get("soft_skills", []),
        total_experience_years=analysis_results.get("experience_years"),
        experience_level=analysis_results.get("experience_level"),
        work_history=analysis_results.get("work_history", []),
        contact_info=analysis_results.get("contact_info", {}),
        ats_score=analysis_results.get("ats_score"),
        ner_entities=analysis_results.get("entities", {})
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return {
        "message": "Analysis completed successfully",
        "analysis": analysis_results
    }

@router.post("/analyze-text")
async def analyze_text(
    text: str = Form(...),
    job_description: Optional[str] = Form(None),
    #current_user: User = Depends(get_current_active_user)
):
    """
    Analyze resume text directly without saving
    """
    # Perform analysis
    analysis_results = await analyzer.analyze_resume(text, job_description)
    
    return {
        "message": "Analysis completed successfully",
        "analysis": analysis_results
    }

@router.get("/skills/extract")
async def extract_skills_from_text(
    text: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Extract skills from any text
    """
    skills_extractor = analyzer.skills_extractor
    skills = skills_extractor.extract_skills(text)
    
    return skills

@router.post("/match-score")
async def calculate_match_score(
    resume_text: str = Form(...),
    job_description: str = Form(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Calculate match score between resume and job description
    """
    # Extract skills from both
    resume_skills = analyzer.skills_extractor.extract_skills(resume_text)
    
    # Calculate match
    match_results = await analyzer.calculate_job_match(
        resume_text,
        job_description,
        resume_skills.get("all_skills", [])
    )
    
    return match_results