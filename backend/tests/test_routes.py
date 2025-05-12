import pytest
from unittest.mock import patch
from pathlib import Path

# ---- Lesson Index ----


def test_list_lessons(client):
    res = client.get("/api/v1/lessons")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert "year" in res.json()[0]
    assert "lesson_id" in res.json()[0]


# ---- Lesson Content ----


def test_get_lesson_valid(client):
    res = client.get("/api/v1/lessons/2025/Q2/lesson-06")
    assert res.status_code == 200
    assert "lesson" in res.json()


def test_get_lesson_invalid(client):
    res = client.get("/api/v1/lessons/2025/Q2/fake-lesson")
    assert res.status_code == 404
    assert res.json()["detail"] == "Lesson not found"


# ---- Metadata ----


def test_get_metadata_valid(client):
    res = client.get("/api/v1/lessons/2025/Q2/lesson-06/metadata")
    assert res.status_code == 200
    assert "title" in res.json()


def test_get_metadata_invalid(client):
    res = client.get("/api/v1/lessons/2025/Q2/unknown/metadata")
    assert res.status_code == 404
    assert res.json()["detail"] == "Metadata not found"


# ---- PDF (mocked) ----


def test_get_pdf_invalid(client):
    res = client.get("/api/v1/lessons/2025/Q2/bogus/pdf")
    assert res.status_code == 404
    assert res.json()["detail"] == "PDF file not found"


# ---- LLM Prompts ----


def test_llm_explain_valid(client):
    res = client.post(
        "/api/v1/llm?lang=en", json={"text": "Isaías 53:5", "mode": "explain"}
    )
    assert res.status_code == 200
    assert "result" in res.json()
    assert isinstance(res.json()["result"], str)


def test_llm_invalid_mode(client):
    res = client.post(
        "/api/v1/llm?lang=en", json={"text": "Something", "mode": "nonsense"}
    )
    assert res.status_code == 422  # FastAPI validation fails


def test_llm_missing_fields(client):
    res = client.post("/api/v1/llm", json={})
    assert res.status_code == 422
