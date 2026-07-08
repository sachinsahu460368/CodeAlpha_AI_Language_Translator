from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class LanguageResponse(BaseModel):
    """Supported language response item."""

    name: str
    code: str


class TranslateRequest(BaseModel):
    """Request body for translation."""

    text: str = Field(..., min_length=1, max_length=5000, examples=["Hello"])
    source: str = Field(..., min_length=2, examples=["en"])
    target: str = Field(..., min_length=2, examples=["hi"])

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Text cannot be empty.")
        return cleaned

    @field_validator("source", "target")
    @classmethod
    def language_code_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Language code cannot be empty.")
        return cleaned


class TranslateResponse(BaseModel):
    """Successful translation response."""

    success: bool
    translated_text: str
    source: str
    target: str


class DetectRequest(BaseModel):
    """Request body for language detection."""

    text: str = Field(..., min_length=1, max_length=5000, examples=["Namaste"])

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Text cannot be empty.")
        return cleaned


class DetectResponse(BaseModel):
    """Language detection response."""

    language: str
    code: str
