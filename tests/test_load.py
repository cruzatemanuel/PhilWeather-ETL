"""Unit tests for Phase 5 Database Loading module."""

# pyrefly: ignore [missing-import]
import pytest
from sqlalchemy import text
from scripts.database import get_engine
from scripts.load import load_weather_data, setup_schema, setup_indexes


@pytest.fixture
def engine():
    """Fixture returning database engine."""
    return get_engine()


def test_database_connection(engine):
    """Test connection to PostgreSQL database."""
    with engine.connect() as conn:
        res = conn.execute(text("SELECT 1")).scalar()
        assert res == 1


def test_load_weather_data_row_count(engine):
    """Verify that database record count matches expected 500,324 rows."""
    db_count = load_weather_data(engine=engine)
    assert db_count == 500324


def test_database_indexes_exist(engine):
    """Verify that optimization indexes exist on daily_weather table."""
    setup_indexes(engine)
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT indexname FROM pg_indexes
            WHERE tablename = 'daily_weather';
        """)).fetchall()
        index_names = [r[0] for r in result]
        
        assert "idx_weather_city" in index_names
        assert "idx_weather_datetime" in index_names
        assert "idx_weather_city_date" in index_names
        assert "idx_weather_year_month" in index_names
