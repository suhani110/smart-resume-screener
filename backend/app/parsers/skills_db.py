"""
A lightweight, dependency-free skill taxonomy.

Kept as plain Python data (no external NLP model) to satisfy the assignment's
"minimal dependencies" requirement while still giving reasonably accurate
structured extraction. Extend this list to widen extraction coverage.
"""

SKILLS_TAXONOMY = [
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "php", "ruby", "kotlin", "swift", "scala", "r", "matlab",
    # Web / frontend
    "react", "angular", "vue", "next.js", "html", "css", "tailwind", "redux",
    # Backend / frameworks
    "node.js", "express", "django", "flask", "fastapi", "spring boot",
    "spring", ".net", "graphql", "rest api",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "dynamodb", "elasticsearch",
    # Cloud / devops
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
    "ci/cd", "linux", "git", "github actions",
    # Data / ML
    "machine learning", "deep learning", "nlp", "pandas", "numpy",
    "tensorflow", "pytorch", "scikit-learn", "data analysis", "llm",
    "prompt engineering", "generative ai",
    # Soft / general
    "agile", "scrum", "microservices", "system design", "unit testing",
    "api design", "communication", "leadership", "project management",
]

DEGREE_KEYWORDS = [
    "b.tech", "b.e.", "bachelor", "bsc", "b.sc", "bca",
    "m.tech", "m.e.", "master", "msc", "m.sc", "mca", "mba",
    "phd", "ph.d", "doctorate", "diploma",
]
