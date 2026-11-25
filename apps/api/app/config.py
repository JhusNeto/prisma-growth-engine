from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    admin_api_key: str
    hotmart_hottok: str = ""
    cors_origins: str = ""
    sentry_dsn: str = ""
    sentry_environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
