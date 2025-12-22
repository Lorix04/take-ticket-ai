"""Configurations"""

from functools import lru_cache
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Env setting"""
    amadeus_api_key: str | None = None
    amadeus_api_secret: str | None = None

    openai_api_key: str | None = None
    openai_model: str | None = None
    openai_temperature: float | None = None
    openai_base_url: str | None = None

    # Resolve .env in the project root (one level above app/)
    project_root: ClassVar[Path] = Path(__file__).resolve().parents[1]
    model_config = SettingsConfigDict(env_file=str(project_root / ".env"), extra="ignore")


@lru_cache
def get_settings():
    """Read settings"""
    return Settings()
