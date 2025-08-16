"""
Main FastAPI application setup and configuration.
This is where everything comes together.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.database import engine, Base, get_db, init_db, check_database_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI app.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting ResumeIQ API...")
    
    # Create DB tables if they don't exist
    if not check_database_connection():
        raise RuntimeError("Database connection failed")
    init_db()

    logger.info("Database connected successfully")
    
    # Pre-load models here
    # logger.info("Loading AI models...")
    
    yield
    
    logger.info("Shutting down ResumeIQ API...")


# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered resume analysis and job matching API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Welcome to ResumeIQ API",
        "version": settings.VERSION,
        "status": "healthy",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint
    """
    return {
        "status": "healthy",
        "database": "connected",  # Add actual DB check in production
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


# API Info endpoint
@app.get("/api/v1/info", tags=["Info"])
async def api_info():
    """
    API information and capabilities
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "features": [
            "Resume parsing (PDF/TXT)",
            "Skills extraction",
            "Experience analysis",
            "Job matching",
            "ATS scoring",
            "Bulk processing"
        ],
        "models": {
            "ner": "dbmdz/bert-large-cased-finetuned-conll03-english",
            "skills": "jjzha/jobbert-base-cased",
            "similarity": "sentence-transformers/all-MiniLM-L6-v2",
            "classification": "microsoft/DialoGPT-medium"
        }
    }


# Global exception handler# COMMENT THESE LINES FOR NOW:
    # if not check_database_connection():
    #     raise RuntimeError("Database connection failed")
    # init_db()
    
    # ADD THIS INSTEAD:
    logger.warning("Database check skipped - running without DB for development")
    
    logger.info("Database connected successfully")
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error occurred",
            "type": "internal_error"
        }
    )


# Register routers (will be added in next few days)
# from app.auth.router import router as auth_router
# from app.resumes.router import router as resume_router
# from app.jobs.router import router as job_router

# app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(resume_router, prefix="/api/v1/resumes", tags=["Resumes"])
# app.include_router(job_router, prefix="/api/v1/jobs", tags=["Jobs"])