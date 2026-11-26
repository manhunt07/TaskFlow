from unittest.mock import patch  #provides a way to replace parts of your system under test and make assertions about how they have been used
from uuid import UUID  #provides a way to create and manipulate UUIDs

from fastapi.testclient import TestClient  #provides a way to test FastAPI applications by simulating HTTP requests

from app.main import app #provides access to the FastAPI application instance defined in the main module


client = TestClient(app)  #provides a test client for the FastAPI application, allowing you to send HTTP requests and receive responses in a test environment


def test_response_contains_request_id():  #verifies that the response from the health check endpoint contains a valid request ID in the headers
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    request_id = response.headers.get(
        "X-Request-ID"
    )

    assert request_id is not None

    # Verify it is a valid UUID.
    UUID(request_id)


def test_missing_project_is_logged(): #verifies that when a request is made for a non-existent project, the request logging middleware logs the request with the appropriate details, including the request ID and status code
    with patch(
        "app.core.request_logging.logger.info"
    ) as mock_log:

        response = client.get(
            "/api/v1/examples/projects/999"
        )

    assert response.status_code == 404

    assert "X-Request-ID" in response.headers

    mock_log.assert_called_once()

    args, kwargs = mock_log.call_args

    assert args[0] == "http_request_completed"

    assert kwargs["extra"]["status_code"] == 404

    assert (
        kwargs["extra"]["request_id"]
        == response.headers["X-Request-ID"]
    )
