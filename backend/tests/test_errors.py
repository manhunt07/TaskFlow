from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_existing_project():
    response = client.get(
        "/api/v1/examples/projects/1"
    )

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "name": "TaskFlow Development",
    }


def test_missing_project():
    response = client.get(
        "/api/v1/examples/projects/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "error": {
            "code": "PROJECT_NOT_FOUND",
            "message": "Project not found",
        }
    }


def test_invalid_project_id():
    response = client.get(
        "/api/v1/examples/projects/abc"
    )

    assert response.status_code == 422

    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
        }
    }


def test_unknown_api_endpoint():
    response = client.get(
        "/api/v1/unknown"
    )

    assert response.status_code == 404

    assert response.json() == {
        "error": {
            "code": "NOT_FOUND",
            "message": "Not Found",
        }
    }
