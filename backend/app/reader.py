
from io import BytesIO
from pypdf import PdfReader
from docx import Document

def read_resume(content, filename):
    if filename.lower().endswith(".pdf"):
        pdf = PdfReader(BytesIO(content))
        return "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    elif filename.lower().endswith(".docx"):
        doc = Document(BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        raise ValueError("Only PDF and DOCX files are supported")
