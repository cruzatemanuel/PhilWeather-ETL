---
name: dbt-analytics-engineer
description: Guides design, development, and deployment of dbt models for weather analytics on Supabase.
---

# Purpose
Provide a comprehensive framework for building, testing, and maintaining dbt models that transform raw weather data into analytics‑ready tables for Metabase dashboards.

# When to Use
- Creating new marts (e.g., daily_summary, station_metrics).
- Refactoring existing models for performance.
- Adding tests, snapshots, or documentation.
- Deploying dbt runs via Airflow or Docker.

# Responsibilities
- Write modular `SELECT` statements using CTEs.
- Define tests (`unique`, `not_null`, `relationships`).
- Manage seeds and snapshots for static reference data.
- Version‑control models in `models/` with clear folder hierarchy.
- Configure dbt Cloud or CLI profiles for Supabase connection.

# Workflow
1. **Create Model** – Add `.sql` file under `models/` with appropriate `{{ config(...) }}`.
2. **Add Tests** – Create schema tests in the same file or separate `tests/` directory.
3. **Run locally** – `dbt run --models <model>` and `dbt test` against a local Docker PostgreSQL.
4. **Document** – Use `dbt docs generate` and `dbt docs serve` for interactive docs.
5. **CI Integration** – Add `dbt deps && dbt build` steps in GitHub Actions.
6. **Deploy** – Trigger via Airflow `BashOperator` or GitHub Actions to run against Supabase.
7. **Monitor** – Track model run times and failures in Metabase logs.

# Best Practices
- Keep each model focused on a single business concept.
- Use `ref()` for dependencies to ensure proper DAG ordering.
- Store raw tables in a `stg_` schema, curated tables in `int_` or `mart_`.
- Leverage incremental models for large historical tables.
- Document columns with `description` property; generate docs.

# Anti‑patterns
- Writing massive monolithic models ( > 500 lines).
- Hard‑coding table names instead of using `ref()`.
- Ignoring dbt test failures; allowing broken data.
- Using `SELECT *` – defeats column‑level documentation.
- Frequent schema changes without migrations; leads to broken downstream.

# Checklist
- [ ] Model file follows `{{ config(materialized='incremental') }}` when appropriate.
- [ ] At least one test per column (unique/not_null).
- [ ] Model passes `dbt compile` without errors.
- [ ] Documentation added via `{{ docs('...') }}`.
- [ ] CI pipeline runs `dbt build` on pull request.
- [ ] Incremental model has proper `unique_key` and `is_incremental()` logic.

# Examples
```sql
-- models/stg_weather_observations.sql
{{ config(materialized='incremental', unique_key='id') }}

WITH source AS (
    SELECT * FROM {{ source('supabase', 'weather_observations') }}
    WHERE observed_at >= (SELECT MAX(observed_at) FROM {{ this }})
)
SELECT
    id,
    station_id,
    observed_at,
    temperature_c,
    humidity_pct,
    payload
FROM source;

{% if not is_incremental() %}
    -- Full refresh logic if needed
{% endif %}
```

# Project‑Specific Guidance
- Configure dbt profile `supabase` with `type: postgres`, `host: <supabase-host>`, `port: 5432`, `user: service_role`, `password: <SERVICE_ROLE_KEY>`.
- Place dbt project under `philweather_dbt/`.
- Use Airflow `BashOperator` to run `dbt run --models stg_+ int_+ mart_+` after the loader DAG completes.
- After successful dbt run, call Metabase API to refresh the `weather` collection.
