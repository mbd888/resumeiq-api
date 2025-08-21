"""Business logic for job operations"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.job import JobDescription
from app.models.user import User, UserType
from app.models.resume import Resume
from app.models.analysis import JobMatch
from app.ai.similarity import SimilarityCalculator
from app.ai.skills_extractor import SkillsExtractor


class JobService:
    """Service class for job operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.similarity_calculator = SimilarityCalculator()
        self.skills_extractor = SkillsExtractor()
    
    def create_job(self, job_data: dict, user: User) -> JobDescription:
        """Create a new job posting"""
        
        # Check if user is recruiter
        if user.user_type not in [UserType.RECRUITER, UserType.ADMIN]:
            raise HTTPException(
                status_code=403,
                detail="Only recruiters can create job postings"
            )
        
        # Set expiration date (30 days from now by default)
        if 'expires_at' not in job_data:
            job_data['expires_at'] = datetime.utcnow() + timedelta(days=30)
        
        job = JobDescription(
            user_id=user.id,
            **job_data
        )
        
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        return job
    
    def get_job(self, job_id: UUID) -> JobDescription:
        """Get a job by ID"""
        job = self.db.query(JobDescription).filter(
            JobDescription.id == job_id
        ).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job
    
    def list_jobs(
        self,
        page: int = 1,
        per_page: int = 10,
        active_only: bool = True,
        user_id: Optional[UUID] = None
    ) -> dict:
        """List jobs with pagination"""
        query = self.db.query(JobDescription)
        
        if active_only:
            query = query.filter(JobDescription.is_active == "active")
        
        if user_id:
            query = query.filter(JobDescription.user_id == user_id)
        
        total = query.count()
        jobs = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            "jobs": jobs,
            "total": total,
            "page": page,
            "per_page": per_page
        }
    
    def update_job(
        self,
        job_id: UUID,
        user: User,
        update_data: dict
    ) -> JobDescription:
        """Update a job posting"""
        job = self.get_job(job_id)
        
        # Check ownership
        if job.user_id != user.id and user.user_type != UserType.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own job postings"
            )
        
        for field, value in update_data.items():
            if hasattr(job, field) and value is not None:
                setattr(job, field, value)
        
        job.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(job)
        
        return job
    
    def delete_job(self, job_id: UUID, user: User) -> bool:
        """Delete a job posting"""
        job = self.get_job(job_id)
        
        # Check ownership
        if job.user_id != user.id and user.user_type != UserType.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="You can only delete your own job postings"
            )
        
        self.db.delete(job)
        self.db.commit()
        
        return True
    
    async def match_resumes_to_job(
        self,
        job_id: UUID,
        resume_ids: List[UUID],
        user: User
    ) -> Dict[str, Any]:
        """Match multiple resumes to a job"""
        
        # Get job
        job = self.get_job(job_id)
        
        # Get resumes
        resumes = self.db.query(Resume).filter(
            Resume.id.in_(resume_ids),
            Resume.user_id == user.id
        ).all()
        
        if not resumes:
            raise HTTPException(status_code=404, detail="No resumes found")
        
        matches = []
        
        for resume in resumes:
            if not resume.raw_text:
                continue
            
            # Calculate similarity
            similarity_score = self.similarity_calculator.calculate_similarity(
                resume.raw_text,
                job.description
            )
            
            # Extract and match skills
            resume_skills = self.skills_extractor.extract_skills(resume.raw_text)
            skill_match = self.skills_extractor.calculate_skill_match(
                resume_skills.get("all_skills", []),
                job.required_skills or []
            )
            
            # Create match record
            job_match = JobMatch(
                resume_id=resume.id,
                job_id=job.id,
                overall_score=similarity_score,
                skills_match_score=skill_match.get("match_score", 0),
                matched_skills=skill_match.get("matched_skills", []),
                missing_skills=skill_match.get("missing_skills", [])
            )
            
            self.db.add(job_match)
            
            matches.append({
                "resume_id": str(resume.id),
                "candidate_name": resume.candidate_name,
                "overall_score": round(similarity_score, 2),
                "skills_match_score": skill_match.get("match_score", 0),
                "matched_skills": skill_match.get("matched_skills", []),
                "missing_skills": skill_match.get("missing_skills", [])
            })
        
        self.db.commit()
        
        # Sort by overall score
        matches.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return {
            "job_id": str(job_id),
            "matches": matches
        }

