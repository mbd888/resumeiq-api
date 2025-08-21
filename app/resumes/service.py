"""Business logic for resume operations"""

import os
import shutil
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import aiofiles

from app.models.resume import Resume, ResumeStatus
from app.models.user import User
from app.config import settings
from app.utils.file_handler import FileHandler
from app.utils.pdf_parser import PDFParser


class ResumeService:
    """Service class for resume operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.file_handler = FileHandler()
        self.pdf_parser = PDFParser()
    
    async def create_resume(
        self,
        file: UploadFile,
        user: User,
        position_applied: Optional[str] = None
    ) -> Resume:
        """Create a new resume record and save file"""
        
        # Validate file
        if not self.file_handler.validate_file(file):
            raise HTTPException(status_code=400, detail="Invalid file type or size")
        
        # Generate unique filename
        file_id = uuid4()
        file_extension = os.path.splitext(file.filename)[1]
        stored_filename = f"{user.id}/{file_id}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, stored_filename)
        
        # Create user directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save file
        try:
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Extract text from file
        raw_text = None
        try:
            if file_extension.lower() == '.pdf':
                raw_text = self.pdf_parser.extract_text(file_path)
            elif file_extension.lower() in ['.txt', '.text']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_text = f.read()
        except Exception as e:
            print(f"Failed to extract text: {e}")
        
        # Create database record
        resume = Resume(
            id=file_id,
            user_id=user.id,
            filename=file.filename,
            file_path=stored_filename,
            file_size=len(content),
            file_type=file_extension[1:] if file_extension else 'unknown',
            raw_text=raw_text,
            position_applied=position_applied,
            status=ResumeStatus.PENDING
        )
        
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        
        return resume
    
    def get_resume(self, resume_id: UUID, user: User) -> Resume:
        """Get a resume by ID"""
        resume = self.db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == user.id
        ).first()
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return resume
    
    def list_resumes(
        self,
        user: User,
        page: int = 1,
        per_page: int = 10,
        status: Optional[ResumeStatus] = None
    ) -> dict:
        """List user's resumes with pagination"""
        query = self.db.query(Resume).filter(Resume.user_id == user.id)
        
        if status:
            query = query.filter(Resume.status == status)
        
        total = query.count()
        resumes = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            "resumes": resumes,
            "total": total,
            "page": page,
            "per_page": per_page
        }
    
    def update_resume(
        self,
        resume_id: UUID,
        user: User,
        update_data: dict
    ) -> Resume:
        """Update a resume"""
        resume = self.get_resume(resume_id, user)
        
        for field, value in update_data.items():
            if hasattr(resume, field) and value is not None:
                setattr(resume, field, value)
        
        self.db.commit()
        self.db.refresh(resume)
        
        return resume
    
    def delete_resume(self, resume_id: UUID, user: User) -> bool:
        """Delete a resume and its file"""
        resume = self.get_resume(resume_id, user)
        
        # Delete file
        file_path = os.path.join(settings.UPLOAD_DIR, resume.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete database record
        self.db.delete(resume)
        self.db.commit()
        
        return True
