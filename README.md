

# Medical NLP Intelligence System 

An AI-powered web application for analyzing clinical text using Natural Language Processing (NLP).  
The system extracts medical entities, applies safety guardrails to redact sensitive data, and generates both clinical and patient-friendly summaries.

---

## Features

- **Medical Entity Extraction**
  - Detects medical conditions and key clinical terms from text.

- **Safety Guardrails**
  - Automatically redacts sensitive information such as SSNs or personal identifiers.

- **Clinical Summary**
  - Generates concise summaries for healthcare professionals.

- **Patient-Friendly Explanation**
  - Provides simplified explanations of medical information.

- **Interactive Web Interface**
  - Built using Streamlit for easy interaction.

---

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **NLP Models:** HuggingFace Transformers (FLAN-T5)
- **Entity Extraction:** Custom Medical NER
- **OCR:** EasyOCR
- **Language:** Python

---

## Project Architecture
# Medical NLP Intelligence System 

An AI-powered web application for analyzing clinical text using Natural Language Processing (NLP).  
The system extracts medical entities, applies safety guardrails to redact sensitive data, and generates both clinical and patient-friendly summaries.

---

## Features

- **Medical Entity Extraction**
  - Detects medical conditions and key clinical terms from text.

- **Safety Guardrails**
  - Automatically redacts sensitive information such as SSNs or personal identifiers.

- **Clinical Summary**
  - Generates concise summaries for healthcare professionals.

- **Patient-Friendly Explanation**
  - Provides simplified explanations of medical information.

- **Interactive Web Interface**
  - Built using Streamlit for easy interaction.

---

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **NLP Models:** HuggingFace Transformers (FLAN-T5)
- **Entity Extraction:** Custom Medical NER
- **OCR:** EasyOCR
- **Language:** Python

---

## Project Architecture
User Input
│
▼
Streamlit Frontend
│
▼
FastAPI Backend
│
├── Text Cleaning
├── PII Safety Guardrails
├── Medical NER Entity Extraction
└── Transformer-based Summarization
│
▼
Clinical Summary + Patient Summary

