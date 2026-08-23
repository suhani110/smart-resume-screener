import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import JobDescription, Resume, ScreeningResult
from app.schemas import ScreeningRequest, ScreeningResultOut
from app.services.llm_service import score_resume_against_job
from app.services.matcher import is_shortlisted

router = APIRouter(prefix="/screening", tags=["screening"])


def _to_out(result: ScreeningResult, candidate_name: str) -> ScreeningResultOut:
    return ScreeningResultOut(
        id=result.id,
        resume_id=result.resume_id,
        job_id=result.job_id,
        candidate_name=candidate_name,
        match_score=result.match_score,
        justification=result.justification,
        matched_skills=json.loads(result.matched_skills or "[]"),
        missing_skills=json.loads(result.missing_skills or "[]"),
        shortlisted=bool(result.shortlisted),
    )


@router.post("/run", response_model=ScreeningResultOut)
def run_screening(payload: ScreeningRequest, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id).first()
    job = db.query(JobDescription).filter(JobDescription.id == payload.job_id).first()
    if not resume:
        raise HTTPException(404, "Resume not found")
    if not job:
        raise HTTPException(404, "Job description not found")

    llm_result = score_resume_against_job(
        resume_text=resume.raw_text,
        jd_text=job.raw_text,
        skills=resume.skills_list(),
        required_skills=job.required_skills_list(),
    )

    score = float(llm_result.get("match_score", 0))
    result = ScreeningResult(
        resume_id=resume.id,
        job_id=job.id,
        match_score=score,
        justification=llm_result.get("justification", ""),
        matched_skills=json.dumps(llm_result.get("matched_skills", [])),
        missing_skills=json.dumps(llm_result.get("missing_skills", [])),
        shortlisted=int(is_shortlisted(score)),
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return _to_out(result, resume.candidate_name)


@router.get("/job/{job_id}", response_model=List[ScreeningResultOut])
def list_results_for_job(job_id: int, shortlisted_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(ScreeningResult).filter(ScreeningResult.job_id == job_id)
    if shortlisted_only:
        query = query.filter(ScreeningResult.shortlisted == 1)
    results = query.order_by(ScreeningResult.match_score.desc()).all()

    out = []
    for r in results:
        candidate_name = r.resume.candidate_name if r.resume else "Unknown"
        out.append(_to_out(r, candidate_name))
    return out
