import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import JobDescription
from app.schemas import JobDescriptionIn, JobDescriptionOut
from app.services.matcher import extract_required_skills

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobDescriptionOut)
def create_job(payload: JobDescriptionIn, db: Session = Depends(get_db)):
    required_skills = extract_required_skills(payload.raw_text)
    job = JobDescription(
        title=payload.title,
        raw_text=payload.raw_text,
        required_skills=json.dumps(required_skills),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return JobDescriptionOut(id=job.id, title=job.title, required_skills=required_skills)


@router.get("", response_model=List[JobDescriptionOut])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobDescription).order_by(JobDescription.id.desc()).all()
    return [
        JobDescriptionOut(id=j.id, title=j.title, required_skills=j.required_skills_list())
        for j in jobs
    ]


@router.get("/{job_id}", response_model=JobDescriptionOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    j = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not j:
        raise HTTPException(404, "Job description not found")
    return JobDescriptionOut(id=j.id, title=j.title, required_skills=j.required_skills_list())
