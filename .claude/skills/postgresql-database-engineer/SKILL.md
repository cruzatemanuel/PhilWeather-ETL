---
name: postgresql-database-engineer
description: Expertise in designing, implementing, and optimizing PostgreSQL/Supabase databases for data pipelines.
---

# Purpose
Provide guidance and reusable patterns for building robust PostgreSQL databases, schemas, migrations, and performance tuning within the PhilWeather ETL project.

# When to Use
- Designing a new schema for weather data ingestion.
- Migrating existing tables to Supabase.
- Optimizing queries for large time‑series datasets.
- Implementing role‑based access control.

# Responsibilities
- Define logical and physical data models.
- Write and version control migration scripts (SQL or dbt).
- Configure connection pooling and replication.
- Setup backup, restore, and point‑in‑time recovery.
- Monitor performance metrics (pg_stat_statements, EXPLAIN).

# Workflow
1. **Requirements Gathering** – Identify entities (stations, observations, forecasts).\\
2. **Schema Design** – Draft ER diagram, choose appropriate data types (JSONB, TIMESTAMP WITH TIME ZONE).\\
3. **Migration Draft** – Write `CREATE TABLE` / `ALTER TABLE` statements in `sql/migrations/`.\\
4. **Review & Test** – Use a local Docker PostgreSQL instance, run unit tests against sample data.\\
5. **Deploy to Supabase** – Apply migrations via Supabase CLI, enable Row Level Security (RLS).\\
6. **Performance Tuning** – Add indexes, configure `work_mem`, enable `pg_hint_plan`.\\
7. **Monitoring** – Add pgAdmin dashboards, set up alerts in Metabase.

# Best Practices
- Use `BIGINT` for primary keys, `UUID` for external IDs.
- Store raw JSON payloads in `JSONB` for flexibility.
- Partition large tables by `date` using declarative partitioning.
- Keep migrations idempotent; name them with timestamps.
- Enable `RLS` and principle‑of‑least‑privilege roles for API users.

# Anti‑patterns
- Storing denormalized CSV strings in a single column.
- Over‑indexing leading to write amplification.
- Exposing `superuser` credentials to Airflow tasks.
- Ignoring time‑zone handling – leads to inconsistent forecasts.

# Checklist
- [ ] ER diagram reviewed with data team.
- [ ] All columns have explicit `NOT NULL` where appropriate.
- [ ] Indexes on foreign keys and timestamp columns.
- [ ] RLS policies defined for `public` and `analytics` roles.
- [ ] Migration scripts pass on a fresh DB.
- [ ] Backup schedule verified (daily full, hourly WAL).

# Examples
```sql
-- migrations/20240715_create_weather_observations.sql
CREATE TABLE IF NOT EXISTS public.weather_observations (
    id BIGSERIAL PRIMARY KEY,
    station_id UUID NOT NULL REFERENCES public.stations(id),
    observed_at TIMESTAMPTZ NOT NULL,
    temperature_c NUMERIC(5,2),
    humidity_pct NUMERIC(4,2),
    payload JSONB
) PARTITION BY RANGE (observed_at);

-- Partition for 2024
CREATE TABLE public.weather_observations_2024 PARTITION OF public.weather_observations
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

# Project‑Specific Guidance
- Use Supabase `auth.users` as the source of truth for user‑scoped API keys.
- Store Airflow connection strings in Supabase `secrets` table, accessed via `supabase_py`.
- Connect Metabase to the Supabase replica for analytics dashboards.
- Leverage Supabase Edge Functions for lightweight data validation before ingestion.
