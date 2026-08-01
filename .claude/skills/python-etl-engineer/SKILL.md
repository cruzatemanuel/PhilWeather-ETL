---
name: python-etl-engineer
description: Guides development of robust, maintainable Python ETL pipelines for weather data using Supabase, Airflow, and dbt.
---

# Purpose
Provide a reusable framework and best‑practice guidance for building Python ETL jobs that extract, transform, and load weather observations into PostgreSQL/Supabase.

# When to Use
- Writing custom ingestion scripts for API or CSV sources.
- Implementing data validation before persisting to the database.
- Integrating with Airflow operators for scheduled runs.
- Refactoring legacy scripts into a modular package.

# Responsibilities
- Structure code as a clean package (`src/etl/`).
- Use type‑hints, `pydantic` models, and `loguru` for logging.
- Manage connections via `supabase-py` and `psycopg2-binary`.
- Write unit tests with `pytest` and fixtures.
- Ensure idempotent loads (upserts on natural keys).

# Workflow
1. **Configuration** – Load secrets from Supabase `secrets` table or Airflow Variable.
2. **Extraction** – Pull raw JSON/CSV from external weather APIs.
3. **Validation** – Parse with `pydantic` models; emit validation errors to a dead‑letter queue.
4. **Transformation** – Apply business rules, convert units, enrich with station metadata.
5. **Loading** – Use `INSERT … ON CONFLICT … DO UPDATE` for idempotent upserts.
6. **Post‑load** – Trigger downstream dbt models via `dbt run-operation`.
7. **Monitoring** – Emit metrics to Prometheus; log to CloudWatch.

# Best Practices
- Keep functions pure; external side‑effects confined to I/O layer.
- Use `asyncio` for I/O‑bound API calls.
- Store intermediate data in Parquet on S3 before bulk load.
- Parameterise dates via Airflow DAG run context.
- Centralise logging format (JSON) for easy ingestion by Metabase.

# Anti‑patterns
- Hard‑coding API keys or DB credentials.
- Mixing transformation logic with database insert statements.
- Ignoring schema evolution – do not drop columns without migration.
- Silent failures – swallow exceptions without reporting.

# Checklist
- [ ] `pyproject.toml` includes `pydantic`, `supabase-py`, `loguru`.
- [ ] All functions have type hints and docstrings.
- [ ] Unit tests cover >80 % of transformation logic.
- [ ] CI pipeline runs `pytest` and `ruff` linting.
- [ ] Airflow task retries set to 3 with exponential back‑off.

# Examples
```python
from supabase import create_client
from pydantic import BaseModel, validator
from loguru import logger

class Observation(BaseModel):
    station_id: str
    observed_at: datetime
    temperature_c: float
    humidity_pct: float
    payload: dict

    @validator('temperature_c')
    def temp_range(cls, v):
        assert -80 <= v <= 60, "temperature out of range"
        return v

def load_observations(observations: List[Observation]):
    client = create_client(url=SUPABASE_URL, key=SUPABASE_KEY)
    sql = """INSERT INTO weather_observations (station_id, observed_at, temperature_c, humidity_pct, payload)
             VALUES (%s,%s,%s,%s,%s)
             ON CONFLICT (station_id, observed_at) DO UPDATE
             SET temperature_c = EXCLUDED.temperature_c,
                 humidity_pct = EXCLUDED.humidity_pct,
                 payload = EXCLUDED.payload;"""
    data = [(o.station_id, o.observed_at, o.temperature_c, o.humidity_pct, json.dumps(o.payload)) for o in observations]
    client.postgrest.from_('weather_observations').insert(data)
```

# Project‑Specific Guidance
- Place ETL package under `philweather_etl/etl/`.
- Store API keys for NOAA in Supabase `secrets` table; load via `supabase_py`.
- Use the Airflow `PythonOperator` with `provide_context=True` to pass `ds` (execution date).
- After successful load, fire a Metabase webhook to refresh the weather dashboard.
