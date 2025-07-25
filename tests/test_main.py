"""
Testes para o módulo principal da aplicação.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    """Testa o endpoint de health check."""
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Sheets Integration API"
    assert data["version"] == "1.0.0"


def test_docs_endpoint():
    """Testa se a documentação está acessível."""
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Testa se o ReDoc está acessível."""
    client = TestClient(app)
    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_schema():
    """Testa se o schema OpenAPI está correto."""
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    assert schema["info"]["title"] == "Sheets Integration API"
    assert schema["info"]["version"] == "1.0.0" 