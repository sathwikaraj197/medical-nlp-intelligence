import re
from typing import List, Dict, Any

class SafetyChecker:
    """
    Implements safety guardrails for medical text processing.
    """
    
    def __init__(self):
        # Basic patterns for PII
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b')
        self.ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
        # Matches partial dates like 12/12/2020, 2020-12-12, 12-12-2020
        self.date_pattern = re.compile(r'\b\d{1,4}[-/]\d{1,2}[-/]\d{2,4}\b')
        
        # Simple keyword list for unsafe content (placeholder for model-based approach)
        self.unsafe_keywords = [
            "ignore previous instructions",
            "system override",
            "drop table",
            "delete all"
        ]

    def audit_pii(self, text: str) -> str:
        """
        Redacts generic PII from text.
        """
        text = self.email_pattern.sub("[EMAIL REDACTED]", text)
        text = self.phone_pattern.sub("[PHONE REDACTED]", text)
        text = self.ssn_pattern.sub("[SSN REDACTED]", text)
        text = self.date_pattern.sub("[DATE REDACTED]", text)
        return text

    def check_content_safety(self, text: str) -> Dict[str, Any]:
        """
        Checks for potentially unsafe content.
        """
        text_lower = text.lower()
        triggered = []
        
        for keyword in self.unsafe_keywords:
            if keyword in text_lower:
                triggered.append(keyword)
                
        is_safe = len(triggered) == 0
        
        return {
            "is_safe": is_safe,
            "triggered_keywords": triggered,
            "message": "Content flagged as potentially unsafe." if not is_safe else "Content appears safe."
        }
