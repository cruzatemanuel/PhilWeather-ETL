"""Unit tests for Phase 4 Transformation module."""

# pyrefly: ignore [missing-import]
import pytest
import pandas as pd
from scripts.extract import extract_weather_data, DEFAULT_DATA_PATH, DEFAULT_UNITS_PATH
from scripts.transform import transform_weather_data, export_cleaned_data


@pytest.fixture
def raw_df():
    """Fixture returning raw weather DataFrame."""
    df, _ = extract_weather_data(DEFAULT_DATA_PATH, DEFAULT_UNITS_PATH)
    return df


def test_transform_weather_data_features(raw_df):
    """Test feature engineering and unit conversions in transform_weather_data."""
    transformed = transform_weather_data(raw_df)
    
    # Assert row count preserved
    assert len(transformed) == 500324
    
    # Assert new columns added
    expected_new_cols = [
        "daylight_hours", "sunshine_hours",
        "temp_range", "heat_index_diff", "year", "month"
    ]
    for col in expected_new_cols:
        assert col in transformed.columns
        
    # Assert dropped columns
    dropped_cols = ["snowfall_sum", "daylight_duration", "sunshine_duration"]
    for col in dropped_cols:
        assert col not in transformed.columns


def test_transform_weather_data_validation(raw_df):
    """Test validation constraints on temperature hierarchy."""
    invalid_df = raw_df.copy()
    # Introduce intentional temp hierarchy violation
    invalid_df.loc[0, "temperature_2m_min"] = 40.0
    invalid_df.loc[0, "temperature_2m_mean"] = 25.0

    with pytest.raises(ValueError, match="temp_min <= temp_mean <= temp_max"):
        transform_weather_data(invalid_df)


def test_export_cleaned_data(raw_df, tmp_path):
    """Test exporting cleaned DataFrame to CSV."""
    transformed = transform_weather_data(raw_df)
    out_file = tmp_path / "cleaned_test.csv"
    
    exported = export_cleaned_data(transformed, out_file)
    assert exported.exists()
    assert exported.stat().st_size > 0
