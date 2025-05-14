import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize("mode", ["explain", "reflect", "apply", "summarize", "ask"])
def test_llm_modes_valid(mode):
    response = client.post(
        "/api/v1/llm",
        json={
            "text": "¿Qué significa tener fe en medio de la prueba?",
            "mode": mode,
            "lang": "es",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)
    assert len(data["result"]) > 0


def test_llm_mode_ask_custom_question():
    response = client.post(
        "/api/v1/llm",
        json={
            "text": "¿Cuál es el mensaje principal del libro de Apocalipsis?",
            "mode": "ask",
            "lang": "es",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)
    assert len(data["result"]) > 0


def test_llm_missing_text():
    response = client.post("/api/v1/llm", json={"mode": "reflect", "lang": "es"})
    assert response.status_code == 422


def test_llm_invalid_mode():
    response = client.post(
        "/api/v1/llm",
        json={"text": "Este es un texto de prueba", "mode": "meditate", "lang": "es"},
    )
    assert response.status_code == 422


def test_llm_empty_text():
    response = client.post(
        "/api/v1/llm", json={"text": "   ", "mode": "apply", "lang": "es"}
    )
    assert response.status_code in [400, 422]
