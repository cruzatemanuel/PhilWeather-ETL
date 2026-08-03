# PhilWeather ETL — Project Roadmap

**Status legend:** ⬜ Not started · 🟨 In progress · ✅ Complete

## Progress Checklist

- [ ] Phase 1 — Project Foundations & Environment Setup
- [ ] Phase 2 — Extraction Layer
- [ ] Phase 3 — Data Validation Layer
- [ ] Phase 4 — Bronze Load Layer
- [ ] Phase 5 — Containerization & Airflow Scaffolding
- [ ] Phase 6 — Airflow DAG (Extract → Validate → Archive → Load)
- [ ] Phase 7 — dbt Setup & Staging Models
- [ ] Phase 8 — dbt Warehouse Models
- [ ] Phase 9 — dbt Mart Models
- [ ] Phase 10 — Airflow + dbt Integration
- [ ] Phase 11 — Metabase Dashboards
- [ ] Phase 12 — End-to-End Testing, Hardening & Security Review
- [ ] Phase 13 — Documentation & Portfolio Polish
- [ ] Phase 14 (Optional) — CI/CD & Extensions

**Estimated total:** ~50–55 hours across Phases 1–13, +3–5 hours if you do Phase 14. At 5–7 hrs/week around a full course load, that's roughly 8–10 weeks.

---

## Phase 1 — Project Foundations & Environment Setup

**Objective:** Establish the repo scaffold, configuration/secrets strategy, and verified connectivity to every external service, so nothing later gets built on shaky ground.
**Deliverables:** Full directory scaffold · validated config layer · confirmed OpenWeather + Supabase connectivity · README skeleton
**Files:** Full `philweather-etl/` tree, `.gitignore`, `.env.example`, `requirements.txt`, `scripts/config.py`, `scripts/utils.py`, `scripts/health_check.py`, `README.md`
**Dependencies:** None — starting point
**Est. time:** 2–3 hours
**Git commit:** `chore: scaffold repository structure and environment configuration`

## Phase 2 — Extraction Layer

**Objective:** Reliably pull current weather data from OpenWeather for a configurable list of cities and persist the raw response untouched.
**Deliverables:** `extract.py` with retry/backoff and structured logging · partitioned raw JSON archive · resolved city-matching strategy (name string vs. lat/lon)
**Files:** `scripts/extract.py`
**Dependencies:** Phase 1
**Est. time:** 3–4 hours
**Git commit:** `feat: implement weather extraction with retry logic and raw archival`

## Phase 3 — Data Validation Layer

**Objective:** Guard the Bronze layer from malformed or partial API payloads before they ever reach the database.
**Deliverables:** `validate.py` with schema + business-rule checks · quarantine strategy for bad records · resolved validate-before-archive vs. archive-before-validate ordering
**Files:** `scripts/validate.py`
**Dependencies:** Phase 2
**Est. time:** 2–3 hours
**Git commit:** `feat: add payload validation layer with quarantine handling`

## Phase 4 — Bronze Load Layer

**Objective:** Land validated raw JSON into PostgreSQL as an immutable, append-only Bronze table.
**Deliverables:** `raw_weather` DDL · idempotent batch load logic
**Files:** `sql/raw_weather.sql`, `scripts/load.py`
**Dependencies:** Phase 1, Phase 3
**Est. time:** 3–4 hours
**Git commit:** `feat: implement Bronze load layer with idempotent inserts`

## Phase 5 — Containerization & Airflow Scaffolding

**Objective:** Stand up a local Airflow instance in Docker that can actually execute our Python scripts.
**Deliverables:** Working `airflow/docker-compose.yml` · resolved dependency-delivery strategy (custom image vs. mounted requirements vs. `PythonVirtualenvOperator`) · healthy Airflow UI
**Files:** `airflow/docker-compose.yml`, `airflow/Dockerfile` (if a custom image is chosen)
**Dependencies:** Phases 1–4
**Est. time:** 3–5 hours
**Git commit:** `chore: add Airflow docker-compose scaffold`

## Phase 6 — Airflow DAG: Extract → Validate → Archive → Load

**Objective:** Orchestrate Phases 2–4 as one scheduled DAG with explicit task dependencies, retries, and observability.
**Deliverables:** `weather_pipeline` DAG using the TaskFlow API · Airflow Connections/Variables for secrets · a successful manual DAG run
**Files:** `airflow/dags/weather_pipeline_dag.py`
**Dependencies:** Phase 5
**Est. time:** 4–6 hours
**Git commit:** `feat: add Airflow DAG orchestrating extract-validate-load`

## Phase 7 — dbt Setup & Staging Models

**Objective:** Initialize dbt against Supabase and build the first Bronze → Silver transformation.
**Deliverables:** `dbt_weather` project scaffold · `sources.yml` · `stg_weather.sql` · first dbt tests
**Files:** `dbt_weather/models/staging/*`, `dbt_weather/dbt_project.yml`
**Dependencies:** Phase 4
**Est. time:** 4–5 hours
**Git commit:** `feat: initialize dbt project with staging model`

## Phase 8 — dbt Warehouse Models

**Objective:** Build the dimensional core — `dim_city` and `fct_daily_weather` — at an explicit, documented grain.
**Deliverables:** Dimension + fact models with surrogate keys and tests
**Files:** `dbt_weather/models/warehouse/*`
**Dependencies:** Phase 7
**Est. time:** 4–6 hours
**Git commit:** `feat: add warehouse layer dimensional models`

## Phase 9 — dbt Mart Models

**Objective:** Build the three analytics-ready marts Metabase will query directly.
**Deliverables:** `mart_monthly_summary`, `mart_temperature_trend`, `mart_weather_conditions`
**Files:** `dbt_weather/models/marts/*`
**Dependencies:** Phase 8
**Est. time:** 4–6 hours
**Git commit:** `feat: add Gold-layer analytics marts`

## Phase 10 — Airflow + dbt Integration

**Objective:** Extend the DAG so `dbt run` / `dbt test` execute automatically after a successful load, completing full orchestration.
**Deliverables:** Updated DAG with dbt tasks · failure-handling strategy · pipeline-completion reporting task
**Files:** `airflow/dags/weather_pipeline_dag.py` (updated)
**Dependencies:** Phase 6, Phase 9
**Est. time:** 3–4 hours
**Git commit:** `feat: integrate dbt run and test into Airflow DAG`

## Phase 11 — Metabase Dashboards

**Objective:** Stand up Metabase and build all 7 required visualizations against the Gold marts.
**Deliverables:** Metabase container · connected data source · complete dashboard (avg temp, monthly trends, humidity, rainfall, condition distribution, city comparison, wind speed)
**Files:** `dashboard/*`, docker-compose additions
**Dependencies:** Phase 9
**Est. time:** 3–5 hours
**Git commit:** `chore: add Metabase service and initial dashboards`

## Phase 12 — End-to-End Testing, Hardening & Security Review

**Objective:** Stress-test the full pipeline against realistic failure modes and audit secrets hygiene before calling it done.
**Deliverables:** Documented failure-mode tests (API downtime, malformed payload, DB unavailability) · idempotency/backfill verification · secrets audit
**Files:** `docs/testing_notes.md`, `tests/*`
**Dependencies:** Phase 10
**Est. time:** 4–6 hours
**Git commit:** `test: add end-to-end pipeline hardening and security review`

## Phase 13 — Documentation & Portfolio Polish

**Objective:** Produce the documentation package that makes this read as a portfolio project, not just working code.
**Deliverables:** Final README · architecture/pipeline/ER diagrams · setup guide · screenshots · lessons learned · future improvements
**Files:** `README.md` (final), `docs/architecture_diagram.*`, `docs/pipeline_diagram.*`, `docs/er_diagram.*`, `docs/setup_guide.md`
**Dependencies:** All prior phases substantially complete
**Est. time:** 4–6 hours
**Git commit:** `docs: complete project documentation and diagrams`

## Phase 14 (Optional) — CI/CD & Extensions

**Objective:** Add automated checks and optionally extend the project's scope for extra differentiation.
**Deliverables:** GitHub Actions workflow (lint + dbt compile check) · stretch ideas (forecast model, alerting, more cities)
**Files:** `.github/workflows/ci.yml`
**Dependencies:** Phase 13
**Est. time:** 3–5 hours
**Git commit:** `ci: add GitHub Actions pipeline for lint and dbt compile checks`

---

## Design Decisions Flagged for Later Phases

Called out now so they don't get lost, but deliberately not resolved yet — we don't have enough information until we're in the relevant phase:

- **Phase 2/3:** validate-then-archive vs. archive-then-validate. Your DAG spec lists Validate before Archive; medallion-architecture convention usually archives raw data first (preserve everything, even garbage, for replay/debugging) and validates as a gate before Load. Real trade-off, worth deciding deliberately rather than by default.
- **Phase 2:** matching cities by name string (`"Manila,PH"`) vs. resolving each city to lat/lon once via OpenWeather's Geocoding API and querying by coordinates thereafter (more robust, avoids ambiguous city-name collisions).
- **Phase 5:** how the Airflow container gets access to `scripts/`'s dependencies — custom Airflow image with `requirements.txt` baked in, a mounted volume, or `PythonVirtualenvOperator`.
- **Phase 8:** grain of `fct_daily_weather` — one row per city per calendar day vs. one row per API pull (matters if the schedule ever runs more than once a day).
- **Phase 9:** incremental vs. full-refresh materialization for the marts as historical volume grows.

---

_This file is meant to live at `docs/ROADMAP.md` in the repo. Update the checkboxes as phases complete._
