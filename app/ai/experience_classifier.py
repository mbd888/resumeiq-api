"""Classify experience level from resume text"""

import re
from typing import Dict, Optional, List
from datetime import datetime
import logging
from app.ai.base import BaseModel
from app.ai.config import EXPERIENCE_KEYWORDS

logger = logging.getLogger(__name__)

class ExperienceClassifier(BaseModel):
    """Classify candidate experience level"""
    
    def __init__(self):
        super().__init__("experience_classifier", "cpu")
        self.experience_keywords = EXPERIENCE_KEYWORDS
        
    def load_model(self):
        """No model needed for rule-based classification"""
        pass
    
    def classify_experience(self, text: str) -> Dict[str, any]:
        """Classify experience level from resume text"""
        text_lower = text.lower()
        
        # Extract years of experience
        years = self._extract_years_of_experience(text)
        
        # Check for experience level keywords
        level = self._classify_by_keywords(text_lower)
        
        # If no keyword match, classify by years
        if not level and years is not None:
            level = self._classify_by_years(years)
        
        # Extract job titles for additional context
        job_titles = self._extract_job_titles(text)
        
        return {
            "experience_years": years,
            "experience_level": level or "Not Specified",
            "job_titles": job_titles,
            "confidence": self._calculate_confidence(level, years, job_titles)
        }
    
    def _extract_years_of_experience(self, text: str) -> Optional[float]:
        """Extract total years of experience from text"""
        
        # Pattern 1: "X years of experience"
        pattern1 = r'(\d+)\+?\s*years?\s*(?:of\s*)?experience'
        match1 = re.search(pattern1, text, re.IGNORECASE)
        if match1:
            return float(match1.group(1))
        
        # Pattern 2: Date ranges (e.g., "2018 - 2023")
        date_pattern = r'(\d{4})\s*[-–]\s*(\d{4}|present|current)'
        date_matches = re.findall(date_pattern, text, re.IGNORECASE)
        
        if date_matches:
            total_years = 0
            current_year = datetime.now().year
            
            for start, end in date_matches:
                start_year = int(start)
                if end.lower() in ['present', 'current']:
                    end_year = current_year
                else:
                    end_year = int(end)
                
                years_diff = end_year - start_year
                if 0 <= years_diff <= 50:  # Sanity check
                    total_years += years_diff
            
            if total_years > 0:
                return float(total_years)
        
        # Pattern 3: "Since YYYY"
        since_pattern = r'since\s*(\d{4})'
        since_match = re.search(since_pattern, text, re.IGNORECASE)
        if since_match:
            start_year = int(since_match.group(1))
            return float(datetime.now().year - start_year)
        
        return None
    
    def _classify_by_keywords(self, text_lower: str) -> Optional[str]:
        """Classify based on keyword matching"""
        
        # Check each experience level
        for level, keywords in self.experience_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if level == "entry":
                        return "Entry Level"
                    elif level == "mid":
                        return "Mid-Level"
                    elif level == "senior":
                        return "Senior"
                    elif level == "executive":
                        return "Executive"
        
        return None
    
    def _classify_by_years(self, years: float) -> str:
        """Classify based on years of experience"""
        if years < 2:
            return "Entry Level"
        elif years < 5:
            return "Mid-Level"
        elif years < 10:
            return "Senior"
        else:
            return "Executive"
    
    def _extract_job_titles(self, text: str) -> List[str]:
        """Extract likely job titles from text"""
        job_titles = []
        
        # Common job title patterns
        title_keywords = [
            "engineer", "developer", "manager", "analyst", "designer",
            "architect", "consultant", "specialist", "coordinator",
            "director", "lead", "senior", "junior", "principal",
            "head of", "vp", "vice president", "chief", "intern"
        ]
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line contains job title keywords
            for keyword in title_keywords:
                if keyword in line_lower and len(line) < 100:  # Likely a title, not a paragraph
                    job_titles.append(line.strip())
                    break
        
        return job_titles[:5]  # Return top 5 job titles
    
    def _calculate_confidence(self, level: str, years: Optional[float], job_titles: List[str]) -> float:
        """Calculate confidence score for the classification"""
        confidence = 0.5  # Base confidence
        
        if level and level != "Not Specified":
            confidence += 0.2
        
        if years is not None:
            confidence += 0.2
        
        if job_titles:
            confidence += 0.1 * min(len(job_titles), 3)
        
        return min(confidence, 1.0)