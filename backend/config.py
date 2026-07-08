from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Language Translator API"
    app_version: str = "1.0.0"
    log_level: str = "INFO"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://127.0.0.1:3000", "http://localhost:3000"]
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
