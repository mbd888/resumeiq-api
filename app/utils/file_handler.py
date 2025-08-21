"""File handling utilities"""

import os
from typing import Optional
from fastapi import UploadFile
from app.config import settings


class FileHandler:
    """Handle file operations"""
    
    def validate_file(self, file: UploadFile) -> bool:
        """Validate file type and size"""
        
        # Check file size
        file.file.seek(0, 2)  # Move to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            return False
        
        # Check file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            return False
        
        return True
    
    def get_file_info(self, file: UploadFile) -> dict:
        """Get file information"""
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file_size,
            "extension": os.path.splitext(file.filename)[1]
        }
