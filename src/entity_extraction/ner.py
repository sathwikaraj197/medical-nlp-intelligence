import spacy
from typing import List, Dict, Any

class MedicalNER:
    """
    Extracts medical entities from text using Spacy.
    """
    
    def __init__(self, model_name: str = "en_core_web_sm", glossary_terms: Dict[str, str] = None):
        try:
            self.nlp = spacy.load(model_name)
            
            # Add EntityRuler if glossary terms provided
            if glossary_terms:
                ruler = self.nlp.add_pipe("entity_ruler", before="ner")
                patterns = [
                    {"label": "MEDICAL_CONDITION", "pattern": term}
                    for term in glossary_terms.keys()
                ]
                ruler.add_patterns(patterns)
                
        except OSError:
            print(f"Warning: Model '{model_name}' not found. Please run 'python -m spacy download {model_name}'")
            # Fallback or re-raise depending on requirements. 
            # For now we'll let it fail if used, or user sees the warning.
            self.nlp = None

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extracts entities and returns them with a confidence score.
        """
        if not self.nlp:
             raise RuntimeError("Spacy model not loaded.")

        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            # Note: Standard spacy NER doesn't provide confidence scores per entity directly 
            # without additional component configuration like SpanCategorizer.
            # For this 'sm' model implementation, we will mock a high confidence 
            # or treat it as a binary extraction.
            # In a real medical model (like scispacy), we might get better specific labels.
            
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
                "confidence": 0.95 # Placeholder for model confidence
            })
            
        return entities
