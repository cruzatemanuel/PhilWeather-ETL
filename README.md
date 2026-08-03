# PhilWeather ETL 🇵🇭☀️🌧️

A production-inspired batch ETL pipeline that extracts weather data for Philippine cities from OpenWeather API, archives raw JSON payloads, loads raw data into PostgreSQL (Supabase Bronze layer), transforms data using dbt, orchestrates execution automatically using Apache Airflow, and serves analytics via Metabase dashboards.

---

## 🏗️ Architecture

```
                  ┌──────────────────────┐
                  │   OpenWeather API    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Python Extraction   │
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌──────────────────────┐           ┌──────────────────────┐
│  Raw JSON Archival   │           │ PostgreSQL (Bronze)  │
│  (data/raw_json/)    │           │ (Supabase raw_weather│
└──────────────────────┘           └──────────┬───────────┘
                                              │
                                              ▼
                                   ┌──────────────────────┐
                                   │ dbt Transformations  │
                                   │ (Staging/Warehouse)  │
                                   └──────────┬───────────┘
                                              │
                                              ▼
                                   ┌──────────────────────┐
                                   │ Gold Analytics Marts │
                                   └──────────┬───────────┘
                                              │
                                              ▼
                                   ┌──────────────────────┐
                                   │  Metabase Dashboards │
                                   └──────────────────────┘
```

> **Orchestration**: Apache Airflow manages and monitors the complete Extract → Validate → Archive → Load → dbt Transform pipeline end-to-end.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Configuration & Validation**: Pydantic v2 / Pydantic-Settings
- **Database / Warehouse**: PostgreSQL (Supabase)
- **Transformations**: dbt Core (`dbt-postgres`)
- **Orchestration**: Apache Airflow (Dockerized)
- **Visualization**: Metabase
- **Data Source**: OpenWeather API

---

## 📂 Repository Structure

```
philweather-etl/
├── airflow/               # Airflow DAGs, plugins, and docker-compose
│   ├── dags/
│   └── plugins/
├── dashboard/             # Metabase export definitions & query documentation
├── data/                  # Local storage for data assets
│   ├── logs/              # Pipeline log files
│   └── raw_json/          # Archived raw weather payloads
├── dbt_weather/           # dbt transformations project
│   ├── models/
│   │   ├── staging/       # Silver layer staging models
│   │   ├── warehouse/     # Silver/Gold dimensional models (dim_city, fct_daily_weather)
│   │   └── marts/         # Gold analytics marts
│   └── tests/             # Custom dbt data tests
├── docs/                  # Architecture & ER diagrams, technical specs
├── scripts/               # Core Python ETL scripts
│   ├── config.py          # Pydantic environment configuration
│   ├── utils.py           # Logging setup & helpers
│   └── health_check.py    # Service connectivity diagnostic
├── sql/                   # DDL scripts (e.g., Bronze raw_weather schema)
├── .env.example           # Environment template file
├── README.md              # Project documentation
├── ROADMAP.md             # Multi-phase implementation roadmap
└── requirements.txt       # Python package dependencies
```

---

## 🚀 Quick Start & Environment Setup

### 1. Prerequisites
- Python 3.10+
- Virtual environment (`venv` or `conda`)
- OpenWeather API Key (Free Tier)
- Supabase PostgreSQL Database credentials

### 2. Installation
Clone the repository and set up a Python virtual environment:

```bash
git clone https://github.com/your-username/philweather-etl.git
cd philweather-etl

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and fill in your actual credentials:

```bash
cp .env.example .env
```

Update your `.env` with:
- `OPENWEATHER_API_KEY`: Your OpenWeather API key
- `SUPABASE_DB_HOST`, `SUPABASE_DB_PORT`, `SUPABASE_DB_USER`, `SUPABASE_DB_PASSWORD`: Your Supabase connection details

### 4. Connectivity Health Check
Run the diagnostic script to verify settings loading and connectivity to OpenWeather and Supabase:

```bash
python3 scripts/health_check.py
```

Expected output:
```text
======================================================================
 🇵🇭 PhilWeather ETL — System Environment & Health Diagnostic
======================================================================
Target Cities: Manila, Cebu, Davao, Baguio, Iloilo, Cagayan de Oro
Database Host: db.your-ref.supabase.co:5432/postgres
----------------------------------------------------------------------
--> Checking OpenWeather API connectivity...
--> Checking Supabase PostgreSQL database connectivity...

======================================================================
 HEALTH DIAGNOSTIC SUMMARY
======================================================================
[✅ PASS] OpenWeather API        (Latency: 142.5 ms)
        Details: Connected OK (City: Manila, Temp: 29.5°C, Condition: few clouds)
[✅ PASS] Supabase PostgreSQL    (Latency: 310.2 ms)
        Details: Connected OK (PostgreSQL 15.1)
======================================================================
 SUCCESS: All services are healthy and fully reachable!
======================================================================
```

---

## 📊 Development Roadmap Summary

- [x] **Phase 1**: Project Foundations & Environment Setup
- [ ] **Phase 2**: Extraction Layer (OpenWeather API pull + archival)
- [ ] **Phase 3**: Data Validation Layer (Pydantic schema validation)
- [ ] **Phase 4**: Bronze Load Layer (Append-only raw PostgreSQL load)
- [ ] **Phase 5**: Containerization & Airflow Scaffolding
- [ ] **Phase 6**: Airflow DAG Orchestration
- [ ] **Phase 7–9**: dbt Setup, Staging, Warehouse & Gold Marts
- [ ] **Phase 10**: Airflow + dbt End-to-End Integration
- [ ] **Phase 11**: Metabase Analytics Dashboards
- [ ] **Phase 12**: End-to-End Hardening & Security Audit
- [ ] **Phase 13**: Final Documentation & Portfolio Polish

---

## 📜 License
MIT License. Free to use for educational and portfolio demonstration purposes.