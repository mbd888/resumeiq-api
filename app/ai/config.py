"""Configuration for AI models"""

from typing import Dict, Any
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

# Model configurations
MODEL_CONFIGS = {
    "ner": {
        "model_name": "dbmdz/bert-large-cased-finetuned-conll03-english",
        "task": "ner",
        "aggregation_strategy": "simple",
        "device": -1  # CPU, use 0 for GPU
    },
    "skills": {
        "model_name": "jjzha/jobbert-base-cased",
        "task": "token-classification",
        "aggregation_strategy": "simple",
        "device": -1
    },
    "similarity": {
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "device": "cpu"
    },
    "zero_shot": {
        "model_name": "facebook/bart-large-mnli",
        "device": -1
    }
}

# Skills database (expand this with more skills)
TECHNICAL_SKILLS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby", "PHP",
    "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Shell", "Bash", "SQL", "HTML", "CSS",
    
    # Web Frameworks
    "React", "Angular", "Vue.js", "Next.js", "Django", "Flask", "FastAPI", "Express.js",
    "Spring Boot", "Ruby on Rails", "Laravel", "ASP.NET", "Node.js", "Svelte",
    
    # Databases
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra", "DynamoDB",
    "Oracle", "SQL Server", "SQLite", "Neo4j", "CouchDB", "MariaDB",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins", "GitLab CI",
    "GitHub Actions", "Terraform", "Ansible", "CloudFormation", "CircleCI", "Travis CI",
    
    # Data Science & ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn", "Keras",
    "Pandas", "NumPy", "Jupyter", "Data Analysis", "Statistics", "NLP", "Computer Vision",
    "Spark", "Hadoop", "Tableau", "Power BI", "Airflow",
    
    # Mobile
    "iOS", "Android", "React Native", "Flutter", "Xamarin", "SwiftUI",
    
    # Other Technical
    "Git", "Linux", "REST API", "GraphQL", "Microservices", "Agile", "Scrum", "CI/CD",
    "Unit Testing", "TDD", "System Design", "Architecture", "Blockchain", "IoT"
]

SOFT_SKILLS = [
    "Leadership", "Communication", "Teamwork", "Problem Solving", "Critical Thinking",
    "Time Management", "Adaptability", "Creativity", "Attention to Detail", "Organization",
    "Project Management", "Mentoring", "Collaboration", "Presentation", "Negotiation",
    "Strategic Planning", "Decision Making", "Conflict Resolution", "Customer Service",
    "Analytical Thinking", "Innovation", "Initiative", "Flexibility", "Reliability"
]

# Experience level keywords
EXPERIENCE_KEYWORDS = {
    "entry": ["intern", "internship", "graduate", "junior", "entry level", "0-2 years", "fresher"],
    "mid": ["mid level", "intermediate", "2-5 years", "3-5 years", "experienced"],
    "senior": ["senior", "lead", "principal", "5+ years", "7+ years", "expert", "advanced"],
    "executive": ["director", "vp", "vice president", "head of", "chief", "cto", "ceo", "partner"]
}
