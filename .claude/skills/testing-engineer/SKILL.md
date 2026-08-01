---
name: testing-engineer
description: Provides a comprehensive testing strategy for Python ETL, SQL dbt models, Docker containers, and Airflow DAGs in the PhilWeather project.
---

# Purpose
Define reusable testing patterns, tools, and CI integration to ensure reliability and correctness of the weather data pipeline.

# When to Use
- Adding new ETL extraction or transformation logic.
- Refactoring existing dbt models or Airflow DAGs.
- Before releasing a new Docker image.
- Whenever a bug is discovered and a regression test is needed.

# Responsibilities
- Write unit tests for pure Python functions (pytest, hypothesis).
- Create integration tests that run against a temporary PostgreSQL container.
- Author dbt tests (schema, data, and custom tests) and ensure they run in CI.
- Validate Docker images with `container-structure-test`.
- Test Airflow DAGs using the `airflow` testing utilities.

# Workflow
1. **Identify Test Scope** – Determine unit vs integration vs end‑to‑end coverage.
2. **Set Up Test Fixtures** – Use `pytest-fixture` to spin up a Docker PostgreSQL (`testcontainers`) and load seed data.
3. **Write Tests** –
   - Python: `assert` statements, property‑based testing with `hypothesis`.
   - SQL: `dbt test` with `schema.yml` and custom `test_` macros.
   - Docker: `hadolint` and `container-structure-test` YAML.
   - Airflow: `airflow tasks test <dag> <task> <date>` within CI.
4. **Run Locally** – Execute `pytest` and `dbt test` to ensure fast feedback.
5. **CI Integration** – Add steps to GitHub Actions:
   ```yaml
   - name: Test Python
     run: pytest -q --cov=philweather_etl
   - name: Test dbt
     run: dbt test --profiles-dir ./profiles
   - name: Test Docker
     run: container-structure-test test --image philweather/loader:${{ github.sha }} --config test/docker/loader-test.yaml
   ```
6. **Report** – Publish test results and coverage to the PR.
7. **Maintenance** – Update flaky test markers, keep fixtures in sync with schema migrations.

# Best Practices
- Keep tests deterministic; mock external API calls with `responses` or `httpretty`.
- Use `pytest-xdist` for parallel test execution.
- Aim for ≥80 % line coverage on new code.
- Separate fast unit tests from slower integration tests using markers (`@pytest.mark.integration`).
- Store test data in `tests/fixtures/` as CSV/JSON that mirrors production formats.

# Anti‑patterns
- Relying on live Supabase instance for CI tests.
- Writing tests that depend on execution order.
- Using `assert` statements without descriptive messages.
- Ignoring dbt test failures and proceeding with deployment.
- Over‑mocking to the point where test no longer reflects real behavior.

# Checklist
- [ ] Unit tests exist for each new function (≥80 % coverage).
- [ ] Integration tests spin up a temporary PostgreSQL container.
- [ ] dbt schema tests (`unique`, `not_null`, `relationships`) are defined.
- [ ] Docker image passes `hadolint` and `container-structure-test`.
- [ ] Airflow DAG syntax validated with `airflow dags list`.
- [ ] CI pipeline runs all test suites on PRs.
- [ ] Flaky tests are marked and investigated.

# Examples
```python
# tests/test_loader.py
import pytest
from philweather_etl.loader import extract_weather

@pytest.fixture(scope='module')
def db_container():
    from testcontainers.postgres import PostgresContainer
    with PostgresContainer('postgres:15') as pg:
        yield pg

def test_extract_returns_observations(db_container):
    observations = extract_weather(date='2024-07-01')
    assert len(observations) > 0
    assert all(o.station_id for o in observations)
```

```yaml
# test/docker/loader-test.yaml
schemaVersion: '2.0.0'
metadataTest:
  env:
    - name: SUPABASE_URL
      value: "http://localhost:8000"
fileExistenceTests:
  - name: "entrypoint"
    path: "/usr/local/bin/python"
```

# Project‑Specific Guidance
- Place all tests under `philweather_etl/tests/`.
- Use the `pytest` configuration in `pyproject.toml` that adds the `supabase` fixture.
- dbt tests should be run against the Supabase replica using the `supabase` profile.
- After a successful load DAG, the CI job should execute `dbt run` followed by `dbt test`.
- Docker images are built from `docker/loader/` and `docker/airflow/`; keep their test configs in `test/docker/`.
