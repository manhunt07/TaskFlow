from fastapi.testclient import TestClient #provides a way to test FastAPI applications by simulating HTTP requests

from app.main import app


client = TestClient(app)

ENDPOINT = "/api/v1/examples/validate-task"  #provides the endpoint for the TaskFlow task example validation API, which is used in the test cases to send requests and receive responses


def test_valid_task():    #
    response = client.post(
        ENDPOINT,
        json={
            "title": "Deploy TaskFlow",
            "priority": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "validated"
    assert data["task"]["title"] == "Deploy TaskFlow"
    assert data["task"]["priority"] == 3


def test_missing_title():  #verifies that the API returns a validation error when the title field is missing
    response = client.post(
        ENDPOINT,
        json={"priority": 3},
    )

    assert response.status_code == 422

    assert response.json()["error"]["code"] == (
        "VALIDATION_ERROR"
    )


def test_invalid_priority():  #verifies that the API returns a validation error when the priority field is outside the allowed range (1-5)
    response = client.post(
        ENDPOINT,
        json={
            "title": "Deploy TaskFlow",
            "priority": 10,
        },
    )

    assert response.status_code == 422


def test_unexpected_field():  #verifies that the API returns a validation error when an unexpected field (admin) is included in the request payload
    response = client.post(
        ENDPOINT,
        json={
            "title": "Deploy TaskFlow",
            "priority": 3,
            "admin": True,
        },
    )

    assert response.status_code == 422


def test_title_whitespace_is_removed():  #verifies that the API correctly strips leading and trailing whitespace from the title field in the request payload, and returns the cleaned title in the response
    response = client.post(
        ENDPOINT,
        json={
            "title": "   Deploy TaskFlow   ",
        },
    )

    assert response.status_code == 200

    assert response.json()["task"]["title"] == (
        "Deploy TaskFlow"
    )
