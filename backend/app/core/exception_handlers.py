from fastapi import Request     #validation error raised by FastAPI when the request payload does not conform to the expected schema, allowing for custom error handling and response formatting
from fastapi.exceptions import RequestValidationError  #validation error raised by FastAPI when the request payload does not conform to the expected schema, allowing for custom error handling and response formatting
from fastapi.responses import JSONResponse  #visualizes the response as a JSON object, allowing for structured error messages to be returned to the client in a standardized format
from starlette.exceptions import HTTPException as StarletteHTTPException  #for handling HTTP exceptions raised by the FastAPI application, allowing for custom error responses to be returned to the client

from app.core.errors import AppError


async def app_error_handler(
    request: Request,
    exc: AppError,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


async def http_error_handler(
    request: Request,
    exc: StarletteHTTPException,
):                                                #used to handle HTTP exceptions raised by the FastAPI application, returning a standardized JSON response with an error code and message based on the HTTP status code of the exception
    codes = {
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        429: "RATE_LIMITED",
    }                                             #used to map HTTP status codes to corresponding error codes for the JSON response, providing a standardized way to represent different types of HTTP errors in the API responses

    code = codes.get(
        exc.status_code,
        "HTTP_ERROR",
    )

    message = (
        exc.detail
        if isinstance(exc.detail, str)
        else "HTTP request failed"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": message,
            }
        },
        headers=exc.headers,
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
            }
        },
    )

async def internal_server_error_handler(
    request: Request,
    exc: Exception,
):                                                  #validation error handler for unexpected server errors, returning a standardized JSON response with an error code and message without exposing sensitive information
    """
    Return a safe response for unexpected server errors.

    Do not expose exception messages or stack traces.
    """

    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    headers = {}

    if request_id:
        headers["X-Request-ID"] = request_id

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            }
        },
        headers=headers,
    )