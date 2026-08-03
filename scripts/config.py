"""Centralized, validated application configuration.

Every script — and later, every Airflow task — should import
`get_settings()` rather than reading `os.environ` directly. That keeps
validation, defaults, and type coercion in one place instead of
scattered across the codebase.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- OpenWeather ---
    openweather_api_key: str
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    openweather_units: str = "metric"  # metric = Celsius; avoids raw Kelvin output

    # --- Database (Supabase Postgres, via Session Pooler) ---
    database_url: str

    # --- Pipeline behavior ---
    cities: list[str] = ["Manila", "Batangas City", "Cebu City", "Davao City"]
    request_timeout_seconds: int = 10
    max_retries: int = 3

    # --- Paths ---
    raw_json_dir: Path = Path("data/raw_json")
    log_dir: Path = Path("data/logs")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Cached so Settings() — which reads and validates the environment —
    only runs once per process, while staying easy to reset in tests via
    get_settings.cache_clear().
    """
    return Settings()