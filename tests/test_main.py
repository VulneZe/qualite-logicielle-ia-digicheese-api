"""
Tests pour le point d'entrée principal de l'application digicheese-api
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app


def test_health_check():
    """Test du endpoint de santé"""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_openapi_docs():
    """Test que la documentation OpenAPI est accessible"""
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()


def test_swagger_docs():
    """Test que la documentation Swagger UI est accessible"""
    with TestClient(app) as client:
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()
