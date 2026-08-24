# Smart Resume Screener

Parses resumes (PDF/TXT), extracts structured data (skills, experience,
education), and uses an LLM to compute a candidate-vs-job match score with
justification. Built for the Unthinkable Solutions assignment.

## Architecture

```
smart-resume-screener/
├── backend/                 FastAPI service
│   ├── app/
│   │   ├── main.py          App entrypoint, router wiring, CORS
│   │   ├── config.py        Env-based settings (.env)
│   │   ├── database.py      SQLAlchemy engine/session (SQLite)
│   │   ├── models.py        ORM models: Resume, JobDescription, ScreeningResult
│   │   ├── schemas.py       Pydantic request/response schemas
│   │   ├── parsers/
│   │   │   ├── resume_parser.py   PDF/TXT text extraction + structured extraction
│   │   │   └── skills_db.py       Skill/degree keyword taxonomy
│   │   ├── services/
│   │   │   ├── llm_service.py     LLM prompt + call + mock fallback
│   │   │   └── matcher.py         JD skill extraction, shortlist threshold
│   │   └── routers/
│   │       ├── resumes.py   Upload/list resumes
│   │       ├── jobs.py      Create/list job descriptions
│   │       └── screening.py Run match + list ranked results
│   └── requirements.txt
├── frontend/                 React (Vite) dashboard
│   └── src/
│       ├── App.jsx           Ties upload → JD → run screening → results
│       ├── api.js            Fetch wrapper for the backend API
│       └── components/       ResumeUpload, JobForm, ResultsTable
└── samples/                  Sample resume + JD for a quick demo run
```

**Flow:** upload resume → text + skills/education/experience extracted →
add job description → JD's required skills extracted with the same
taxonomy → "Run Match" calls the LLM (or mock) to score fit 1–10 with
justification → results are stored and ranked, with candidates scoring
≥ 7.0 flagged as shortlisted.

**Why SQLite:** zero-setup, file-based, native to Python (via SQLAlchemy) —
satisfies "database storage for parsed resumes" without adding infra
dependencies for a take-home assignment.

**Why a taxonomy-based extractor instead of a heavy NLP model:** the
submission guidelines ask to keep dependencies minimal and native. A curated
skill/degree keyword list gives reliable, explainable extraction without
pulling in spaCy/large ML models. It's easy to extend
(`app/parsers/skills_db.py`).

## LLM Usage

`app/services/llm_service.py` calls the Anthropic Messages API with a prompt
built from the assignment's suggested template, extended to force a
structured, parseable JSON response:

```
You are an expert technical recruiter.

Compare the following resume with this job description and rate the fit on
a scale of 1-10, with a clear justification.

Job Description:
"""{jd_text}"""

Resume:
"""{resume_text}"""

Candidate's extracted skills: {skills}
Job's required skills: {required_skills}

Respond with ONLY valid JSON in this exact shape, no other text:
{
  "match_score": <number from 1 to 10, one decimal allowed>,
  "justification": "<2-4 sentence explanation citing specific matched or missing skills/experience>",
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"]
}
```

Passing the pre-extracted skill lists alongside the raw text lets the model
ground its justification in specifics rather than vague praise, and the
forced-JSON format keeps the response reliably parseable.

**Mock fallback:** if `ANTHROPIC_API_KEY` is not set (or the API call fails
for any reason), `app/services/llm_service.py` falls back to a deterministic
scorer based on skill-set overlap between the resume and job description, so
the whole app still runs end-to-end without a paid API key. Mock-scored
results are clearly labeled as such in the justification text.

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # optionally add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs` (FastAPI Swagger UI).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at `https://smart-resume-screener-frontend-e46n.onrender.com`.

### Quick test without the frontend

```bash
curl -X POST http://localhost:8000/resumes/upload -F "file=@../samples/sample_resume.txt"
curl -X POST http://localhost:8000/jobs -H "Content-Type: application/json" \
  -d '{"title": "Backend Engineer", "raw_text": "<paste samples/sample_job_description.txt content>"}'
curl -X POST http://localhost:8000/screening/run -H "Content-Type: application/json" \
  -d '{"resume_id": 1, "job_id": 1}'
```

## API Endpoints

| Method | Endpoint                  | Description                              |
|--------|----------------------------|-------------------------------------------|
| POST   | `/resumes/upload`          | Upload a PDF/TXT resume, parse & store    |
| GET    | `/resumes`                 | List all parsed resumes                   |
| POST   | `/jobs`                    | Create a job description                  |
| GET    | `/jobs`                    | List job descriptions                     |
| POST   | `/screening/run`           | Run LLM match scoring for resume + job    |
| GET    | `/screening/job/{job_id}`  | List ranked results for a job (with `?shortlisted_only=true`) |

## Notes

- Shortlist threshold is 7.0/10, configurable in `app/services/matcher.py`.
- Uploaded files and the SQLite DB are gitignored (runtime data, not source).
- Only PDF and TXT resumes are accepted, per the assignment scope.
