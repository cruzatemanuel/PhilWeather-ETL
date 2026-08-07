"""Unit tests for Phase 6 SQL Analysis module."""

# pyrefly: ignore [missing-import]
import pytest
from scripts.database import get_engine
from scripts.analyze import run_all_analysis, run_sql_file, SQL_DIR, SQL_FILES


@pytest.fixture
def engine():
    """Fixture returning database engine."""
    return get_engine()


def test_sql_files_exist():
    """Verify all 5 SQL files exist in sql/ directory."""
    for sql_file in SQL_FILES:
        path = SQL_DIR / sql_file
        assert path.exists(), f"Missing SQL file: {path}"


def test_sql_analysis_execution(engine):
    """Verify all 5 SQL scripts execute against PostgreSQL and return non-empty DataFrames."""
    results = run_all_analysis(engine)
    
    assert len(results) == 5
    for filename, df in results.items():
        assert not df.empty, f"SQL Query {filename} returned empty result set!"
        assert df.shape[0] > 0
