from app.parsers.resume_parser import extract_skills

SHORTLIST_THRESHOLD = 7.0  # match_score >= this value => shortlisted


def extract_required_skills(jd_text: str):
    """Reuses the same taxonomy-based extractor for the job description text."""
    return extract_skills(jd_text)


def is_shortlisted(match_score: float) -> bool:
    return match_score >= SHORTLIST_THRESHOLD
