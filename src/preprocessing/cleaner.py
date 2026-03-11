import re

def clean_text(text: str) -> str:
    """
    Cleans and normalizes input text for NLP processing.
    
    Args:
        text (str): Raw input text.
        
    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    
    # Normalize unicode characters can be added here if needed
    
    # Replace multiple spaces/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text
