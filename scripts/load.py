#!/usr/bin/env python3
"""Database loading module for PhilWeather ETL pipeline.

Creates PostgreSQL database schema DDL, indexes, and loads cleaned 500,000+ daily
weather records in ultra-fast batch mode using psycopg2 execute_values / COPY.
"""

import io
from pathlib import Path
import time
from sqlalchemy import text
from sqlalchemy.engine import Engine
import pandas as pd
from scripts.database import get_engine
from scripts.transform import CLEANED_DATA_PATH

# DDL for daily_weather table schema
CREATE_TABLE_DDL = """
CREATE TABLE IF NOT EXISTS daily_weather (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(8,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    datetime DATE NOT NULL,
    weather_code SMALLINT,
    temperature_2m_max DECIMAL(4,1),
    temperature_2m_min DECIMAL(4,1),
    temperature_2m_mean DECIMAL(4,1),
    apparent_temperature_max DECIMAL(4,1),
    apparent_temperature_min DECIMAL(4,1),
    apparent_temperature_mean DECIMAL(4,1),
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    daylight_hours DECIMAL(4,2),
    sunshine_hours DECIMAL(4,2),
    precipitation_sum DECIMAL(6,2),
    rain_sum DECIMAL(6,2),
    precipitation_hours DECIMAL(4,1),
    wind_speed_10m_max DECIMAL(5,1),
    wind_gusts_10m_max DECIMAL(5,1),
    wind_direction_10m_dominant SMALLINT,
    shortwave_radiation_sum DECIMAL(6,2),
    et0_fao_evapotranspiration DECIMAL(5,2),
    temp_range DECIMAL(4,1),
    heat_index_diff DECIMAL(4,1),
    year SMALLINT,
    month SMALLINT,
    CONSTRAINT unique_city_date UNIQUE (city_name, datetime)
);
"""

# DDL for database indexes
CREATE_INDEXES_DDL = """
CREATE INDEX IF NOT EXISTS idx_weather_city ON daily_weather(city_name);
CREATE INDEX IF NOT EXISTS idx_weather_datetime ON daily_weather(datetime);
CREATE INDEX IF NOT EXISTS idx_weather_city_date ON daily_weather(city_name, datetime);
CREATE INDEX IF NOT EXISTS idx_weather_year_month ON daily_weather(year, month);
"""


def setup_schema(engine: Engine) -> None:
    """Create table DDL and indexes if they do not exist.

    Args:
        engine: SQLAlchemy database engine.
    """
    print("1. Creating table schema and constraints...")
    with engine.begin() as conn:
        conn.execute(text(CREATE_TABLE_DDL))
    print("✓ Table 'daily_weather' verified/created.")


def setup_indexes(engine: Engine) -> None:
    """Create optimization indexes for analytical queries.

    Args:
        engine: SQLAlchemy database engine.
    """
    print("3. Creating optimization indexes...")
    with engine.begin() as conn:
        conn.execute(text(CREATE_INDEXES_DDL))
    print("✓ Optimization indexes verified/created.")


def fast_copy_dataframe(df: pd.DataFrame, engine: Engine, table_name: str = "daily_weather") -> None:
    """Perform ultra-fast COPY IN stream loading from DataFrame buffer into PostgreSQL.

    Args:
        df: Dataframe to load.
        engine: SQLAlchemy Engine.
        table_name: Destination table name.
    """
    raw_conn = engine.raw_connection()
    try:
        with raw_conn.cursor() as cur:
            buffer = io.StringIO()
            # Save to CSV in-memory buffer without header or index
            df.to_csv(buffer, index=False, header=False)
            buffer.seek(0)
            
            columns_str = ", ".join([f'"{col}"' for col in df.columns])
            copy_sql = f"COPY {table_name} ({columns_str}) FROM STDIN WITH (FORMAT csv, NULL '')"
            cur.copy_expert(copy_sql, buffer)
        raw_conn.commit()
    finally:
        raw_conn.close()


def load_weather_data(
    cleaned_data_path: Path | str = CLEANED_DATA_PATH,
    engine: Engine | None = None
) -> int:
    """Load cleaned weather data CSV into PostgreSQL database.

    Args:
        cleaned_data_path: Path to daily_weather_cleaned.csv.
        engine: SQLAlchemy Engine. If None, retrieves from get_engine().

    Returns:
        int: Total row count verified in database.
    """
    start_time = time.time()
    path = Path(cleaned_data_path)

    print("=" * 70)
    print("PHILWEATHER ETL — PHASE 5: DATABASE LOADING STAGE")
    print("=" * 70)

    if not path.exists():
        raise FileNotFoundError(f"Cleaned dataset file not found at: {path}")

    if engine is None:
        engine = get_engine()

    # 1. Setup DDL Table Schema
    setup_schema(engine)

    # 2. Read Cleaned Data
    print(f"Reading cleaned dataset from: {path}...")
    df = pd.read_csv(path)
    expected_rows = len(df)
    print(f"Loaded {expected_rows:,} records into DataFrame.")

    # 3. Truncate table if data already exists to allow idempotent re-runs
    print("2. Ingesting records into PostgreSQL via high-performance COPY buffer...")
    with engine.begin() as conn:
        current_count = conn.execute(text("SELECT COUNT(*) FROM daily_weather")).scalar()
        if current_count > 0:
            print(f"  Existing records found ({current_count:,}). Truncating table for clean reload...")
            conn.execute(text("TRUNCATE TABLE daily_weather RESTART IDENTITY"))

    # 4. Ultra-Fast COPY Insertion
    fast_copy_dataframe(df, engine, "daily_weather")

    # 5. Create Optimization Indexes
    setup_indexes(engine)

    # 6. Verify Database Row Count
    with engine.connect() as conn:
        db_count = conn.execute(text("SELECT COUNT(*) FROM daily_weather")).scalar()

    elapsed = time.time() - start_time

    print("\n--- LOADING SUMMARY & VERIFICATION ---")
    print(f"• Expected Records: {expected_rows:,}")
    print(f"• Ingested Database Records: {db_count:,}")
    print(f"• Ingestion Strategy: PostgreSQL COPY FROM STDIN")
    print(f"• Total Loading Runtime: {elapsed:.2f} seconds")

    if db_count == expected_rows:
        print("✓ SUCCESS: Database row count perfectly matches transformed dataset!")
    else:
        raise ValueError(f"Mismatch Error: DB count ({db_count}) != Expected count ({expected_rows}).")

    print("=" * 70)
    return db_count


if __name__ == "__main__":
    load_weather_data()
