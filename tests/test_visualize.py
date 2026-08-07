"""Unit tests for Phase 7 Data Visualization module."""

# pyrefly: ignore [missing-import]
import pytest
from scripts.database import get_engine
from scripts.visualize import generate_all_visualizations, CHARTS_DIR


@pytest.fixture
def engine():
    """Fixture returning database engine."""
    return get_engine()


def test_generate_all_visualizations(engine, tmp_path):
    """Verify that all 4 PNG charts are created and non-empty."""
    chart_paths = generate_all_visualizations(engine)
    
    assert len(chart_paths) == 4
    for path in chart_paths:
        assert path.exists(), f"Chart file missing: {path}"
        assert path.stat().st_size > 0, f"Chart file is empty: {path}"
