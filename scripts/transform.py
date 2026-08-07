#!/usr/bin/env python3
"""Transformation module for PhilWeather ETL pipeline.

Cleans raw weather data, casts data types, converts unit-based durations from seconds
to hours, drops redundant features, validates weather physics constraints, and exports
cleaned records to CSV ready for PostgreSQL ingestion.
"""

from pathlib import Path
import time
import pandas as pd
from scripts.extract import extract_weather_data

# Default paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DATA_PATH = BASE_DIR / "data" / "cleaned" / "daily_weather_cleaned.csv"


def transform_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform raw weather DataFrame according to ETL business rules.

    Args:
        df: Raw weather DataFrame from extract module.

    Returns:
        pd.DataFrame: Cleaned and transformed weather DataFrame.

    Raises:
        ValueError: If data validation checks fail.
    """
    start_time = time.time()
    print("=" * 70)
    print("PHILWEATHER ETL — PHASE 4: TRANSFORMATION STAGE")
    print("=" * 70)

    transformed = df.copy()

    # 1. Date & Time Parsing
    print("1. Parsing dates and timestamps...")
    transformed["datetime"] = pd.to_datetime(transformed["datetime"]).dt.date
    transformed["sunrise"] = pd.to_datetime(transformed["sunrise"])
    transformed["sunset"] = pd.to_datetime(transformed["sunset"])

    # 2. Temporal & Integer Type Extractions
    print("2. Casting integer fields & extracting temporal features (year, month)...")
    if "weather_code" in transformed.columns:
        transformed["weather_code"] = transformed["weather_code"].astype("Int16")
    if "wind_direction_10m_dominant" in transformed.columns:
        transformed["wind_direction_10m_dominant"] = transformed["wind_direction_10m_dominant"].astype("Int16")
    transformed["year"] = pd.to_datetime(transformed["datetime"]).dt.year.astype("int16")
    transformed["month"] = pd.to_datetime(transformed["datetime"]).dt.month.astype("int8")

    # 3. Unit Conversions (seconds -> hours)
    print("3. Converting durations (seconds to hours)...")
    if "daylight_duration" in transformed.columns:
        transformed["daylight_hours"] = (transformed["daylight_duration"] / 3600.0).round(2)
    if "sunshine_duration" in transformed.columns:
        transformed["sunshine_hours"] = (transformed["sunshine_duration"] / 3600.0).round(2)

    # 4. Feature Engineering
    print("4. Computing derived metrics (temp_range, heat_index_diff)...")
    transformed["temp_range"] = (
        transformed["temperature_2m_max"] - transformed["temperature_2m_min"]
    ).round(1)

    transformed["heat_index_diff"] = (
        transformed["apparent_temperature_mean"] - transformed["temperature_2m_mean"]
    ).round(1)

    # 5. Column Cleanup
    print("5. Dropping redundant columns (snowfall_sum, raw duration fields)...")
    cols_to_drop = ["snowfall_sum", "daylight_duration", "sunshine_duration"]
    existing_drops = [c for c in cols_to_drop if c in transformed.columns]
    transformed.drop(columns=existing_drops, inplace=True)

    # 6. Data Validation
    print("6. Executing data validation rules...")
    # Rule A: Temperature hierarchy min <= mean <= max
    temp_invalid = (
        (transformed["temperature_2m_min"] > transformed["temperature_2m_mean"]) |
        (transformed["temperature_2m_mean"] > transformed["temperature_2m_max"])
    ).sum()
    if temp_invalid > 0:
        raise ValueError(f"Validation Error: {temp_invalid} rows violate temp_min <= temp_mean <= temp_max constraint.")

    # Rule B: Non-negative precipitation, wind, and radiation bounds
    non_negative_cols = [
        "precipitation_sum", "rain_sum", "precipitation_hours",
        "wind_speed_10m_max", "wind_gusts_10m_max",
        "shortwave_radiation_sum", "et0_fao_evapotranspiration",
        "daylight_hours", "sunshine_hours"
    ]
    for col in non_negative_cols:
        if col in transformed.columns:
            negative_count = (transformed[col] < 0).sum()
            if negative_count > 0:
                raise ValueError(f"Validation Error: {negative_count} negative values found in '{col}'.")

    elapsed = time.time() - start_time
    print("\n--- TRANSFORMATION SUMMARY ---")
    print(f"• Input Rows: {len(df):,} | Output Rows: {len(transformed):,}")
    print(f"• Columns: {df.shape[1]} raw -> {transformed.shape[1]} transformed")
    print(f"• Execution Time: {elapsed:.2f} seconds")
    print(f"• New Features Added: daylight_hours, sunshine_hours, temp_range, heat_index_diff, year, month")
    print(f"• Columns Dropped: {', '.join(existing_drops)}")
    print("=" * 70)

    return transformed


def export_cleaned_data(df: pd.DataFrame, output_path: Path | str = CLEANED_DATA_PATH) -> Path:
    """Export transformed DataFrame to CSV.

    Args:
        df: Cleaned DataFrame.
        output_path: Target file path.

    Returns:
        Path: Path to exported CSV.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Exporting cleaned data to: {path}...")
    df.to_csv(path, index=False)
    print(f"✓ Successfully exported {len(df):,} records ({path.stat().st_size / (1024 * 1024):.2f} MB).")
    return path


def run_pipeline() -> tuple[pd.DataFrame, Path]:
    """Execute Extract -> Transform -> Export pipeline."""
    raw_df, _ = extract_weather_data()
    cleaned_df = transform_weather_data(raw_df)
    exported_path = export_cleaned_data(cleaned_df)
    return cleaned_df, exported_path


if __name__ == "__main__":
    run_pipeline()
