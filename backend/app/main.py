from fastapi import FastAPI

from app.api.router import api_router    #registering the API router
from app.core.config import settings      #registering the application settings
from app.schemas.health import HealthResponse   #registering the health response schema
from app.api.v1.health import health_check   #registering the health check endpoint

from fastapi.exceptions import RequestValidationError    #registering the request validation error exception
from starlette.exceptions import HTTPException as StarletteHTTPException   #registering the HTTP exception from Starlette

from app.core.errors import AppError  #registering the custom application error exception
from app.core.exception_handlers import (
    app_error_handler,
    http_error_handler,
    validation_error_handler,
    internal_server_error_handler       #registering the internal server error handler for unhandled exceptions
)                                       #registering the custom exception handlers for application errors, HTTP errors, and validation errors

from app.core.logging_config import setup_logging  #registering the logging configuration

from app.core.request_logging import (
    request_logging_middleware,
)                                                  #registering the request logging middleware

def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        description=(
            "TaskFlow project and task management API"
        ),
    )

    # Configure structured application logging.
    setup_logging()

    # Register request logging middleware.
    application.middleware("http")(
        request_logging_middleware
    )

    application.add_exception_handler(
        AppError,
        app_error_handler,
    )

    application.add_exception_handler(
        StarletteHTTPException,
        http_error_handler,
    )

    application.add_exception_handler(
        RequestValidationError,
        validation_error_handler,
    )

    application.add_exception_handler(
        Exception,
        internal_server_error_handler,
    )

    application.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
    )

    @application.get("/")
    async def root():
        return {
            "application": "TaskFlow",
            "message": "Welcome to TaskFlow API",
            "version": settings.app_version,
        }

    # Compatibility endpoint for the existing
    # Docker Compose health check.
    @application.get(
        "/health",
        response_model=HealthResponse,
        include_in_schema=False,
    )
    async def legacy_health():
        return await health_check()

    return application


app = create_app()