import datetime
import json

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(255), default="Unknown Candidate")
    filename = Column(String(255))
    raw_text = Column(Text)
    skills = Column(Text, default="[]")          # JSON-encoded list[str]
    education = Column(Text, default="[]")        # JSON-encoded list[str]
    experience_years = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    results = relationship("ScreeningResult", back_populates="resume")

    def skills_list(self):
        return json.loads(self.skills or "[]")

    def education_list(self):
        return json.loads(self.education or "[]")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    raw_text = Column(Text)
    required_skills = Column(Text, default="[]")  # JSON-encoded list[str]
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    results = relationship("ScreeningResult", back_populates="job")

    def required_skills_list(self):
        return json.loads(self.required_skills or "[]")


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    match_score = Column(Float)          # 1-10 scale from the LLM
    justification = Column(Text)
    matched_skills = Column(Text, default="[]")
    missing_skills = Column(Text, default="[]")
    shortlisted = Column(Integer, default=0)  # 1/0 boolean flag
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    resume = relationship("Resume", back_populates="results")
    job = relationship("JobDescription", back_populates="results")
