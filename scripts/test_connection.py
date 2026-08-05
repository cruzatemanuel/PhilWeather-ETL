#!/usr/bin/env python3
"""Test PostgreSQL database connection for PhilWeather ETL."""

import sys
from sqlalchemy import text
from scripts.database import get_engine


def test_connection() -> bool:
    """
    Test the database connection by executing SELECT 1.

    Returns:
        bool: True if connection successful, False otherwise.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row and row[0] == 1:
                print("✓ Successfully connected to PostgreSQL database: philweather_db")
                return True
            else:
                print("✗ Connection test failed: unexpected result from SELECT 1")
                return False
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("  Ensure .env file exists and contains all required PostgreSQL variables.")
        return False
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("  Ensure PostgreSQL is running and .env is configured correctly.")
        print("  Run: createdb philweather_db (if database doesn't exist)")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)