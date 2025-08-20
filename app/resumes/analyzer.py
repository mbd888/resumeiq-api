"""Main resume analyzer that orchestrates all AI models"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

from app.ai.ner_extractor import NERExtractor
from app.ai.skills_extractor import SkillsExtractor
from app.ai.similarity import SimilarityCalculator
from app.ai.experience_classifier import ExperienceClassifier

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """Orchestrate all AI models to analyze a resume"""
    
    def __init__(self):
        self.ner_extractor = NERExtractor()
        self.skills_extractor = SkillsExtractor()
        self.similarity_calculator = SimilarityCalculator()
        self.experience_classifier = ExperienceClassifier()
        
    async def analyze_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform complete analysis of a resume
        
        Args:
            resume_text: The text content of the resume
            job_description: Optional job description for matching
            
        Returns:
            Dictionary containing all analysis results
        """
        logger.info("Starting resume analysis")
        
        analysis_results = {}
        
        try:
            # 1. Extract named entities
            logger.info("Extracting entities...")
            ner_results = self.ner_extractor.extract_entities(resume_text)
            analysis_results.update({
                "candidate_name": ner_results.get("candidate_name"),
                "contact_info": ner_results.get("contact_info", {}),
                "work_history": ner_results.get("work_history", []),
                "entities": ner_results.get("entities", {})
            })
            
            # 2. Extract skills
            logger.info("Extracting skills...")
            skills_results = self.skills_extractor.extract_skills(resume_text)
            analysis_results.update({
                "technical_skills": skills_results.get("technical_skills", []),
                "soft_skills": skills_results.get("soft_skills", []),
                "all_skills": skills_results.get("all_skills", [])
            })
            
            # 3. Classify experience level
            logger.info("Classifying experience...")
            experience_results = self.experience_classifier.classify_experience(resume_text)
            analysis_results.update({
                "experience_years": experience_results.get("experience_years"),
                "experience_level": experience_results.get("experience_level"),
                "job_titles": experience_results.get("job_titles", [])
            })
            
            # 4. Calculate ATS score
            logger.info("Calculating ATS score...")
            ats_score = self._calculate_ats_score(analysis_results, resume_text)
            analysis_results["ats_score"] = ats_score
            
            # 5. If job description provided, calculate match
            if job_description:
                logger.info("Calculating job match...")
                match_results = await self.calculate_job_match(
                    resume_text, 
                    job_description,
                    analysis_results.get("all_skills", [])
                )
                analysis_results["job_match"] = match_results
            
            # 6. Generate recommendations
            recommendations = self._generate_recommendations(analysis_results)
            analysis_results["recommendations"] = recommendations
            
            # Add metadata
            analysis_results["analyzed_at"] = datetime.utcnow().isoformat()
            analysis_results["status"] = "completed"
            
        except Exception as e:
            logger.error(f"Error during resume analysis: {e}")
            analysis_results["status"] = "failed"
            analysis_results["error"] = str(e)
        
        return analysis_results
    
    async def calculate_job_match(self, resume_text: str, job_description: str, resume_skills: List[str]) -> Dict[str, Any]:
        """Calculate how well a resume matches a job description"""
        
        # Calculate overall similarity
        similarity_score = self.similarity_calculator.calculate_similarity(
            resume_text, 
            job_description
        )
        
        # Extract required skills from job description
        job_skills = self.skills_extractor.extract_skills(job_description)
        required_skills = job_skills.get("all_skills", [])
        
        # Calculate skill match
        skill_match = self.skills_extractor.calculate_skill_match(
            resume_skills,
            required_skills
        )
        
        # Calculate section-wise similarity
        section_scores = self.similarity_calculator.find_similar_sections(
            resume_text,
            job_description
        )
        
        # Overall match score (weighted average)
        overall_score = (
            similarity_score * 0.4 +
            skill_match.get("match_score", 0) * 0.4 +
            max(section_scores.values(), default=0) * 0.2
        )
        
        return {
            "overall_score": round(overall_score, 2),
            "similarity_score": round(similarity_score, 2),
            "skills_match": skill_match,
            "section_scores": section_scores,
            "matched_skills": skill_match.get("matched_skills", []),
            "missing_skills": skill_match.get("missing_skills", [])
        }
    
    def _calculate_ats_score(self, analysis_results: Dict, resume_text: str) -> int:
        """Calculate ATS (Applicant Tracking System) compatibility score"""
        score = 0
        max_score = 100
        
        # Check for contact information (20 points)
        contact_info = analysis_results.get("contact_info", {})
        if contact_info.get("email"):
            score += 10
        if contact_info.get("phone"):
            score += 10
        
        # Check for skills section (20 points)
        if analysis_results.get("technical_skills"):
            score += 20
        
        # Check for work history (20 points)
        if analysis_results.get("work_history"):
            score += 20
        
        # Check for experience years (10 points)
        if analysis_results.get("experience_years") is not None:
            score += 10
        
        # Check for proper formatting (15 points)
        if self._check_formatting(resume_text):
            score += 15
        
        # Check for keywords density (15 points)
        keyword_score = min(len(analysis_results.get("all_skills", [])) * 3, 15)
        score += keyword_score
        
        return min(score, max_score)
    
    def _check_formatting(self, text: str) -> bool:
        """Check if resume has good formatting for ATS"""
        # Simple checks for formatting
        has_sections = any(keyword in text.lower() for keyword in 
                          ["experience", "education", "skills", "summary"])
        has_bullets = "•" in text or "-" in text[:1000]
        reasonable_length = 500 < len(text) < 10000
        
        return has_sections and reasonable_length
    
    def _generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generate recommendations for resume improvement"""
        recommendations = []
        
        # ATS score recommendations
        ats_score = analysis_results.get("ats_score", 0)
        if ats_score < 70:
            recommendations.append("Consider improving ATS compatibility by adding more keywords")
        
        # Contact info recommendations
        contact_info = analysis_results.get("contact_info", {})
        if not contact_info.get("email"):
            recommendations.append("Add email address for contact information")
        if not contact_info.get("phone"):
            recommendations.append("Include phone number for easier contact")
        if not contact_info.get("linkedin"):
            recommendations.append("Add LinkedIn profile URL")
        
        # Skills recommendations
        if len(analysis_results.get("technical_skills", [])) < 5:
            recommendations.append("Include more technical skills relevant to your field")
        
        # Experience recommendations
        if not analysis_results.get("experience_years"):
            recommendations.append("Clearly mention total years of experience")
        
        # Work history recommendations
        if len(analysis_results.get("work_history", [])) < 2:
            recommendations.append("Provide more detailed work history with company names and dates")
        
        return recommendations
