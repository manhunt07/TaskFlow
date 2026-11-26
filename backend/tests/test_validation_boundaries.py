import pytest

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)                      #this is for testing the FastAPI application by simulating HTTP requests and responses

ENDPOINT = "/api/v1/examples/validate-task"


@pytest.mark.parametrize(                #verifies that the API returns a validation error when the priority field is outside the allowed range (1-5) or is of an invalid type
    "priority",
    [0, 6, -1, 100, "3", True, None],
)
def test_invalid_priority_values(priority):

    response = client.post(
        ENDPOINT,
        json={
            "title": "Deploy TaskFlow",
            "priority": priority,
        },
    )

    assert response.status_code == 422

    assert response.json()["error"]["code"] == (
        "VALIDATION_ERROR"
    )


@pytest.mark.parametrize(                    #verifies that the API accepts valid priority values at the boundaries of the allowed range (1 and 5)
    "priority",
    [1, 5],
)
def test_valid_priority_boundaries(priority):

    response = client.post(
        ENDPOINT,
        json={
            "title": "Deploy TaskFlow",
            "priority": priority,
        },
    )

    assert response.status_code == 200

    assert response.json()["task"]["priority"] == priority


def test_whitespace_only_title():

    response = client.post(
        ENDPOINT,
        json={
            "title": "     ",
            "priority": 3,
        },
    )

    assert response.status_code == 422


def test_title_exceeds_maximum_length():

    response = client.post(
        ENDPOINT,
        json={
            "title": "A" * 101,
            "priority": 3,
        },
    )

    assert response.status_code == 422


def test_description_exceeds_maximum_length():

    response = client.post(
        ENDPOINT,
        json={
            "title": "Deploy TaskFlow",
            "description": "A" * 501,
            "priority": 3,
        },
    )

    assert response.status_code == 422
