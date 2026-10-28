
from typing import Literal
from pydantic import BaseModel, ConfigDict
import uuid
from pathlib import Path

class Skill(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skill_id: str
    skill_name: str
    category_code: Literal[
        "COD", "DSA", "OOD", "APTI", "COMM", "AI",
        "CLOUD", "SQL", "SWE", "SYSD", "NETW", "OS", "OTHER"
    ]
    evidence: str
    confidence: Literal["high", "medium", "low"]
    source_type: Literal["document", "manual", "hypothetical"]
    source_id: str | None
    source_page: int | None
    claim_status: Literal["claimed", "needs_review"]


class RequirementGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requirement_id: str
    skill_ids: list[str]
    operator: Literal["AND", "OR"]
    requirement_type: Literal["mandatory", "preferred", "unspecified"]
    evidence: str


class Extraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["TEAM-V1"]
    id: str
    revision: int
    source_type: Literal["jd", "resume"]
    source_file: str
    source_text: str
    company: str | None
    role: str | None
    name: str
    email: str
    skills: list[Skill]
    requirement_groups: list[RequirementGroup]
    education: list[str]
    projects: list[str]
    experience: list[str]
    internships: list[str]
    hackathons: list[str]
    certifications: list[str]
    achievements: list[str]
    review_status: Literal["needs_review", "reviewed"]
    extraction_method: Literal["groq", "manual", "rules"]
    warnings: list[str]
