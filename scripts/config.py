"""
PhilWeather ETL — Configuration Layer

Provides type-safe configuration management using Pydantic Settings v2.
Loads settings from environment variables and optional .env file.
"""

from functools import lru_cache
from typing import Annotated, List, Union

from pydantic import Field, field_validator
from pydantic.functional_validators import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cities_list(v: Union[str, List[str]]) -> List[str]:
    """Parse a comma-separated string or JSON array into a list of city strings."""
    if isinstance(v, str):
        v = v.strip()
        # Try JSON first (for ["a","b"] format)
        if v.startswith("[") and v.endswith("]"):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                pass
        # Fall back to comma-separated
        return [city.strip() for city in v.split(",") if city.strip()]
    return v


CitiesList = Annotated[List[str], BeforeValidator(parse_cities_list)]


class Settings(BaseSettings):
    """Type-safe application configuration loaded from environment or .env file."""

    # OpenWeather API Configuration
    openweather_api_key: str = Field(
        default="",
        description="OpenWeather API Key",
    )
    openweather_base_url: str = Field(
        default="https://api.openweathermap.org/data/2.5",
        description="Base URL for OpenWeather API endpoints",
    )

    # Supabase PostgreSQL Database Credentials
    supabase_db_host: str = Field(
        default="localhost",
        description="PostgreSQL Database Host",
    )
    supabase_db_port: int = Field(
        default=5432,
        description="PostgreSQL Database Port",
    )
    supabase_db_name: str = Field(
        default="postgres",
        description="PostgreSQL Database Name",
    )
    supabase_db_user: str = Field(
        default="postgres",
        description="PostgreSQL Database User",
    )
    supabase_db_password: str = Field(
        default="",
        description="PostgreSQL Database Password",
    )

    # Pipeline Settings
    cities_list: CitiesList = Field(
        default_factory=lambda: [
            "Manila",
            "Cebu",
            "Davao",
            "Baguio",
            "Iloilo",
            "Cagayan de Oro",
        ],
        description="Target Philippine cities for weather extraction (JSON array or comma-separated)",
    )
    log_level: str = Field(
        default="INFO",
        description="Global logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection string URL."""
        return (
            f"postgresql://{self.supabase_db_user}:{self.supabase_db_password}"
            f"@{self.supabase_db_host}:{self.supabase_db_port}/{self.supabase_db_name}"
        )


@lru_cache()
def get_settings() -> Settings:
    """Retrieve singleton cached application settings instance.

    Returns:
        Settings: Configured Settings instance.
    """
    return Settings()
