"""PDF parsing utilities"""

import PyPDF2
import pdfplumber
from typing import Optional


class PDFParser:
    """Parse PDF files to extract text"""
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """Extract text from PDF file"""
        text = ""
        
        try:
            # Try with pdfplumber first (better for tables)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                return text
            
            # Fallback to PyPDF2
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            return text.strip() if text.strip() else None
            
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None
    
    def extract_metadata(self, file_path: str) -> dict:
        """Extract PDF metadata"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                return {
                    "author": metadata.get('/Author', ''),
                    "title": metadata.get('/Title', ''),
                    "subject": metadata.get('/Subject', ''),
                    "creator": metadata.get('/Creator', ''),
                    "pages": len(pdf_reader.pages)
                } if metadata else {}
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}