import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central place for all configuration/env values."""

    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "").strip()
    LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./resume_screener.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")

    @property
    def llm_enabled(self) -> bool:
        """True if a real LLM key is configured, False -> mock scorer is used."""
        return bool(self.ANTHROPIC_API_KEY)


settings = Settings()
