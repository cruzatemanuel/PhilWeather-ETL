"""
PhilWeather ETL — Environment & Connectivity Health Check

Standalone script to verify:
1. Configuration loading and required secret presence.
2. OpenWeather API connectivity and key validity.
3. Supabase PostgreSQL database connectivity via psycopg2.

Usage:
    python scripts/health_check.py
"""

import sys
import time
from pathlib import Path
from typing import Dict, Tuple

# Ensure project root is in sys.path when script is executed directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import psycopg2
import requests

from scripts.config import get_settings
from scripts.utils import get_logger

logger = get_logger("health_check")


def check_openweather() -> Tuple[bool, str, float]:
    """Test connectivity to OpenWeather API using configured key and base URL.

    Returns:
        Tuple[bool, str, float]: (Success flag, Message/Details, Latency in ms)
    """
    settings = get_settings()

    if not settings.openweather_api_key or settings.openweather_api_key == "your_openweather_api_key_here":
        return False, "Missing OPENWEATHER_API_KEY in environment or .env", 0.0

    test_city = settings.cities_list[0] if settings.cities_list else "Manila"
    url = f"{settings.openweather_base_url}/weather"
    params = {
        "q": f"{test_city},PH",
        "appid": settings.openweather_api_key,
        "units": "metric",
    }

    start_time = time.time()
    try:
        response = requests.get(url, params=params, timeout=10)
        latency_ms = (time.time() - start_time) * 1000

        if response.status_code == 200:
            data = response.json()
            temp = data.get("main", {}).get("temp", "N/A")
            desc = data.get("weather", [{}])[0].get("description", "N/A")
            msg = f"Connected OK (City: {test_city}, Temp: {temp}°C, Condition: {desc})"
            return True, msg, latency_ms
        elif response.status_code == 401:
            return False, "HTTP 401 Unauthorized: Invalid OpenWeather API key", latency_ms
        else:
            return (
                False,
                f"HTTP {response.status_code}: {response.text}",
                latency_ms,
            )
    except requests.exceptions.RequestException as exc:
        latency_ms = (time.time() - start_time) * 1000
        return False, f"Network error connecting to OpenWeather: {str(exc)}", latency_ms


def check_postgres() -> Tuple[bool, str, float]:
    """Test connectivity to Supabase PostgreSQL database via psycopg2.

    Returns:
        Tuple[bool, str, float]: (Success flag, Message/Details, Latency in ms)
    """
    settings = get_settings()

    if not settings.supabase_db_password or settings.supabase_db_password == "your_supabase_db_password_here":
        return False, "Missing SUPABASE_DB_PASSWORD in environment or .env", 0.0

    start_time = time.time()
    try:
        conn = psycopg2.connect(
            host=settings.supabase_db_host,
            port=settings.supabase_db_port,
            dbname=settings.supabase_db_name,
            user=settings.supabase_db_user,
            password=settings.supabase_db_password,
            connect_timeout=5,
        )
        latency_ms = (time.time() - start_time) * 1000

        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            db_version = cur.fetchone()[0]
            short_version = db_version.split(",")[0] if db_version else "PostgreSQL"

        conn.close()
        return True, f"Connected OK ({short_version})", latency_ms
    except psycopg2.OperationalError as err:
        latency_ms = (time.time() - start_time) * 1000
        return False, f"OperationalError: {str(err).strip()}", latency_ms
    except Exception as err:
        latency_ms = (time.time() - start_time) * 1000
        return False, f"Database Connection Error: {str(err).strip()}", latency_ms


def main() -> None:
    """Run all health check diagnostics and output a summary report."""
    print("\n" + "=" * 70)
    print(" 🇵🇭 PhilWeather ETL — System Environment & Health Diagnostic")
    print("=" * 70)

    settings = get_settings()
    logger.info("Loaded configuration for environment check.")
    print(f"Target Cities: {', '.join(settings.cities_list)}")
    print(f"Database Host: {settings.supabase_db_host}:{settings.supabase_db_port}/{settings.supabase_db_name}")
    print("-" * 70)

    results: Dict[str, Tuple[bool, str, float]] = {}

    # Check 1: OpenWeather API
    print("--> Checking OpenWeather API connectivity...")
    ow_success, ow_msg, ow_latency = check_openweather()
    results["OpenWeather API"] = (ow_success, ow_msg, ow_latency)

    # Check 2: Supabase PostgreSQL
    print("--> Checking Supabase PostgreSQL database connectivity...")
    db_success, db_msg, db_latency = check_postgres()
    results["Supabase PostgreSQL"] = (db_success, db_msg, db_latency)

    # Summary Report
    print("\n" + "=" * 70)
    print(" HEALTH DIAGNOSTIC SUMMARY")
    print("=" * 70)

    all_passed = True
    for service, (passed, msg, latency) in results.items():
        status_symbol = "✅ PASS" if passed else "❌ FAIL"
        latency_str = f"{latency:.1f} ms" if latency > 0 else "N/A"
        print(f"[{status_symbol}] {service:<22} (Latency: {latency_str})")
        print(f"        Details: {msg}")
        if not passed:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print(" SUCCESS: All services are healthy and fully reachable!")
        print("=" * 70 + "\n")
        sys.exit(0)
    else:
        print(" WARNING: One or more service checks failed.")
        print(" Please update your local .env file with valid credentials.")
        print("=" * 70 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
