import logging
import time
import uuid

from fastapi import Request


logger = logging.getLogger("taskflow.requests")


async def request_logging_middleware(
    request: Request,
    call_next,
):
    # Generate a unique ID for this request.
    request_id = uuid.uuid4().hex

    # Make it available to the application.
    request.state.request_id = request_id

    # Record the starting time.
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

    except Exception as exc:
        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        logger.error(
            "http_request_failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": "unhandled",
                "status_code": 500,
                "duration_ms": duration_ms,
                "exception_type": type(exc).__name__,
            },
        )

        # Preserve normal exception handling.
        raise

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2,
    )

    # Read the matched route template where available.
    route = request.scope.get("route")

    safe_path = (
        getattr(route, "path", None)
        if route is not None
        else None
    ) or "unmatched"

    # Return the request ID to the client.
    response.headers["X-Request-ID"] = request_id

    log_fields = {
        "request_id": request_id,
        "method": request.method,
        "path": safe_path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
    }

    log_method = (
        logger.error
        if response.status_code >= 500
        else logger.info
    )

    log_method(
        "http_request_completed",
        extra=log_fields,
    )

    return response
