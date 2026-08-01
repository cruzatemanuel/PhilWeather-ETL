---
name: airflow-dag-engineer
description: Provides patterns and guidance for building maintainable Airflow DAGs to orchestrate weather ETL pipelines.
---

# Purpose
Standardise the creation, testing, and deployment of Airflow DAGs that coordinate data extraction, transformation, and loading for the PhilWeather project.

# When to Use
- Defining a new scheduled ingestion pipeline.
- Refactoring monolithic DAGs into modular sub‑DAGs.
- Adding alerting, retries, and SLA monitoring.
- Integrating dbt and Docker tasks within Airflow.

# Responsibilities
- Design DAG structure with clear dependencies.
- Use reusable custom operators for Supabase, dbt, and Docker.
- Implement idempotent tasks and proper execution dates.
- Manage Airflow Variables / Connections securely.
- Write unit tests with `airflow‑testing` utilities.

# Workflow
1. **Define DAG File** – Place in `dags/` following naming convention `weather_<name>_dag.py`.
2. **Configure Default Args** – `retries`, `retry_delay`, `execution_timeout`, `on_failure_callback`.
3. **Create Tasks** – Use `PythonOperator`, `DockerOperator`, `BashOperator` or custom operators for Supabase and dbt.
4. **Set Dependencies** – Use `>>` and `<<` to express logical order; group related tasks with `TaskGroup`.
5. **Testing** – Run `airflow tasks test <dag_id> <task_id> <execution_date>` locally; add `pytest` tests with `airflow.models.DagBag`.
6. **Deployment** – Store DAGs in Git; CI pipeline copies them to `$AIRFLOW_HOME/dags` or uses `helm` chart values.
7. **Monitoring** – Configure SLA miss alerts, UI health checks, and Metabase dashboard refresh.

# Best Practices
- Keep DAG code pure; avoid heavy logic inside the DAG file itself.
- Parameterise dates and environment via `{{ ds }}` and Airflow Variables.
- Use `TriggerRule.ALL_DONE` for cleanup tasks.
- Limit DAG run duration (< 30 min) to avoid scheduler overload.
- Version‑control custom operators as a pip‑installable package.

# Anti‑patterns
- Hard‑coding connection strings inside the DAG.
- Using `BashOperator` for complex Python logic.
- Overly long task execution times causing scheduler starvation.
- Ignoring task retries – leads to data loss on transient failures.

# Checklist
- [ ] DAG file passes `airflow dags list` without errors.
- [ ] All tasks have `owner` and `email_on_failure` set.
- [ ] Secrets fetched from Supabase via `Variable.get` with `deserialize_json=True`.
- [ ] Unit tests cover each operator's success and failure paths.
- [ ] CI pipeline validates DAG syntax (`airflow dags check`).

# Examples
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
}

with DAG(
    dag_id='weather_ingest',
    schedule_interval='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
) as dag:
    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_weather,
    )

    load = DockerOperator(
        task_id='load_to_supabase',
        image='philweather/loader:latest',
        api_version='auto',
        auto_remove=True,
        command='python -m loader',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
    )

    dbt_run = DockerOperator(
        task_id='dbt_transform',
        image='philweather/dbt:latest',
        command='dbt run --models weather',
        docker_url='unix://var/run/docker.sock',
    )

    extract >> load >> dbt_run
```

# Project‑Specific Guidance
- Store Airflow connection `supabase_conn` in the UI; retrieve via `BaseHook.get_connection('supabase_conn')`.
- Use the `philweather/docker-loader` image built from `docker/loader/` in the repository.
- After `dbt_transform`, push a Metabase cache refresh via HTTP hook.
- Keep DAGs lightweight; heavy ETL logic resides in the Python package under `philweather_etl/`.
