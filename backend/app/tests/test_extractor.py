
import json
from unittest.mock import patch

from backend.app.extractor import extract_resume


def test_ai_extracts_skill_categories_and_evidence():
    resume_text = "Skills: Python, SQL, HTML, Git"

    fake_result = {
        "company": None,
        "role": "Student Developer",
        "name": "Asha Example",
        "email": "asha@example.com",
        "skills": [
            {
                "skill_name": "Python",
                "category_code": "COD",
                "evidence": "Python",
                "confidence": "high",
                "source_page": None,
                "claim_status": "claimed",
            },
            {
                "skill_name": "SQL",
                "category_code": "SQL",
                "evidence": "SQL",
                "confidence": "high",
                "source_page": None,
                "claim_status": "claimed",
            },
            {
                "skill_name": "HTML",
                "category_code": "SWE",
                "evidence": "HTML",
                "confidence": "high",
                "source_page": None,
                "claim_status": "claimed",
            },
            {
                "skill_name": "Git",
                "category_code": "SWE",
                "evidence": "Git",
                "confidence": "high",
                "source_page": None,
                "claim_status": "claimed",
            },
        ],
        "education": [],
        "projects": [],
        "experience": [],
        "internships": [],
        "hackathons": [],
        "certifications": [],
        "achievements": [],
    }

    fake_response = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(fake_result)
                }
            }
        ]
    }

    with patch("backend.app.extractor.httpx.post") as mock_post:
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.json.return_value = fake_response

        with patch.dict("os.environ", {"GROQ_API_KEY": "test-key"}):
            result = extract_resume(
                resume_text,
                hosted_consent=True,
            )

    categories = {
        skill["skill_name"]: skill["category_code"]
        for skill in result["skills"]
    }

    assert categories["Python"] == "COD"
    assert categories["SQL"] == "SQL"
    assert categories["HTML"] == "SWE"
    assert categories["Git"] == "SWE"

    for skill in result["skills"]:
        assert skill["evidence"] in resume_text
        assert skill["source_type"] == "document"
        assert skill["claim_status"] == "claimed"
def test_ai_marks_missing_evidence_for_review():
    resume_text = "Skills: Python, SQL"

    fake_result = {
        "company": None,
        "role": None,
        "name": "Asha Example",
        "email": "asha@example.com",
        "skills": [
            {
                "skill_name": "Python",
                "category_code": "COD",
                "evidence": "Java",
                "confidence": "high",
                "source_page": None,
                "claim_status": "claimed",
            }
        ],
        "education": [],
        "projects": [],
        "experience": [],
        "internships": [],
        "hackathons": [],
        "certifications": [],
        "achievements": [],
    }

    fake_response = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(fake_result)
                }
            }
        ]
    }

    with patch("backend.app.extractor.httpx.post") as mock_post:
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.json.return_value = fake_response

        with patch.dict("os.environ", {"GROQ_API_KEY": "test-key"}):
            result = extract_resume(
                resume_text,
                hosted_consent=True,
            )

    assert result["skills"][0]["claim_status"] == "needs_review"
