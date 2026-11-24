from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    app_version: str = "0.1.0"

    app_env: Literal[
        "development",
        "testing",
        "production"
    ] = "development"

    debug: bool = False

    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
