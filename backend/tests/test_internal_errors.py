from uuid import UUID

from fastapi.testclient import TestClient

from app.main import create_app

from unittest.mock import patch         #for mocking objects and functions during testing


def test_unexpected_error_returns_safe_response():

    # Create a separate application for testing.
    app = create_app()

    # This endpoint exists only in this test.
    @app.get("/test-internal-error")
    async def simulate_error():
        raise RuntimeError(
            "Sensitive internal diagnostic information"
        )

    # Allow the client to inspect HTTP 500 responses.
    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get("/test-internal-error")

    # Verify the HTTP status.
    assert response.status_code == 500

    # Verify our standardized error response.
    assert response.json() == {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
        }
    }

    # Verify sensitive details were not exposed.
    assert (
        "Sensitive internal diagnostic information"
        not in response.text
    )

    # Verify the response contains a request ID.
    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None

    # Confirm the identifier is a valid UUID.
    UUID(request_id)

def test_internal_error_request_id_matches_log():         #verifies that the request ID returned in the response headers matches the request ID logged in the server logs for an internal server error, ensuring proper correlation of logs and easier debugging of server errors

    app = create_app()

    @app.get("/test-correlation-error")
    async def simulate_error():
        raise RuntimeError("Simulated internal failure")

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    with patch(
        "app.core.request_logging.logger.error"
    ) as mock_log:

        response = client.get(
            "/test-correlation-error"
        )

    assert response.status_code == 500

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None

    mock_log.assert_called_once()

    args, kwargs = mock_log.call_args

    assert args[0] == "http_request_failed"

    assert kwargs["extra"]["request_id"] == request_id

    assert kwargs["extra"]["status_code"] == 500

    assert kwargs["extra"]["exception_type"] == "RuntimeError"