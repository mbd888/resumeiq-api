"""Base class for AI models with caching and error handling"""

import logging
from typing import Any, Dict, Optional
from functools import lru_cache
import torch

logger = logging.getLogger(__name__)

class BaseModel:
    """Base class for AI models with common functionality"""
    
    def __init__(self, model_name: str, device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.tokenizer = None
        self._loaded = False
        
    def load_model(self):
        """Load model - to be implemented by subclasses"""
        raise NotImplementedError
        
    def ensure_loaded(self):
        """Ensure model is loaded before inference"""
        if not self._loaded:
            logger.info(f"Loading model: {self.model_name}")
            self.load_model()
            self._loaded = True
            
    def predict(self, text: str) -> Any:
        """Make prediction - to be implemented by subclasses"""
        raise NotImplementedError
        
    def unload_model(self):
        """Unload model to free memory"""
        if self._loaded:
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            self._loaded = False
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.info(f"Unloaded model: {self.model_name}")
