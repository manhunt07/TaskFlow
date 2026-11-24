from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "TaskFlow"
    assert data["version"] == "0.1.0"


def test_versioned_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "TaskFlow API"
    assert data["version"] == "0.1.0"

    # Verify the timestamp is valid ISO 8601.
    datetime.fromisoformat(data["timestamp"])


def test_legacy_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_unknown_endpoint_returns_404():
    response = client.get("/api/v1/not-found")

    assert response.status_code == 404
