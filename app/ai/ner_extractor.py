"""Named Entity Recognition for extracting names, companies, dates, etc."""

from typing import List, Dict, Any
from transformers import pipeline
import logging
import re
from datetime import datetime
from app.ai.base import BaseModel
from app.ai.config import MODEL_CONFIGS

logger = logging.getLogger(__name__)

class NERExtractor(BaseModel):
    """Extract named entities from resume text"""
    
    def __init__(self):
        config = MODEL_CONFIGS["ner"]
        super().__init__(config["model_name"], config.get("device", -1))
        self.pipeline = None
        
    def load_model(self):
        """Load NER model"""
        try:
            self.pipeline = pipeline(
                "ner",
                model=self.model_name,
                aggregation_strategy="simple",
                device=self.device
            )
            logger.info("NER model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading NER model: {e}")
            # Fallback to smaller model if large one fails
            self.pipeline = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple",
                device=self.device
            )
            
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract all entities from text"""
        self.ensure_loaded()
        
        try:
            # Get raw entities
            entities = self.pipeline(text)
            
            # Organize by type
            organized = {
                "persons": [],
                "organizations": [],
                "locations": [],
                "dates": [],
                "misc": []
            }
            
            for entity in entities:

                entity_type = entity['entity_group']
                entity_text = entity['word'].strip()

                # Skip BERT subword tokens
                if entity_text.startswith('##'):
                    continue
                
                if entity_type == "PER":
                    organized["persons"].append(entity_text)
                elif entity_type == "ORG":
                    organized["organizations"].append(entity_text)
                elif entity_type == "LOC":
                    organized["locations"].append(entity_text)
                elif entity_type == "DATE":
                    organized["dates"].append(entity_text)
                else:
                    organized["misc"].append(entity_text)
            
            # Deduplicate
            for key in organized:
                organized[key] = list(set(organized[key]))
            
            # Extract specific information
            contact_info = self._extract_contact_info(text)
            work_history = self._extract_work_history(text, organized)
            
            return {
                "entities": organized,
                "contact_info": contact_info,
                "work_history": work_history,
                "candidate_name": organized["persons"][0] if organized["persons"] else None
            }
            
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return self._fallback_extraction(text)
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information using regex"""
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact["email"] = emails[0]
        
        # Phone
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact["phone"] = phones[0]
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin:
            contact["linkedin"] = linkedin.group()
        
        # GitHub
        github_pattern = r'github\.com/[\w-]+'
        github = re.search(github_pattern, text, re.IGNORECASE)
        if github:
            contact["github"] = github.group()
            
        return contact
    
    def _extract_work_history(self, text: str, entities: Dict) -> List[Dict]:
        """Extract work history from text and entities"""
        work_history = []
        
        # Simple pattern matching for work experience
        # This is a simplified version - you can make it more sophisticated
        companies = entities.get("organizations", [])
        dates = entities.get("dates", [])
        
        # Look for job titles
        job_title_keywords = ["engineer", "developer", "manager", "analyst", "designer", 
                             "consultant", "specialist", "coordinator", "director", "lead"]
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if line contains job title keywords
            for keyword in job_title_keywords:
                if keyword in line_lower:
                    # Try to find associated company and date
                    position = {
                        "position": line.strip(),
                        "company": None,
                        "duration": None
                    }
                    
                    # Look for company in nearby lines
                    for company in companies:
                        if company.lower() in text[max(0, i-100):i+100].lower():
                            position["company"] = company
                            break
                    
                    # Look for dates in nearby lines
                    for date in dates:
                        if date in text[max(0, i-100):i+100]:
                            position["duration"] = date
                            break
                    
                    if position["company"] or position["duration"]:
                        work_history.append(position)
                    break
        
        return work_history[:5]  # Return top 5 work experiences
    
    def _fallback_extraction(self, text: str) -> Dict[str, Any]:
        """Fallback extraction using regex when model fails"""
        logger.info("Using fallback extraction method")
        
        contact_info = self._extract_contact_info(text)
        
        # Simple name extraction (first line often contains name)
        lines = text.strip().split('\n')
        candidate_name = lines[0] if lines else None
        
        return {
            "entities": {
                "persons": [candidate_name] if candidate_name else [],
                "organizations": [],
                "locations": [],
                "dates": [],
                "misc": []
            },
            "contact_info": contact_info,
            "work_history": [],
            "candidate_name": candidate_name
        }
