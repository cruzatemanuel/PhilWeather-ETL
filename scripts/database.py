"""Database connection utilities for PhilWeather ETL."""

import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = [
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
]


def get_engine() -> Engine:
    """
    Create and return a SQLAlchemy Engine for PostgreSQL.

    Loads configuration from environment variables and validates
    that all required variables are present.

    Returns:
        Engine: Configured SQLAlchemy engine with connection pooling.

    Raises:
        ValueError: If any required environment variable is missing.
    """
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Please check your .env file."
        )

    url = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    # pool_pre_ping=True enables connection health checks before use
    return create_engine(url, pool_pre_ping=True)


if __name__ == "__main__":
    # Quick syntax validation when run directly
    try:
        engine = get_engine()
        # Don't print the password - use hide_password for safety
        print(f"Engine created successfully: {engine.url.render_as_string(hide_password=True)}")
    except ValueError as e:
        print(f"Configuration error: {e}")