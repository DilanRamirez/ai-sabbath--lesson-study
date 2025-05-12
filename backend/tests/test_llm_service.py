import pytest
from unittest.mock import patch, MagicMock
from app.services.llm_service import generate_llm_response
from app.services.prompts.sabbath import build_prompt


# --- TEST build_prompt ---


def test_build_prompt_explain_english():
    prompt = build_prompt("explain", "Isaiah 53:5", lang="en")
    assert "Explain the meaning" in prompt
    assert "<TextToAnalyze>" in prompt
    assert "Isaiah 53:5" in prompt
    assert "Please write your response in English" in prompt


def test_build_prompt_reflect_spanish():
    prompt = build_prompt("reflect", "Juan 3:16", lang="es")
    assert "Please write your response in Spanish" in prompt
    assert "Juan 3:16" in prompt
    assert "<Instructions>" in prompt


def test_build_prompt_invalid_mode_defaults():
    prompt = build_prompt("unknown_mode", "John 1:1", lang="en")
    assert "Provide spiritual insight" in prompt


# --- TEST generate_llm_response ---


@patch("app.services.llm_service.model.generate_content")
def test_generate_llm_response_valid(mock_generate):
    mock_generate.return_value = MagicMock(text="Jesus died for our sins.")
    result = generate_llm_response("Isaiah 53:5", "explain", "en")
    assert isinstance(result, str)
    assert "Jesus" in result


@patch("app.services.llm_service.model.generate_content")
def test_generate_llm_response_spanish(mock_generate):
    mock_generate.return_value = MagicMock(text="Jesús murió por nuestros pecados.")
    result = generate_llm_response("Isaías 53:5", "explain", "es")
    assert "Jesús" in result


@patch("app.services.llm_service.model.generate_content")
def test_generate_llm_response_error_handling(mock_generate):
    mock_generate.side_effect = Exception("Gemini is down")
    result = generate_llm_response("Isaiah 53:5", "reflect", "en")
    assert result.startswith("[Error with Gemini SDK:")
