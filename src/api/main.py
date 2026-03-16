from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from src.preprocessing.cleaner import clean_text
from src.safety.guardrails import SafetyChecker
from src.entity_extraction.ner import MedicalNER
from src.entity_extraction.glossary import MedicalGlossary

app = FastAPI(title="Medical NLP Intelligence API", version="0.1.0")

# Initialize components
safety_checker = SafetyChecker()
glossary = MedicalGlossary()

ner_engine = None

def load_ner():
    global ner_engine
    if ner_engine is None:
        try:
            ner_engine = MedicalNER(glossary_terms=glossary.get_terms())
        except Exception as e:
            print(f"Failed to initialize NER engine: {e}")
    # Initialize summarization model

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = None
summarizer_model = None

def load_summarizer():
    global tokenizer, summarizer_model
    if tokenizer is None or summarizer_model is None:
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        summarizer_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def summarize(prompt, max_length=120):
    load_summarizer()

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = summarizer_model.generate(**inputs, max_new_tokens=max_length)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

class AnalyzeRequest(BaseModel):
    text: str

class Entity(BaseModel):
    text: str
    label: str
    confidence: float
    standardized_term: Optional[str] = None
    start: int
    end: int

class AnalyzeResponse(BaseModel):
    original_text_length: int
    cleaned_text: str
    safety_audit: Dict[str, Any]
    entities: List[Entity]
    clinical_summary: Optional[str] = None
    patient_summary: Optional[str] = None

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):

    # 1. Safety Check
    safety_result = safety_checker.check_content_safety(request.text)
    redacted_text = safety_checker.audit_pii(request.text)

    # 2. Preprocessing
    cleaned = clean_text(redacted_text)

    # 3. Entity Extraction
   # 3. Entity Extraction
entities_out = []

load_ner()

if ner_engine and ner_engine.nlp:
    raw_entities = ner_engine.extract_entities(cleaned)
    for ent in raw_entities:
        std_term = glossary.normalize_term(ent["text"])
        entities_out.append(Entity(
            text=ent["text"],
            label=ent["label"],
            confidence=ent["confidence"],
            standardized_term=std_term if std_term != ent["text"].lower() else None,
            start=ent["start"],
            end=ent["end"]
        ))
    # ---------------- SUMMARIZATION ----------------

    clinical_summary = None
    patient_summary = None

    if summarizer_model:
        try:
            prompt = f"Summarize clinically: {redacted_text}"
            clinical_summary = summarize(prompt)

            patient_prompt = f"Explain simply for patient: {redacted_text}"
            patient_summary = summarize(patient_prompt)
        except Exception as e:
            print("Summary error:", e)

    # --------------- RETURN ----------------

    return AnalyzeResponse(
        original_text_length=len(request.text),
        cleaned_text=cleaned,
        safety_audit=safety_result,
        entities=entities_out,
        clinical_summary=clinical_summary,
        patient_summary=patient_summary
    )
    

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Medical NLP Intelligence System is running."}
