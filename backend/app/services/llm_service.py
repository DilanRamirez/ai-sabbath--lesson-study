import google.generativeai as genai
from typing import Literal
import logging

from app.core.config import settings
from app.core.prompt_builder import build_prompt


# Initialize Gemini client
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")


def generate_llm_response(
    text: str,
    mode: Literal["explain", "reflect", "apply", "summarize"],
    context_text: str,
    lang: str = "en",
) -> str:
    if not text or not text.strip():
        return "[Error: Empty input provided to LLM]"
    try:
        # instead of inline string, call:
        prompt = build_prompt(mode, text, context_text, lang)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Error generating LLM response: {e}")
        return f"[Error with Gemini SDK: {str(e)}]"
