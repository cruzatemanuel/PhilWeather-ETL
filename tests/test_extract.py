"""Unit tests for Phase 3 Extraction module."""

import pytest
import pandas as pd
from scripts.extract import extract_weather_data, extract_units_metadata, DEFAULT_DATA_PATH, DEFAULT_UNITS_PATH


def test_extract_units_metadata_success():
    """Verify that unit metadata is loaded into a dictionary."""
    units = extract_units_metadata(DEFAULT_UNITS_PATH)
    assert isinstance(units, dict)
    assert len(units) > 0
    assert "temperature_2m_max" in units
    assert units["temperature_2m_max"] == "°C"


def test_extract_units_metadata_missing_file(tmp_path):
    """Verify FileNotFoundError raised when units file is missing."""
    missing_file = tmp_path / "non_existent_units.csv"
    with pytest.raises(FileNotFoundError):
        extract_units_metadata(missing_file)


def test_extract_weather_data_success():
    """Verify extraction of raw weather data and attached unit metadata."""
    df, unit_map = extract_weather_data(DEFAULT_DATA_PATH, DEFAULT_UNITS_PATH)
    
    # Assert DataFrame shape and attrs
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 500324
    assert df.shape[1] == 24
    assert "city_name" in df.columns
    assert "datetime" in df.columns
    
    # Assert metadata dictionary
    assert isinstance(unit_map, dict)
    assert df.attrs.get("units") == unit_map


def test_extract_weather_data_missing_file(tmp_path):
    """Verify FileNotFoundError when dataset file does not exist."""
    missing_data = tmp_path / "missing_data.csv"
    with pytest.raises(FileNotFoundError):
        extract_weather_data(missing_data, DEFAULT_UNITS_PATH)
