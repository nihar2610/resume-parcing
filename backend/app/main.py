
import os
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from backend.app.extractor import extract_resume
from backend.app.models import Extraction
from backend.app.reader import read_resume
from backend.app.manual_extractor import extract_manual
app = FastAPI(title="Resume Parser API")

@app.get("/api/team/v1/health")
def health():
    return {"status": "ok"}


@app.post("/api/team/v1/resumes/extract", response_model=Extraction)
async def extract_uploaded_resume(
    file: UploadFile = File(...),
    hosted_consent: bool = Form(False)
):
    if not file.filename or not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(400, "Upload a PDF or DOCX file")

    content = await file.read()

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(413, "File must be under 5 MB")

    try:
        text = read_resume(content, file.filename)

        if not text.strip():
            raise HTTPException(400, "No readable text found")

        warnings = []
        result = {}

        
        if hosted_consent:
            try:
                result = extract_resume(text, hosted_consent=True)
                method = "groq"
            except RuntimeError as e:
                if "API key is not configured" in str(e):
                    raise HTTPException(503, str(e))
                raise HTTPException(502, "AI extraction failed")
        else:
            result = extract_manual(text)
            method = "manual"


        return Extraction(
            schema_version="TEAM-V1",
            id=str(uuid.uuid4()),
            revision=1,
            source_type="resume",
            source_file=Path(file.filename).name,
            source_text=text,
            company=result.get("company"),
            role=result.get("role"),
            name=result.get("name", ""),
            email=result.get("email", ""),
            skills=result.get("skills", []),
            requirement_groups=[],
            education=result.get("education", []),
            projects=result.get("projects", []),
            experience=result.get("experience", []),
            internships=result.get("internships", []),
            hackathons=result.get("hackathons", []),
            certifications=result.get("certifications", []),
            achievements=result.get("achievements", []),
            review_status="needs_review",
            extraction_method=method,
            warnings=warnings + result.get("warnings", [])
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(400, str(e))
