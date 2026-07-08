from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from language import get_languages, get_language_name, normalize_language_code, validate_language
from models import DetectRequest, DetectResponse, LanguageResponse, TranslateRequest, TranslateResponse
from translator import TranslationService, TranslatorError

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
translation_service = TranslationService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Log API lifecycle events."""
    logger.info("API Started")
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API for AI Language Translator frontend integration.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    """Health endpoint for quick API checks."""
    return {"message": "Language Translator API Running"}


@app.get("/languages", response_model=list[LanguageResponse])
def languages() -> list[LanguageResponse]:
    """Return all languages supported by the translation service."""
    return [LanguageResponse(**language) for language in get_languages()]


@app.post("/translate", response_model=TranslateResponse)
def translate(payload: TranslateRequest) -> TranslateResponse:
    """Translate text from a source language into a target language."""
    source = normalize_language_code(payload.source)
    target = normalize_language_code(payload.target)

    if not validate_language(source):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "error": f"Unsupported source language: {payload.source}"},
        )

    if not validate_language(target):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "error": f"Unsupported target language: {payload.target}"},
        )

    if source == target:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "error": "Source and target languages must be different."},
        )

    logger.info("Translation Request: source=%s target=%s length=%s", source, target, len(payload.text))

    try:
        translated_text = translation_service.translate_text(
            text=payload.text,
            source=source,
            target=target,
        )
        logger.info("Translation Success: source=%s target=%s", source, target)
        return TranslateResponse(
            success=True,
            translated_text=translated_text,
            source=get_language_name(source),
            target=get_language_name(target),
        )
    except TranslatorError as exc:
        logger.warning("Translation Failure: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"success": False, "error": str(exc)},
        ) from exc
    except Exception as exc:
        logger.exception("Unknown translation error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "error": "Unexpected server error while translating text."},
        ) from exc


@app.post("/detect", response_model=DetectResponse)
def detect(payload: DetectRequest) -> DetectResponse:
    """Detect the language of the submitted text."""
    try:
        language_code = translation_service.detect_language(payload.text)
    except TranslatorError as exc:
        logger.warning("Language detection failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"success": False, "error": str(exc)},
        ) from exc
    except Exception as exc:
        logger.exception("Unknown detection error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "error": "Unexpected server error while detecting language."},
        ) from exc

    return DetectResponse(language=get_language_name(language_code), code=language_code)
