import json
import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Resume
from app.parsers.resume_parser import parse_resume
from app.schemas import ResumeOut

router = APIRouter(prefix="/resumes", tags=["resumes"])

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post("/upload", response_model=ResumeOut)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type '{ext}'. Only PDF or TXT allowed.")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    saved_name = f"{uuid.uuid4().hex}{ext}"
    saved_path = os.path.join(settings.UPLOAD_DIR, saved_name)

    with open(saved_path, "wb") as f:
        f.write(await file.read())

    name, raw_text, skills, education, experience = parse_resume(saved_path, file.filename)

    resume = Resume(
        candidate_name=name,
        filename=file.filename,
        raw_text=raw_text,
        skills=json.dumps(skills),
        education=json.dumps(education),
        experience_years=experience,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return ResumeOut(
        id=resume.id,
        candidate_name=resume.candidate_name,
        filename=resume.filename,
        skills=skills,
        education=education,
        experience_years=experience,
    )


@router.get("", response_model=List[ResumeOut])
def list_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).order_by(Resume.id.desc()).all()
    return [
        ResumeOut(
            id=r.id,
            candidate_name=r.candidate_name,
            filename=r.filename,
            skills=r.skills_list(),
            education=r.education_list(),
            experience_years=r.experience_years,
        )
        for r in resumes
    ]


@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    r = db.query(Resume).filter(Resume.id == resume_id).first()
    if not r:
        raise HTTPException(404, "Resume not found")
    return ResumeOut(
        id=r.id,
        candidate_name=r.candidate_name,
        filename=r.filename,
        skills=r.skills_list(),
        education=r.education_list(),
        experience_years=r.experience_years,
    )
