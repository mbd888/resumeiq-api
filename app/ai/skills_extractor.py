"""Skills extraction from resume text"""

from typing import List, Dict, Set, Any
import re
import logging
from app.ai.base import BaseModel
from app.ai.config import TECHNICAL_SKILLS, SOFT_SKILLS

logger = logging.getLogger(__name__)

class SkillsExtractor(BaseModel):
    """Extract technical and soft skills from resume text"""
    
    def __init__(self):
        super().__init__("skills_extractor", "cpu")
        self.technical_skills = set(skill.lower() for skill in TECHNICAL_SKILLS)
        self.soft_skills = set(skill.lower() for skill in SOFT_SKILLS)
        
    def load_model(self):
        """No model to load for rule-based extraction"""
        # We're using rule-based extraction for skills
        # You can enhance this with a model like JobBERT later
        pass
        
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract technical and soft skills from text"""
        text_lower = text.lower()
        
        # Clean text for better matching
        text_cleaned = re.sub(r'[^\w\s\+\#]', ' ', text_lower)
        
        found_technical = []
        found_soft = []
        
        # Extract technical skills
        for skill in TECHNICAL_SKILLS:
            skill_lower = skill.lower()
            # Check for word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_cleaned):
                found_technical.append(skill)
        
        # Extract soft skills
        for skill in SOFT_SKILLS:
            skill_lower = skill.lower()
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_cleaned):
                found_soft.append(skill)
        
        # Look for additional technical skills patterns
        additional_technical = self._extract_additional_technical_skills(text)
        found_technical.extend(additional_technical)
        
        # Remove duplicates while preserving order
        found_technical = list(dict.fromkeys(found_technical))
        found_soft = list(dict.fromkeys(found_soft))
        
        return {
            "technical_skills": found_technical[:20],  # Top 20 technical skills
            "soft_skills": found_soft[:10],  # Top 10 soft skills
            "all_skills": found_technical + found_soft
        }
    
    def _extract_additional_technical_skills(self, text: str) -> List[str]:
        """Extract additional technical skills using patterns"""
        additional = []
        
        # Programming language patterns
        prog_pattern = r'\b(?:proficient|experienced|skilled|knowledge|familiar)\s+(?:in|with)\s+([A-Z][a-zA-Z\+\#]+)'
        prog_matches = re.findall(prog_pattern, text)
        additional.extend(prog_matches)
        
        # Technology stack pattern
        stack_pattern = r'(?:tech|technology)\s+stack[:\s]+([^\.]+)'
        stack_matches = re.findall(stack_pattern, text, re.IGNORECASE)
        for match in stack_matches:
            # Split by common delimiters
            techs = re.split(r'[,;]', match)
            additional.extend([t.strip() for t in techs])
        
        # Framework/library pattern
        framework_pattern = r'\b([A-Z][a-z]+(?:JS|\.js|DB|SQL|API|SDK|UI|ML|AI|NLP))\b'
        framework_matches = re.findall(framework_pattern, text)
        additional.extend(framework_matches)
        
        # Filter out non-technical terms
        non_technical = {"I", "A", "The", "In", "With", "For", "And", "Or", "But"}
        additional = [skill for skill in additional if skill not in non_technical]
        
        return additional
    
    def calculate_skill_match(self, resume_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """Calculate skill match between resume and job requirements"""
        resume_set = set(skill.lower() for skill in resume_skills)
        required_set = set(skill.lower() for skill in required_skills)
        
        matched = resume_set.intersection(required_set)
        missing = required_set - resume_set
        
        match_score = len(matched) / len(required_set) if required_set else 0
        
        return {
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "match_score": round(match_score, 2),
            "matched_count": len(matched),
            "required_count": len(required_set)
        }