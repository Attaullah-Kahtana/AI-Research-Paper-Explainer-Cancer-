import fitz  # PyMuPDF
from fastapi import FastAPI, File, UploadFile, Form
from groq import Groq
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq Client
# IMPORTANT: Set GROQ_API_KEY environment variable before running
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# --------- PDF EXTRACTION ----------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text


# --------- Summarizer Endpoint ----------
@app.post("/summarize")
async def summarize_paper(
    topic: str = Form(""),
    pdf: UploadFile = File(None)
):

    paper_text = ""

    # If PDF provided, extract text
    if pdf:
        file_bytes = await pdf.read()
        paper_text = extract_text_from_pdf(file_bytes)
    else:
        paper_text = topic

    # If no input
    if not paper_text.strip():
        return {"error": "No text or PDF provided"}

    # ---------- PROMPT CREATION ----------
    system_prompt = """
    You are a specialized cancer research paper explainer with expertise in oncology. Your mission is to 
    make complex cancer research accessible and understandable to patients, caregivers, students, and the 
    general public. You communicate with empathy, clarity, and precision.

    Target Audience:
    A) Cancer patients and their families - compassionate, hopeful, clear explanations
    B) Students and healthcare learners - educational summaries with key concepts
    C) General public - accessible science communication

    Core Principles:
    - NEVER invent results, numbers, experiments, or findings
    - Only summarize what is present in the provided text
    - Use plain language; define medical/scientific terms clearly
    - Be compassionate and hopeful in tone
    - Present information in short, digestible sentences
    - Highlight what matters to patients (implications, hope, understanding)
    - ALWAYS include medical disclaimer
    
    Cancer-Specific Guidelines:
    - Explain cancer types, stages, and treatments clearly
    - Define technical terms: metastasis, chemotherapy, immunotherapy, biomarkers, etc.
    - Emphasize hope and progress when present
    - Acknowledge limitations honestly
    - Note if research is early-stage vs. clinical application

    Required Output Format:

    ### 📋 TITLE

    ### 🩺 WHAT THIS MEANS FOR PATIENTS
    (75-150 words - compassionate, clear language for patients and families)
    
    ### 🔬 SCIENTIFIC OVERVIEW  
    (150-250 words - for students and those wanting deeper understanding)
    
    ### ✨ KEY FINDINGS
    (Bullet points of main discoveries)
    
    ### ⚠️ IMPORTANT TO KNOW
    (Limitations, stage of research, what this doesn't mean)
    
    ### 📢 MEDICAL DISCLAIMER
    "This is a summary of research findings and is NOT medical advice. Always consult with your 
    healthcare provider for medical decisions. Research findings may not apply to all patients."
    """

    user_prompt = f"""
    Below is the extracted text from a research paper. Use only this text.
    Summarize it using the required format.

    --- PAPER CONTENT START ---
    {paper_text[:15000]}   # limit for safety
    --- PAPER CONTENT END ---
    """

    # ---------- CALL GROQ API ----------
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    result = completion.choices[0].message.content

    return {"summary": result}


# --------- Run Server ----------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
