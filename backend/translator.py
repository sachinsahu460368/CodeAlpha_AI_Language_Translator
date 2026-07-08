from __future__ import annotations

import re
from collections import Counter

from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException, NotValidPayload

from language import validate_language


class TranslatorError(Exception):
    """Raised when translation or detection cannot be completed cleanly."""


class TranslationService:
    """Service layer for translation and language detection operations."""

    _SCRIPT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
        ("hi", re.compile(r"[\u0900-\u097F]")),
        ("bn", re.compile(r"[\u0980-\u09FF]")),
        ("pa", re.compile(r"[\u0A00-\u0A7F]")),
        ("gu", re.compile(r"[\u0A80-\u0AFF]")),
        ("ta", re.compile(r"[\u0B80-\u0BFF]")),
        ("te", re.compile(r"[\u0C00-\u0C7F]")),
        ("kn", re.compile(r"[\u0C80-\u0CFF]")),
        ("ml", re.compile(r"[\u0D00-\u0D7F]")),
        ("si", re.compile(r"[\u0D80-\u0DFF]")),
        ("th", re.compile(r"[\u0E00-\u0E7F]")),
        ("lo", re.compile(r"[\u0E80-\u0EFF]")),
        ("my", re.compile(r"[\u1000-\u109F]")),
        ("ka", re.compile(r"[\u10A0-\u10FF]")),
        ("ja", re.compile(r"[\u3040-\u30FF]")),
        ("ko", re.compile(r"[\uAC00-\uD7AF]")),
        ("zh-CN", re.compile(r"[\u4E00-\u9FFF]")),
        ("ar", re.compile(r"[\u0600-\u06FF]")),
        ("iw", re.compile(r"[\u0590-\u05FF]")),
        ("ru", re.compile(r"[\u0400-\u04FF]")),
        ("el", re.compile(r"[\u0370-\u03FF]")),
    )

    _LATIN_LANGUAGE_HINTS: dict[str, set[str]] = {
        "en": {"the", "and", "is", "are", "hello", "please", "good", "morning", "you"},
        "es": {"el", "la", "los", "las", "hola", "gracias", "por", "favor", "buenos"},
        "fr": {"le", "la", "les", "bonjour", "merci", "vous", "pour", "avec", "une"},
        "de": {"der", "die", "das", "hallo", "danke", "und", "ist", "bitte", "guten"},
        "it": {"il", "lo", "la", "ciao", "grazie", "per", "con", "buongiorno"},
        "pt": {"o", "a", "os", "as", "ola", "obrigado", "por", "favor", "bom"},
    }

    def translate_text(self, text: str, source: str, target: str) -> str:
        """Translate text using deep-translator."""
        if not validate_language(source):
            raise TranslatorError(f"Unsupported source language: {source}")
        if not validate_language(target):
            raise TranslatorError(f"Unsupported target language: {target}")

        try:
            translated = GoogleTranslator(source=source, target=target).translate(text)
        except LanguageNotSupportedException as exc:
            raise TranslatorError("Unsupported language supplied to translation service.") from exc
        except NotValidPayload as exc:
            raise TranslatorError("Translation input is not valid.") from exc
        except ConnectionError as exc:
            raise TranslatorError("Internet connection failed while translating text.") from exc
        except Exception as exc:
            raise TranslatorError("Translation service failed. Please try again later.") from exc

        if not translated:
            raise TranslatorError("Translation service returned an empty response.")

        return translated

    def detect_language(self, text: str) -> str:
        """Detect language without requiring a paid detection API key."""
        script_code = self._detect_by_script(text)
        if script_code:
            return script_code

        latin_code = self._detect_latin_language(text)
        if latin_code:
            return latin_code

        return "en"

    def _detect_by_script(self, text: str) -> str | None:
        """Detect languages that use distinctive Unicode script ranges."""
        matches: Counter[str] = Counter()
        for code, pattern in self._SCRIPT_PATTERNS:
            match_count = len(pattern.findall(text))
            if match_count:
                matches[code] = match_count

        if not matches:
            return None

        detected_code = matches.most_common(1)[0][0]
        return detected_code if validate_language(detected_code) else None

    def _detect_latin_language(self, text: str) -> str | None:
        """Detect common Latin-script languages using lightweight word hints."""
        words = re.findall(r"[a-zA-ZÀ-ÿ]+", text.lower())
        if not words:
            return None

        word_counts = Counter(words)
        scores = {
            code: sum(word_counts[word] for word in hints)
            for code, hints in self._LATIN_LANGUAGE_HINTS.items()
        }
        best_code, best_score = max(scores.items(), key=lambda item: item[1])
        return best_code if best_score > 0 and validate_language(best_code) else None
