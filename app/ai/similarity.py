"""Text similarity for matching resumes to job descriptions"""

from typing import List, Tuple, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
import logging
import re
from app.ai.base import BaseModel
from app.ai.config import MODEL_CONFIGS

logger = logging.getLogger(__name__)

class SimilarityCalculator(BaseModel):
    """Calculate semantic similarity between texts"""
    
    def __init__(self):
        config = MODEL_CONFIGS["similarity"]
        super().__init__(config["model_name"], config.get("device", "cpu"))
        
    def load_model(self):
        """Load sentence transformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info("Similarity model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading similarity model: {e}")
            # Fallback to smaller model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        self.ensure_loaded()
        
        try:
            # Encode texts to embeddings
            embeddings = self.model.encode([text1, text2])
            
            # Calculate cosine similarity
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def rank_candidates(self, job_description: str, resumes: List[Dict]) -> List[Dict]:
        """Rank resumes by similarity to job description"""
        self.ensure_loaded()
        
        try:
            # Encode job description
            job_embedding = self.model.encode(job_description)
            
            # Calculate similarities
            results = []
            for resume in resumes:
                resume_text = resume.get("text", "")
                resume_embedding = self.model.encode(resume_text)
                
                similarity = np.dot(job_embedding, resume_embedding) / (
                    np.linalg.norm(job_embedding) * np.linalg.norm(resume_embedding)
                )
                
                results.append({
                    "resume_id": resume.get("id"),
                    "similarity_score": float(similarity),
                    "candidate_name": resume.get("candidate_name")
                })
            
            # Sort by similarity score
            results.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return results
            
        except Exception as e:
            logger.error(f"Error ranking candidates: {e}")
            return []
    
    def find_similar_sections(self, resume_text: str, job_text: str) -> Dict[str, float]:
        """Find which sections of resume match job description best"""
        self.ensure_loaded()
        
        # Split resume into sections
        sections = self._split_into_sections(resume_text)
        
        # Calculate similarity for each section
        section_scores = {}
        job_embedding = self.model.encode(job_text)
        
        for section_name, section_text in sections.items():
            if section_text:
                section_embedding = self.model.encode(section_text)
                similarity = np.dot(job_embedding, section_embedding) / (
                    np.linalg.norm(job_embedding) * np.linalg.norm(section_embedding)
                )
                section_scores[section_name] = float(similarity)
        
        return section_scores
    
    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split resume text into common sections"""
        sections = {
            "experience": "",
            "education": "",
            "skills": "",
            "summary": "",
            "projects": ""
        }
        
        # Common section headers
        section_patterns = {
            "experience": r"(?:work\s+)?experience|employment|career|professional\s+background",
            "education": r"education|academic|qualification|degree",
            "skills": r"skills|technical\s+skills|competencies|technologies",
            "summary": r"summary|objective|profile|about",
            "projects": r"projects|portfolio|accomplishments"
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            for section, pattern in section_patterns.items():
                if re.search(pattern, line_lower):
                    current_section = section
                    break
            
            # Add line to current section
            if current_section:
                sections[current_section] += line + "\n"
        
        return sections
