#!/usr/bin/env python3
"""Extraction module for PhilWeather ETL pipeline.

Loads raw historical daily weather CSV data and unit metadata CSV,
attaches unit mapping metadata to the DataFrame, validates file integrity,
and logs extraction diagnostics.
"""

from pathlib import Path
import time
import pandas as pd

# Default file paths
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "raw" / "daily_data_combined_2010_to_2019.csv"
DEFAULT_UNITS_PATH = BASE_DIR / "data" / "raw" / "daily_units_2010_to_2019.csv"


def extract_units_metadata(units_path: Path | str = DEFAULT_UNITS_PATH) -> dict[str, str]:
    """Load and parse unit metadata from CSV into a dictionary.

    Args:
        units_path: Path to daily_units_2010_to_2019.csv.

    Returns:
        dict[str, str]: Mapping of column name to its unit of measurement.

    Raises:
        FileNotFoundError: If the units CSV file does not exist.
        ValueError: If the units CSV file is empty or corrupted.
    """
    path = Path(units_path)
    if not path.exists():
        raise FileNotFoundError(f"Unit metadata file not found at: {path}")

    try:
        units_df = pd.read_csv(path)
        if units_df.empty:
            raise ValueError(f"Unit metadata file at {path} is empty.")
        
        # Convert first row of units to dictionary mapping
        unit_map = units_df.to_dict(orient="records")[0]
        return unit_map
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Failed to parse unit metadata from {path}: {e}") from e


def extract_weather_data(
    data_path: Path | str = DEFAULT_DATA_PATH,
    units_path: Path | str = DEFAULT_UNITS_PATH
) -> tuple[pd.DataFrame, dict[str, str]]:
    """Extract raw weather records and attach unit metadata.

    Args:
        data_path: Path to daily_data_combined_2010_to_2019.csv.
        units_path: Path to daily_units_2010_to_2019.csv.

    Returns:
        tuple[pd.DataFrame, dict[str, str]]:
            - Raw weather DataFrame with unit metadata attached to `df.attrs['units']`.
            - Unit metadata dictionary.

    Raises:
        FileNotFoundError: If either raw data file or units file is missing.
        ValueError: If data is empty or invalid.
    """
    start_time = time.time()
    data_file = Path(data_path)

    print("=" * 70)
    print("PHILWEATHER ETL — PHASE 3: EXTRACTION STAGE")
    print("=" * 70)

    # 1. Load Unit Metadata
    print(f"Reading unit metadata from: {units_path}")
    unit_map = extract_units_metadata(units_path)
    print(f"✓ Parsed unit metadata for {len(unit_map)} columns.")

    # 2. Read Raw Dataset
    if not data_file.exists():
        raise FileNotFoundError(f"Raw weather dataset file not found at: {data_file}")

    print(f"Reading raw weather dataset from: {data_file}...")
    df = pd.read_csv(data_file)

    if df.empty:
        raise ValueError(f"Raw weather dataset at {data_file} is empty.")

    # 3. Attach metadata to DataFrame attrs
    df.attrs["units"] = unit_map
    elapsed_time = time.time() - start_time

    # 4. Log Diagnostics
    print("\n--- EXTRACTION METRICS & DIAGNOSTICS ---")
    print(f"• Total Rows Extracted: {len(df):,}")
    print(f"• Total Columns: {df.shape[1]}")
    print(f"• Execution Time: {elapsed_time:.2f} seconds")
    print(f"• Unique Cities: {df['city_name'].nunique()}")
    print(f"• Date Range: {df['datetime'].min()} to {df['datetime'].max()}")
    print(f"• Memory Usage: {df.memory_usage(deep=True).sum() / (1024 * 1024):.2f} MB")
    print("=" * 70)

    return df, unit_map


if __name__ == "__main__":
    extract_weather_data()
