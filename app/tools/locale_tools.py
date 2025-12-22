from functools import lru_cache
from typing import Optional

from config import get_settings

try:
    from langchain_openai import ChatOpenAI  # type: ignore
except Exception:  # pragma: no cover
    ChatOpenAI = None  # type: ignore


@lru_cache
def _get_llm() -> Optional[object]:
    settings = get_settings()
    if not ChatOpenAI or not settings.openai_api_key:
        return None
    try:
        return ChatOpenAI(
            model=settings.openai_model or "gpt-5-mini",
            temperature=settings.openai_temperature or 0,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
    except Exception:
        return None


_IT_EN_SYNONYMS = {
    # Cities
    "roma": "rome",
    "milano": "milan",
    "firenze": "florence",
    "napoli": "naples",
    "venezia": "venice",
    "torino": "turin",
    "genova": "genoa",
    "bologna": "bologna",
    "monaco": "munich",  # ambiguity: Monaco (IT) vs Munich (DE)
    # Countries (if ever used)
    "italia": "italy",
    "stati uniti": "united states",
    "regno unito": "united kingdom",
    "spagna": "spain",
    "francia": "france",
    "germania": "germany",
}


@lru_cache
def translate_to_english(text: str) -> str:
    """Translate a location name to English. Uses small dict + LLM fallback.
    Returns original text if translation not possible.
    """
    if not text:
        return text
    t = text.strip()
    low = t.lower()
    if low in _IT_EN_SYNONYMS:
        return _IT_EN_SYNONYMS[low]

    llm = _get_llm()
    if not llm:
        return t

    prompt = (
        "You are a translation utility. Translate the following place name to English. "
        "Return only the translated name without extra words, punctuation or quotes.\n"
        f"Text: {t}"
    )
    try:
        resp = llm.invoke(prompt)  # type: ignore
        content = getattr(resp, "content", "")
        if isinstance(content, str):
            out = content.strip()
        else:
            out = str(content).strip()
        # basic cleanup
        out = out.strip('"\'\n ')
        return out or t
    except Exception:
        return t
