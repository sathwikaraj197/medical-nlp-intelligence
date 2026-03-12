import streamlit as st
import requests
import json
import easyocr
import numpy as np
from PIL import Image

# Configuration
API_URL = "https://medical-nlp-api-ej42.onrender.com/analyze"

st.set_page_config(
    page_title="Medical NLP Intelligence",
    page_icon="🏥",
    layout="wide"
)

# Initialize Session State for Text
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = "Patient reports severe headache and potential heart attack. SSN: 123-45-6789."

@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

def extract_text_from_image(image_file):
    reader = load_reader()
    image = Image.open(image_file)
    image_np = np.array(image)
    result = reader.readtext(image_np, detail=0)
    return " ".join(result)

def analyze_text(text):
    try:
        response = requests.post(API_URL, json={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None

def main():
    st.title("🏥 Medical NLP Intelligence System")
    st.markdown("""
    This system analyzes medical text to extract entities, standardize terms, and ensure safety.
    """)

    role = st.radio(
    "Select User Type",
    ["Healthcare Professional", "Patient"]
)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Input")
        
        # Image Upload
        uploaded_file = st.file_uploader("Upload Prescription/Note (Image)", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
             with st.spinner("Extracting text from image..."):
                 try:
                     extracted = extract_text_from_image(uploaded_file)
                     if extracted != st.session_state.ocr_text:
                         st.session_state.ocr_text = extracted
                         st.success("Text extracted successfully!")
                 except Exception as e:
                     st.error(f"OCR Error: {e}")

        text_input = st.text_area(
            "Enter Medical Notes", 
            height=300, 
            value=st.session_state.ocr_text
        )
        # Update session state if user types manually
        if text_input != st.session_state.ocr_text:
            st.session_state.ocr_text = text_input
        
        analyze_btn = st.button("Analyze Text", type="primary")

    with col2:
        st.subheader("Analysis Results")
        
        if analyze_btn:
            if not text_input.strip():
                st.warning("Please enter some text to analyze.")
            else:
                with st.spinner("Analyzing..."):
                    result = analyze_text(text_input)
                
                if result:
                    safety = result.get("safety_audit", {})

                    if safety.get("is_safe"):
                        st.success("✅ Content Safety Check Passed")
                    else:
                        st.error("❌ Content Flagged as Unsafe")
                        st.write(safety.get("message"))

                    st.markdown("### Processed Text (Redacted)")
                    st.info(result.get("cleaned_text"))

                    # ---------- DOCTOR MODE ----------
                    if role == "Healthcare Professional":
                        st.markdown("### Clinical Entities")
                        entities = result.get("entities", [])

                        if entities:
                            for ent in entities:
                                with st.expander(f"{ent['text']} ({ent['label']})"):
                                    st.write(f"Standard Term: {ent.get('standardized_term','N/A')}")
                                    st.write(f"Confidence: {ent.get('confidence','N/A')}")
                        else:
                            st.write("No entities detected.")

                        st.markdown("### Clinical Summary")
                        st.success(result.get("clinical_summary"))

                    # ---------- PATIENT MODE ----------
                    else:
                        st.markdown("### Patient-Friendly Summary")
                        patient_summary = result.get("patient_summary")

                        if patient_summary:
                            st.success(patient_summary)
                        else:
                            st.info("Patient explanation not available yet.")

                    st.markdown("---")

                    with st.expander("View Raw JSON"):
                        st.json(result)
                                    

if __name__ == "__main__":
    main()
