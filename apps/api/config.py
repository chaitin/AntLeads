"""Application configuration."""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    APP_NAME: str = "AntLeads"
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "*"]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./antleads.db"

    # AI Scoring
    AI_SCORING_ENABLED: bool = True
    AI_MODEL_NAME: str = "gpt-4"
    OPENAI_API_KEY: str = ""

    # Task automation
    AUTO_TASK_ENABLED: bool = True
    DEFAULT_FOLLOW_UP_DAYS: int = 3


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
