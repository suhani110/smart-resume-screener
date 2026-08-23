import json
import re
from typing import List

from app.config import settings

# The exact-style prompt suggested by the assignment brief, extended to
# request structured JSON so the API response is easy (and reliable) to parse.
PROMPT_TEMPLATE = """You are an expert technical recruiter.

Compare the following resume with this job description and rate the fit on a
scale of 1-10, with a clear justification.

Job Description:
\"\"\"{jd_text}\"\"\"

Resume:
\"\"\"{resume_text}\"\"\"

Candidate's extracted skills: {skills}
Job's required skills: {required_skills}

Respond with ONLY valid JSON in this exact shape, no other text:
{{
  "match_score": <number from 1 to 10, one decimal allowed>,
  "justification": "<2-4 sentence explanation citing specific matched or missing skills/experience>",
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"]
}}
"""


def _build_prompt(resume_text: str, jd_text: str, skills: List[str], required_skills: List[str]) -> str:
    return PROMPT_TEMPLATE.format(
        jd_text=jd_text[:6000],
        resume_text=resume_text[:6000],
        skills=", ".join(skills) if skills else "none detected",
        required_skills=", ".join(required_skills) if required_skills else "none detected",
    )


def _call_real_llm(prompt: str) -> dict:
    """Calls the Anthropic API and parses the JSON response."""
    import anthropic

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=settings.LLM_MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )
    return _parse_llm_json(raw_text)


def _parse_llm_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```json\s*|\s*```$", "", cleaned, flags=re.MULTILINE)
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find JSON in LLM response: {raw_text[:200]}")
    return json.loads(match.group(0))


def _mock_score(skills: List[str], required_skills: List[str]) -> dict:
    """
    Deterministic offline fallback used when no ANTHROPIC_API_KEY is set.
    Scores purely on skill-set overlap so the whole app still runs end-to-end
    without any paid API access.
    """
    skills_set = {s.lower() for s in skills}
    required_set = {s.lower() for s in required_skills}

    if not required_set:
        return {
            "match_score": 5.0,
            "justification": "No specific required skills were detected in the job "
            "description, so a neutral baseline score was assigned. (mock scorer - "
            "no LLM API key configured)",
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = sorted(skills_set & required_set)
    missing = sorted(required_set - skills_set)
    overlap_ratio = len(matched) / len(required_set)
    score = round(1 + overlap_ratio * 9, 1)  # scale 1-10

    justification = (
        f"(mock scorer - no LLM API key configured) Candidate matches "
        f"{len(matched)} of {len(required_set)} required skills "
        f"({round(overlap_ratio * 100)}%). "
    )
    if matched:
        justification += f"Strong overlap in: {', '.join(matched[:5])}. "
    if missing:
        justification += f"Missing: {', '.join(missing[:5])}."

    return {
        "match_score": score,
        "justification": justification.strip(),
        "matched_skills": matched,
        "missing_skills": missing,
    }


def score_resume_against_job(
    resume_text: str, jd_text: str, skills: List[str], required_skills: List[str]
) -> dict:
    """
    Main entry point. Uses the real LLM when an API key is configured,
    otherwise falls back to a deterministic mock scorer so the project
    always runs end-to-end.
    """
    if settings.llm_enabled:
        try:
            prompt = _build_prompt(resume_text, jd_text, skills, required_skills)
            return _call_real_llm(prompt)
        except Exception as exc:  # noqa: BLE001 - fall back gracefully on any API issue
            fallback = _mock_score(skills, required_skills)
            fallback["justification"] = (
                f"[LLM call failed, used mock fallback: {exc}] " + fallback["justification"]
            )
            return fallback

    return _mock_score(skills, required_skills)
