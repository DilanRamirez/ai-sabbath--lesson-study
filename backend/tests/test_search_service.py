import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_valid_query_returns_results():
    response = client.get("/api/v1/search?q=evangelio")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert "query" in data
    assert data["query"] == "evangelio"
    assert all("score" in r and "normalized_score" in r for r in data["results"])


def test_search_empty_query():
    response = client.get("/api/v1/search?q=")
    assert response.status_code == 422  # FastAPI will validate missing required query


def test_search_invalid_type_filter():
    response = client.get("/api/v1/search?q=esperanza&type=invalid")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_search_top_k_too_high():
    response = client.get("/api/v1/search?q=fe&top_k=100")
    assert response.status_code == 422  # max is 20 as per route definition


def test_search_top_k_too_low():
    response = client.get("/api/v1/search?q=fe&top_k=0")
    assert response.status_code == 422  # min is 1 as per route definition


def test_search_with_type_lesson():
    response = client.get("/api/v1/search?q=gracia&type=lesson")
    assert response.status_code == 200
    data = response.json()
    assert all(
        r.get("type") == "lesson" or r.get("type") == "lesson-section"
        for r in data["results"]
    )


def test_search_with_type_book():
    response = client.get("/api/v1/search?q=vida&type=book")
    assert response.status_code == 200
    data = response.json()
    assert all(
        r.get("type") == "book" or r.get("type") == "book-section"
        for r in data["results"]
    )
