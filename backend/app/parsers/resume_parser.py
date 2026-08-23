import re
from typing import List, Tuple

import pdfplumber

from app.parsers.skills_db import DEGREE_KEYWORDS, SKILLS_TAXONOMY

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
EXPERIENCE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs)\s*(?:of)?\s*(?:experience|exp)?",
    re.IGNORECASE,
)


def extract_text(file_path: str) -> str:
    """Extract raw text from a PDF or plain-text resume file."""
    if file_path.lower().endswith(".pdf"):
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
        return "\n".join(text_parts)

    # Fallback: treat as plain text (.txt)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def guess_candidate_name(text: str, filename: str) -> str:
    """Best-effort guess: first non-empty line that isn't an email/contact line."""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if EMAIL_RE.search(line) or any(ch.isdigit() for ch in line):
            continue
        if 2 <= len(line.split()) <= 5:
            return line.title()
        break
    return filename.rsplit(".", 1)[0].replace("_", " ").title()


def extract_skills(text: str) -> List[str]:
    lowered = text.lower()
    found = set()
    for skill in SKILLS_TAXONOMY:
        # word-boundary-ish match so "r" doesn't match inside other words
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, lowered):
            found.add(skill)
    return sorted(found)


def extract_education(text: str) -> List[str]:
    lowered = text.lower()
    found = set()
    for kw in DEGREE_KEYWORDS:
        if kw in lowered:
            found.add(kw.upper() if len(kw) <= 5 else kw.title())
    return sorted(found)


def extract_experience_years(text: str) -> float:
    matches = EXPERIENCE_RE.findall(text)
    years = [float(m) for m in matches if m]
    return max(years) if years else 0.0


def parse_resume(file_path: str, filename: str) -> Tuple[str, str, List[str], List[str], float]:
    """Returns (candidate_name, raw_text, skills, education, experience_years)."""
    text = extract_text(file_path)
    name = guess_candidate_name(text, filename)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience_years(text)
    return name, text, skills, education, experience
