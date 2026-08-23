from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import jobs, resumes, screening

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Resume Screener API",
    description="Parses resumes, extracts structured data, and uses an LLM "
    "to score candidate fit against a job description.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # relaxed for local/demo use only
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resumes.router)
app.include_router(jobs.router)
app.include_router(screening.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "smart-resume-screener"}
