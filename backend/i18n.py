import json
from pathlib import Path

DEFAULT_LOCALE = "en"
SUPPORTED_LOCALES = ("en", "ja", "ko")

_LOCALES_DIR = Path(__file__).parent / "locales"

def _load_catalog() -> dict[str, dict[str, str]]:
    catalog = {}
    for locale in SUPPORTED_LOCALES:
        path = _LOCALES_DIR / f"{locale}.json"
        with open(path, encoding="utf-8") as f:
            catalog[locale] = json.load(f)
    return catalog

_MESSAGES = _load_catalog()

def normalize_locale(language: str | None) -> str:
    if not language:
        return DEFAULT_LOCALE
    code = language.lower().split("-")[0]
    return code if code in SUPPORTED_LOCALES else DEFAULT_LOCALE

def t(language: str | None, key: str) -> str:
    locale = normalize_locale(language)
    messages = _MESSAGES.get(locale, _MESSAGES[DEFAULT_LOCALE])
    return messages.get(key) or _MESSAGES[DEFAULT_LOCALE].get(key) or key