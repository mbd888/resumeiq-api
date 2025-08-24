"""
Configuration management using Pydantic Settings.
Handles all environment variables and settings.
"""

from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import secrets
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    PROJECT_NAME: str = "ResumeIQ API"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: str = "resumeiq_user"
    POSTGRES_PASSWORD: str = "resumeiq_password"
    POSTGRES_DB: str = "resumeiq"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    
    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values) -> str:
        if isinstance(v, str):
            return v

        user = values.data.get("POSTGRES_USER")
        password = values.data.get("POSTGRES_PASSWORD")
        host = values.data.get("POSTGRES_HOST")
        port = values.data.get("POSTGRES_PORT")
        db = values.data.get("POSTGRES_DB")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    REDIS_URL: str = "redis://localhost:6379/0"
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".docx"]
    
    # Model Settings
    MODEL_CACHE_DIR: str = "models"
    MAX_MODEL_CACHE_SIZE: int = 5
    MODEL_INFERENCE_TIMEOUT: int = 30
    
    # Celery Settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_TASK_SOFT_TIME_LIMIT: int = 60
    CELERY_TASK_TIME_LIMIT: int = 120
    
    # Email Settings (notifications)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = "ResumeIQ"
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "resumeiq.log"
    
    # Features Flags
    ENABLE_BULK_PROCESSING: bool = True
    ENABLE_AI_ANALYSIS: bool = True
    ENABLE_JOB_MATCHING: bool = True
    ENABLE_ATS_SCORING: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        json_schema_extra = {
            "example": {
                "SECRET_KEY": "your-secret-key-here",
                "DATABASE_URL": "postgresql://user:password@localhost:5432/resumeiq",
                "REDIS_URL": "redis://localhost:6379/0",
                "BACKEND_CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8000"]'
            }
        }

settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODEL_CACHE_DIR, exist_ok=True)