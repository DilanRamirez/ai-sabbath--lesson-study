import os
from pathlib import Path
from typing import Optional

# Directory where prompt templates are stored (each mode has its own .txt file)
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_template(mode: str) -> str:
    """
    Load the prompt template for the given mode from the prompts directory.
    """
    template_path = TEMPLATES_DIR / f"{mode}.txt"
    if not template_path.exists():
        raise FileNotFoundError(
            f"Template for mode '{mode}' not found at {template_path}"
        )
    return template_path.read_text(encoding="utf-8")


def truncate_context(context: str, max_chars: int = 2000) -> str:
    """
    Truncate the context string to at most `max_chars` characters,
    preserving the end of the text for relevance.
    """
    if len(context) <= max_chars:
        return context
    # Naive approach: keep the last max_chars characters
    return context[-max_chars:]


def build_prompt(
    mode: str,
    question: str,
    context: str,
    lang: str = "es",
    max_context_chars: Optional[int] = 2000,
) -> str:
    """
    Build the final LLM prompt by:
    1. Loading the template for `mode` (e.g., 'explain', 'reflect', 'apply', 'summarize', 'ask').
    2. Truncating the context to avoid exceeding token limits.
    3. Replacing placeholders in the template with the truncated context, question, and language.

    Templates should use placeholders:
      {context}, {question}, {lang}
    """
    print(
        # Debugging line to check the mode
        f"Building prompt for mode: {mode}"
    )
    # Load template text
    template = load_template(mode)
    print(f"Template: {template}")  # Debugging line to check the template

    # Truncate context if needed
    truncated = truncate_context(context, max_chars=max_context_chars)

    # Fill in placeholders
    prompt = template.format(context=truncated, question=question, lang=lang)
    print(f"Prompt: {prompt}")  # Debugging line to check the prompt
    return prompt
