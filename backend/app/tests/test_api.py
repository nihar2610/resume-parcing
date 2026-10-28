
from fastapi.testclient import TestClient
from backend.app.main import app
from io import BytesIO
from docx import Document

client = TestClient(app)


def test_health():
    response = client.get("/api/team/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_reject_unsupported_file():
    response = client.post(
        "/api/team/v1/resumes/extract",
        files={
            "file": ("resume.txt", b"Some resume text", "text/plain")
        },
        data={"hosted_consent": "false"},
    )

    assert response.status_code == 400


def test_reject_large_file():
    large_content = b"a" * (5 * 1024 * 1024 + 1)

    response = client.post(
        "/api/team/v1/resumes/extract",
        files={
            "file": ("resume.pdf", large_content, "application/pdf")
        },
        data={"hosted_consent": "false"},
    )

    assert response.status_code == 413


def test_reject_empty_resume():
    document = Document()
    buffer = BytesIO()
    document.save(buffer)
    empty_docx = buffer.getvalue()

    response = client.post(
        "/api/team/v1/resumes/extract",
        files={
            "file": (
                "empty.docx",
                empty_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        data={"hosted_consent": "false"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No readable text found"


def test_extract_rejects_missing_file():
    response = client.post(
        "/api/team/v1/resumes/extract",
        data={"hosted_consent": "false"},
    )

    assert response.status_code == 422
