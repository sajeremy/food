from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    database_url: str | None = Field(default=None, description="Database connection URL")
    google_api_key: str | None = Field(default=None, description="Google API key for various Google services")
    log_level: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")

    model_config = {
        "env_file": ".env.local",
        "env_file_encoding": "utf-8",
    }


# Create a global settings instance
settings = Settings()
