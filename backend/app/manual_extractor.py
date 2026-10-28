

import re
import uuid

def extract_manual(text):
    email = re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    name = ""
    if lines and not any(x in lines[0].lower() for x in ["resume", "cv", "email"]):
        name = lines[0].title()

    sections = {
        "education": [], "projects": [], "experience": [],
        "internships": [], "hackathons": [],
        "certifications": [], "achievements": []
    }

    current = None
    for line in lines:
        heading = line.lower().strip(":")
        if heading in sections:
            current = heading
        elif heading in ["technical skills", "skills"]:
            current = "skills"
        elif heading in ["career objective", "additional information"]:
            current = None
        elif current in sections:
            sections[current].append(line)

    skill_names = [
        "Python", "C", "C++", "Java", "SQL", "MySQL",
        "HTML", "CSS", "JavaScript", "Git", "GitHub"
    ]

    categories = {
        "Python": "COD", "C": "COD", "C++": "COD", "Java": "COD",
        "SQL": "SQL", "MySQL": "SQL",
        "HTML": "SWE", "CSS": "SWE", "JavaScript": "SWE",
        "Git": "SWE", "GitHub": "SWE"
    }

    skills = [
        {
            "skill_id": str(uuid.uuid4()),
            "skill_name": s,
            "category_code": categories[s],
            "evidence": s,
            "confidence": "medium",
            "source_type": "document",
            "source_id": "resume",
            "source_page": None,
            "claim_status": "claimed"
        }
        for s in skill_names
        if re.search(r'(?<!\w)' + re.escape(s) + r'(?!\w)', text, re.I)
    ]

    return {
        "name": name,
        "email": email.group(0) if email else "",
        "skills": skills,
        **sections
    }
