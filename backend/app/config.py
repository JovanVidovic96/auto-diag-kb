from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from environment variables (and .env).

    Field names map to variables case-insensitively: arango_url <- ARANGO_URL.
    Similar to @ConfigurationProperties in Spring.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    arango_url: str = "http://localhost:8529"
    arango_root_password: str
    arango_db: str = "autodiag"

    cors_origins: str = "http://localhost:8501"
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    # lru_cache makes this a singleton: the environment is read only once.
    return Settings()
