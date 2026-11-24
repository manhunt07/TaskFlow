from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.schemas.health import HealthResponse
from app.api.v1.health import health_check


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        description=(
            "TaskFlow project and task management API"
        ),
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