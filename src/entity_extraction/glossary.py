from typing import Dict, Optional

class MedicalGlossary:
    """
    Standardizes medical terms to a common lexicon.
    """
    
    def __init__(self, data_path: str = "data/medical_glossary.json"):
        import json
        import os
        
        self.term_mapping = {}
        try:
            if os.path.exists(data_path):
                with open(data_path, 'r') as f:
                    self.term_mapping = json.load(f)
            else:
                print(f"Warning: Glossary file not found at {data_path}")
        except Exception as e:
            print(f"Error loading glossary: {e}")

    def get_terms(self) -> Dict[str, str]:
        """Returns the full dictionary of terms."""
        return self.term_mapping

    def normalize_term(self, term: str) -> str:
        """
        Returns the standardized medical term if found, else returns the original term.
        """
        key = term.lower()
        return self.term_mapping.get(key, term)

    def explain_term(self, term: str) -> Optional[str]:
        """
        Could provide definitions in the future.
        """
        # Placeholder for definitions
        return None
