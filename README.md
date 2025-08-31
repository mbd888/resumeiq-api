# ResumeIQ - AI-Powered Resume Analysis Platform

An intelligent resume analysis and job matching system that leverages cutting-edge NLP models to extract skills, analyze experience, and match candidates to job opportunities.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)

## Features

### Core Functionality
- **AI-Powered Resume Analysis**: Automatically extract skills, experience, and contact information using BERT NER and custom NLP pipelines
- **Smart Job Matching**: Match resumes to job descriptions using sentence transformers and cosine similarity scoring
- **ATS Compatibility Scoring**: Evaluate resumes for Applicant Tracking System compatibility (0-100 score)
- **Skill Gap Analysis**: Identify missing skills between candidate profiles and job requirements
- **Role-Based Access Control**: Separate interfaces for job seekers and recruiters with JWT authentication

### Technical Highlights
- **Multiple AI Models**: Integrates 4 different HuggingFace transformer models for comprehensive analysis
- **Real-time Processing**: Analyze resumes and get results in seconds
- **File Support**: Handle PDF, TXT, and DOCX formats with automatic text extraction
- **RESTful API**: Full CRUD operations for resumes, jobs, and user management
- **Modern Frontend**: Responsive Next.js interface with TypeScript and Tailwind CSS

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                    │
│                   - TypeScript                          │
│                   - Tailwind CSS                        │
│                   - React Hook Form                     │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────▼───────────────────────────────┐
│                   Backend (FastAPI)                     │
│                   - JWT Authentication                  │
│                   - Role-based Access                   │
│                   - File Upload Handling                │
└────--──┬──────────────────┬──────────────────┬─────-────┘
         │                  │                  │
  ┌──────▼──────┐   ┌───────▼──────┐  ┌────────▼────────┐
  │ PostgreSQL  │   │ HuggingFace  │  │  File Storage   │
  │  Database   │   │   Models     │  │   (uploads/)    │
  └─────────────┘   └──────────────┘  └─────────────────┘
```

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **AI/ML**: HuggingFace Transformers, Sentence-Transformers
- **File Processing**: PyPDF2, pdfplumber, python-docx
- **Migrations**: Alembic

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form
- **HTTP Client**: Axios
- **Icons**: Lucide React

### AI Models
- **BERT NER**: `dbmdz/bert-large-cased-finetuned-conll03-english` for entity extraction
- **Sentence-BERT**: `sentence-transformers/all-MiniLM-L6-v2` for semantic similarity
- **Custom Models**: Skills extraction and experience classification

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15
- 2GB+ free space for AI models

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/mbd888/resumeiq-api.git
cd resumeiq-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL**
```bash
# Create database and user
psql postgres
CREATE USER resumeiq_user WITH PASSWORD 'resumeiq_password';
CREATE DATABASE resumeiq OWNER resumeiq_user;
\q
```

5. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

6. **Run migrations**
```bash
alembic upgrade head
```

7. **Create uploads directory**
```bash
mkdir uploads
```

8. **Start the backend**
```bash
uvicorn app.main:app --reload
```

Backend API will be available at http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd resumeiq-frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and receive JWT token
- `GET /api/v1/auth/me` - Get current user profile

#### Resumes
- `POST /api/v1/resumes/upload` - Upload resume file
- `GET /api/v1/resumes/{id}` - Get specific resume
- `GET /api/v1/resumes/` - List user's resumes
- `DELETE /api/v1/resumes/{id}` - Delete resume

#### Jobs
- `POST /api/v1/jobs/` - Create job posting (recruiters only)
- `GET /api/v1/jobs/{id}` - Get job details
- `POST /api/v1/jobs/{id}/match` - Match resumes to job

#### AI Analysis
- `POST /api/v1/ai/analyze/{resume_id}` - Analyze uploaded resume
- `POST /api/v1/ai/analyze-text` - Analyze text directly
- `GET /api/v1/ai/skills/extract` - Extract skills from text

## Usage Guide

### For Job Seekers
1. Register an account as "job_seeker"
2. Upload your resume (PDF or TXT)
3. View AI-extracted skills and ATS score
4. Browse job opportunities
5. See match scores for available positions

### For Recruiters
1. Register an account as "recruiter"
2. Create job postings with required skills
3. Upload candidate resumes
4. Use AI matching to find best candidates
5. View skill gap analysis for each match

## Testing

### Quick Test Flow
1. Register a job seeker account
2. Upload a sample resume
3. View the analysis results
4. Register a recruiter account
5. Create a job posting
6. Match resumes to the job

### Sample Test Data
Create a file `test_resume.txt`:
```
John Doe
john.doe@email.com | (555) 123-4567

Senior Software Engineer at Google (2020-2023)
- Developed microservices using Python, FastAPI, Docker
- Led team of 5 engineers on cloud migration

Skills: Python, JavaScript, React, PostgreSQL, AWS, Docker
Education: BS Computer Science - Stanford University
```

## Project Structure

```
resumeiq-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings management
│   ├── database.py          # Database configuration
│   ├── models/              # SQLAlchemy models
│   ├── auth/                # Authentication module
│   ├── resumes/             # Resume management
│   ├── jobs/                # Job management
│   ├── ai/                  # AI model integrations
│   └── utils/               # Utility functions
├── alembic/                 # Database migrations
├── uploads/                 # File storage
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables

resumeiq-frontend/
├── app/                     # Next.js app router
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── login/              # Login page
│   ├── register/           # Registration page
│   └── dashboard/          # Dashboard pages
├── lib/                     # Utility functions
│   ├── api.ts              # API client
│   └── auth.ts             # Auth utilities
└── package.json            # Node dependencies
```

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://resumeiq_user:resumeiq_password@localhost:5432/resumeiq
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
MOCK_MODE=false  # Set to true to use mock AI models
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Deployment

### Using Docker (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Deployment
1. Set up PostgreSQL database
2. Configure environment variables for production
3. Run migrations
4. Start backend with Gunicorn/Uvicorn
5. Build and deploy frontend with Vercel/Netlify

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- HuggingFace for transformer models
- FastAPI for the excellent web framework
- Next.js team for the React framework
- All open-source contributors

**Note**: First-time model downloads may take 5-10 minutes (~1.5GB). Models are cached locally in `~/.cache/huggingface/`
