from typing import List, Optional

from pydantic import BaseModel


class ResumeOut(BaseModel):
    id: int
    candidate_name: str
    filename: str
    skills: List[str]
    education: List[str]
    experience_years: float

    class Config:
        from_attributes = True


class JobDescriptionIn(BaseModel):
    title: str
    raw_text: str


class JobDescriptionOut(BaseModel):
    id: int
    title: str
    required_skills: List[str]

    class Config:
        from_attributes = True


class ScreeningRequest(BaseModel):
    resume_id: int
    job_id: int


class ScreeningResultOut(BaseModel):
    id: int
    resume_id: int
    job_id: int
    candidate_name: str
    match_score: float
    justification: str
    matched_skills: List[str]
    missing_skills: List[str]
    shortlisted: bool

    class Config:
        from_attributes = True
