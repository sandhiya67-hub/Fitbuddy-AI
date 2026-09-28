"""Gemini gateway with a safe local fallback when no key is available."""
import logging
from collections.abc import Callable
from .config import GOOGLE_API_KEY, GEMINI_WORKOUT_MODEL, GEMINI_TIP_MODEL
logger = logging.getLogger(__name__)
def call(prompt: str, model: str, fallback: Callable[[], str]) -> str:
    if not GOOGLE_API_KEY: return fallback()
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        text = genai.GenerativeModel(model).generate_content(prompt).text
        if not text: raise RuntimeError("Gemini returned no text")
        return text.strip()
    except Exception as exc:
        logger.warning("Gemini unavailable; using local fallback: %s", exc)
        return fallback()
def workout(prompt, fallback): return call(prompt, GEMINI_WORKOUT_MODEL, fallback)
def tip(prompt, fallback): return call(prompt, GEMINI_TIP_MODEL, fallback)
