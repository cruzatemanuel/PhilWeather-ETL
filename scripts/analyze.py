#!/usr/bin/env python3
"""SQL Analysis runner module for PhilWeather ETL pipeline.

Executes all 5 analytical SQL query scripts against PostgreSQL daily_weather table
and prints formatted meteorological insights.
"""

from pathlib import Path
import time
from sqlalchemy import text
from sqlalchemy.engine import Engine
import pandas as pd
from scripts.database import get_engine

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"

SQL_FILES = [
    "01_hottest_cities.sql",
    "02_rainiest_cities.sql",
    "03_monthly_climate_profile.sql",
    "04_extreme_weather_events.sql",
    "05_city_rainfall_ranking_window.sql"
]


def run_sql_file(sql_file_path: Path | str, engine: Engine) -> pd.DataFrame:
    """Execute a single SQL file against PostgreSQL engine and return DataFrame.

    Args:
        sql_file_path: Path to .sql file.
        engine: SQLAlchemy Engine.

    Returns:
        pd.DataFrame: Query result dataset.
    """
    path = Path(sql_file_path)
    if not path.exists():
        raise FileNotFoundError(f"SQL script not found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        query = f.read()

    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn)

    return df


def run_all_analysis(engine: Engine | None = None) -> dict[str, pd.DataFrame]:
    """Execute all 5 analytical SQL queries and print formatted reports.

    Args:
        engine: SQLAlchemy Engine. If None, loaded from get_engine().

    Returns:
        dict[str, pd.DataFrame]: Mapping of script name to query results.
    """
    start_time = time.time()
    if engine is None:
        engine = get_engine()

    results = {}

    print("=" * 70)
    print("PHILWEATHER ETL — PHASE 6: SQL ANALYTICS STAGE")
    print("=" * 70)

    for sql_filename in SQL_FILES:
        file_path = SQL_DIR / sql_filename
        print(f"\n▶ EXECUTING: {sql_filename}")
        df = run_sql_file(file_path, engine)
        results[sql_filename] = df
        
        # Display preview table
        print(df.to_string(index=False))
        print("-" * 70)

    elapsed = time.time() - start_time
    print(f"\n✓ Successfully executed all 5 SQL analytical scripts in {elapsed:.2f} seconds!")
    print("=" * 70)

    return results


if __name__ == "__main__":
    run_all_analysis()
