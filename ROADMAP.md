# PhilWeather Analytics Roadmap

## Project Goal

Build a small, portfolio-ready ETL (Extract, Transform, Load) pipeline that demonstrates fundamental Data Engineering skills by processing a 10-year historical weather dataset covering 137 cities in the Philippines (`daily_data_combined_2010_to_2019.csv`) alongside its unit metadata (`daily_units_2010_to_2019.csv`).

The finished project should:

- Read and parse a 500,000+ row daily weather dataset (2010–2019) and unit metadata
- Clean, transform, and derive meaningful weather features using **pandas**
- Load the normalized data into a **PostgreSQL** database with optimized indexes
- Perform analytical SQL queries (aggregations, temporal trends, extreme weather detection, window functions)
- Generate publication-quality visualizations using **matplotlib** & **seaborn**
- Document the project professionally on GitHub as a ready-to-show portfolio piece

**Target Completion:** 2 Weeks

---

# Tech Stack

- **Language:** Python 3.10+
- **Data Processing:** pandas, NumPy
- **Database:** PostgreSQL 14+
- **ORM / DB Driver:** SQLAlchemy, psycopg2-binary
- **SQL Analysis:** PostgreSQL dialect (Aggregations, CTEs, Window Functions)
- **Data Visualization:** matplotlib, seaborn
- **Version Control:** Git, GitHub

---

# Data Dictionary (`daily_data_combined_2010_to_2019.csv` & `daily_units_2010_to_2019.csv`)

The raw dataset contains **500,324 rows** across **24 columns**, representing 10 years (2010-01-01 to 2019-12-31) of daily ERA5 historical weather data for **137 Philippine cities**. Measurement units for each variable are sourced from `daily_units_2010_to_2019.csv`.

| Field Name | Raw Type | Target SQL Type | Unit | Description | Sample Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `city_name` | String | `VARCHAR(100)` | Text | Name of the Philippine city | `'Alaminos'` |
| `latitude` | Float | `DECIMAL(8,6)` | `°N` | Geographic latitude coordinate | `16.156111` |
| `longitude` | Float | `DECIMAL(9,6)` | `°E` | Geographic longitude coordinate | `119.98111` |
| `datetime` | String | `DATE` | `iso8601` | Recording date (`YYYY-MM-DD`) | `'2010-01-01'` |
| `weather_code` | Float | `SMALLINT` | `wmo code` | WMO Weather interpretation code | `1.0` |
| `temperature_2m_max` | Float | `DECIMAL(4,1)` | `°C` | Maximum daily air temp at 2m | `29.9` |
| `temperature_2m_min` | Float | `DECIMAL(4,1)` | `°C` | Minimum daily air temp at 2m | `24.8` |
| `temperature_2m_mean` | Float | `DECIMAL(4,1)` | `°C` | Mean daily air temp at 2m | `26.6` |
| `apparent_temperature_max` | Float | `DECIMAL(4,1)` | `°C` | Max daily apparent temp / heat index | `32.0` |
| `apparent_temperature_min` | Float | `DECIMAL(4,1)` | `°C` | Min daily apparent temp / heat index | `26.5` |
| `apparent_temperature_mean` | Float | `DECIMAL(4,1)` | `°C` | Mean daily apparent temp / heat index | `29.1` |
| `sunrise` | String | `TIMESTAMP` | `iso8601` | Sunrise timestamp (`YYYY-MM-DDTHH:MM`) | `'2010-01-01T06:28'` |
| `sunset` | String | `TIMESTAMP` | `iso8601` | Sunset timestamp (`YYYY-MM-DDTHH:MM`) | `'2010-01-01T17:39'` |
| `daylight_duration` | Float | `DECIMAL(8,2)` | `s` | Total daylight duration in seconds | `40269.62` |
| `sunshine_duration` | Float | `DECIMAL(8,2)` | `s` | Total sunshine duration in seconds | `36331.94` |
| `precipitation_sum` | Float | `DECIMAL(6,2)` | `mm` | Total daily precipitation | `0.0` |
| `rain_sum` | Float | `DECIMAL(6,2)` | `mm` | Daily rain sum | `0.0` |
| `snowfall_sum` | Float | `DECIMAL(4,2)` | `cm` | Daily snowfall sum (always `0.0` in PH) | `0.0` |
| `precipitation_hours` | Float | `DECIMAL(4,1)` | `h` | Hours with precipitation in a day | `0.0` |
| `wind_speed_10m_max` | Float | `DECIMAL(5,1)` | `km/h` | Maximum wind speed at 10m | `16.5` |
| `wind_gusts_10m_max` | Float | `DECIMAL(5,1)` | `km/h` | Maximum wind gusts at 10m | `33.5` |
| `wind_direction_10m_dominant` | Float | `SMALLINT` | `°` | Dominant wind direction in degrees (0–360°) | `141.0` |
| `shortwave_radiation_sum` | Float | `DECIMAL(6,2)` | `MJ/m²` | Solar shortwave radiation sum | `18.63` |
| `et0_fao_evapotranspiration` | Float | `DECIMAL(5,2)` | `mm` | FAO reference evapotranspiration | `4.4` |

---

# Project Structure

```text
philweather-analytics/

├── data/
│   ├── raw/
│   │   ├── daily_data_combined_2010_to_2019.csv
│   │   └── daily_units_2010_to_2019.csv
│   └── cleaned/
│       └── daily_weather_cleaned.csv
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── visualize.py
│
├── sql/
│   ├── 01_hottest_cities.sql
│   ├── 02_rainiest_cities.sql
│   ├── 03_monthly_climate_profile.sql
│   ├── 04_extreme_weather_events.sql
│   └── 05_city_rainfall_ranking_window.sql
│
├── charts/
│   ├── monthly_temp_apparent_trend.png
│   ├── top_10_rainiest_cities.png
│   ├── top_10_hottest_cities_heat_index.png
│   └── extreme_weather_scatter.png
│
├── notebooks/
│   └── data_exploration.ipynb
│
├── README.md
├── ROADMAP.md
├── requirements.txt
└── .gitignore
```

---

# Project Workflow

```text
daily_data_combined_2010_to_2019.csv + daily_units_2010_to_2019.csv
        │
        ▼
extract.py
(Read Weather Dataset & Parse Unit Metadata)
        │
        ▼
transform.py (pandas)
(Data Cleaning, Type Casting, Unit Conversion, Feature Engineering & Validation)
        │
        ▼
load.py (SQLAlchemy / PostgreSQL)
(Create Schema, Batch Load & Index city_name + datetime)
        │
        ▼
SQL Analysis (psycopg2 / SQL Scripts)
(Aggregations, Heat Index Analysis, Typhoon Markers, Window Functions)
        │
        ▼
visualize.py (matplotlib / seaborn)
(Publication-Quality Charts with Corrected Units)
        │
        ▼
GitHub Portfolio Presentation
(Comprehensive README & Insights)
```

---

# Phase 1 — Project Setup

## Objective

Prepare the development environment, database instance, and repository structure.

## Tasks

- Create Python virtual environment (`venv`)
- Install project dependencies (`pandas`, `sqlalchemy`, `psycopg2-binary`, `matplotlib`, `seaborn`)
- Setup local PostgreSQL database (`philweather_db`)
- Configure `.gitignore` (ignore `data/raw/*.csv`, virtual environments, and `.env`)
- Create `requirements.txt`
- Set up project directory tree

## Deliverables

- Clean, structured repository layout
- Configured PostgreSQL database connection
- Verified `requirements.txt`

---

# Phase 2 — Data Exploration

## Objective

Analyze the raw CSV dataset (`daily_data_combined_2010_to_2019.csv`) and unit metadata (`daily_units_2010_to_2019.csv`) to inform data cleaning rules and database schema design.

## Key Dataset Characteristics Identified

- **Record Count:** 500,324 daily records
- **Coverage:** 137 unique Philippine cities across 10 calendar years (2010-01-01 to 2019-12-31; 3,652 days per city)
- **Completeness:** 0 missing/null values across all 24 columns
- **Unit Metadata:** Units provided per column via `daily_units_2010_to_2019.csv` (e.g. `°C` for temperature, `s` for duration, `mm` for rainfall, `km/h` for wind, `MJ/m²` for solar radiation, `°` for wind direction)
- **Special Characteristics:** `snowfall_sum` is uniformly `0.0` (unit `cm`; tropical climate context); `sunrise` and `sunset` are ISO8601-formatted timestamp strings

## Tasks

- Write exploration script / Jupyter notebook (`notebooks/data_exploration.ipynb`)
- Load and parse `daily_units_2010_to_2019.csv` to map field units
- Verify data types, value ranges, and unexpected values
- Check for duplicate entries on composite key `(city_name, datetime)`
- Calculate summary statistics (min/max temperatures, extreme precipitation, maximum wind speeds)

## Deliverables

- Data profiling output and unit mapping dictionary
- Finalized schema definition mapping raw CSV columns and units to PostgreSQL data types

---

# Phase 3 — Extract

## Objective

Build a modular extraction script to load the raw weather dataset and unit metadata.

## Tasks

- Create `scripts/extract.py`
- Load `daily_data_combined_2010_to_2019.csv` and `daily_units_2010_to_2019.csv`
- Map unit headers from `daily_units_2010_to_2019.csv` to dataframe column metadata
- Implement error handling for missing files or memory bottlenecks
- Log extraction metadata (row counts, column list, unit mapping, execution time)

## Deliverables

- Modular `extract.py` script returning DataFrame with embedded unit metadata

---

# Phase 4 — Transform

## Objective

Clean raw weather data, cast data types, convert unit-based durations (seconds to hours), drop redundant features, and create derived analytical fields.

## Required Transformations

1. **Standardize Column Names:** Ensure snake_case naming matching SQL conventions.
2. **Date & Time Parsing:**
   - Convert `datetime` string to pandas `datetime64[ns]` / `DATE`.
   - Parse `sunrise` and `sunset` into timestamp objects.
3. **Unit Conversions & Feature Engineering:**
   - `temp_range`: Calculate daily temperature swing (`temperature_2m_max` - `temperature_2m_min` in `°C`).
   - `heat_index_diff`: Difference between felt temperature and actual temperature (`apparent_temperature_mean` - `temperature_2m_mean` in `°C`).
   - `daylight_hours`: Convert `daylight_duration` from seconds (`s`) to hours (`h`) (`daylight_duration / 3600`).
   - `sunshine_hours`: Convert `sunshine_duration` from seconds (`s`) to hours (`h`) (`sunshine_duration / 3600`).
   - `year`, `month`, `year_month`: Temporal extractions for accelerated group-by queries.
4. **Column Cleanup:**
   - Drop `snowfall_sum` (redundant column with constant `0.0` value in tropical context).
5. **Data Validation:**
   - Validate temperature constraints (`min <= mean <= max` in `°C`).
   - Validate non-negative bounds for precipitation (`mm`), wind (`km/h`), and radiation (`MJ/m²`).
6. **Export:**
   - Export cleaned dataset to `data/cleaned/daily_weather_cleaned.csv`.

## Deliverables

- Reusable `scripts/transform.py` module
- Cleaned DataFrame ready for database insertion

---

# Phase 5 — Load

## Objective

Load the cleaned 500k+ weather dataset into PostgreSQL with optimized database schema and indexes.

## Database Schema (`daily_weather`)

```sql
CREATE TABLE IF NOT EXISTS daily_weather (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(8,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    datetime DATE NOT NULL,
    weather_code SMALLINT,
    temperature_2m_max DECIMAL(4,1), -- °C
    temperature_2m_min DECIMAL(4,1), -- °C
    temperature_2m_mean DECIMAL(4,1), -- °C
    apparent_temperature_max DECIMAL(4,1), -- °C
    apparent_temperature_min DECIMAL(4,1), -- °C
    apparent_temperature_mean DECIMAL(4,1), -- °C
    sunrise TIMESTAMP,
    sunset TIMESTAMP,
    daylight_hours DECIMAL(4,2), -- hours
    sunshine_hours DECIMAL(4,2), -- hours
    precipitation_sum DECIMAL(6,2), -- mm
    rain_sum DECIMAL(6,2), -- mm
    precipitation_hours DECIMAL(4,1), -- hours
    wind_speed_10m_max DECIMAL(5,1), -- km/h
    wind_gusts_10m_max DECIMAL(5,1), -- km/h
    wind_direction_10m_dominant SMALLINT, -- degrees (°)
    shortwave_radiation_sum DECIMAL(6,2), -- MJ/m²
    et0_fao_evapotranspiration DECIMAL(5,2), -- mm
    temp_range DECIMAL(4,1), -- °C
    heat_index_diff DECIMAL(4,1), -- °C
    year SMALLINT,
    month SMALLINT,
    CONSTRAINT unique_city_date UNIQUE (city_name, datetime)
);

-- Optimization Indexes for 500,000+ Row Analytical Queries
CREATE INDEX idx_weather_city ON daily_weather(city_name);
CREATE INDEX idx_weather_datetime ON daily_weather(datetime);
CREATE INDEX idx_weather_city_date ON daily_weather(city_name, datetime);
CREATE INDEX idx_weather_year_month ON daily_weather(year, month);
```

## Tasks

- Create `scripts/load.py` using SQLAlchemy engine
- Execute DDL to initialize `daily_weather` table and indexes
- Perform high-performance batch insertion (`method='multi'`, `chunksize=10000`)
- Verify row counts against transformed dataset (target: 500,324 rows)

## Deliverables

- Automated database setup and load script (`load.py`)
- Populated PostgreSQL `daily_weather` table

---

# Phase 6 — SQL Analysis

## Objective

Extract meaningful meteorological insights from PostgreSQL using optimized SQL queries leveraging the dataset's specific fields and units.

## Required Queries

### Query 1: Top 10 Hottest Cities by Peak Heat Index & Temperature
- **Filename:** `sql/01_hottest_cities.sql`
- **Fields Used:** `city_name`, `temperature_2m_max`, `apparent_temperature_max`, `heat_index_diff` (°C)
- **Goal:** Rank cities by their average maximum temperature and maximum apparent heat index across 2010–2019.

### Query 2: Top 10 Wettest Cities & Annual Precipitation
- **Filename:** `sql/02_rainiest_cities.sql`
- **Fields Used:** `city_name`, `precipitation_sum` (mm), `precipitation_hours` (h)
- **Goal:** Calculate total accumulated rainfall and annual average precipitation by city to identify the wettest urban areas.

### Query 3: Monthly Climate Profile & Seasonal Heat Difference
- **Filename:** `sql/03_monthly_climate_profile.sql`
- **Fields Used:** `month`, `temperature_2m_mean` (°C), `apparent_temperature_mean` (°C), `precipitation_sum` (mm), `shortwave_radiation_sum` (MJ/m²)
- **Goal:** Aggregate 10-year monthly averages to chart the Philippines' wet and dry seasons and highlight months with extreme heat index gaps.

### Query 4: Extreme Weather Events & Severe Gust / Rainfall Days (Typhoon Markers)
- **Filename:** `sql/04_extreme_weather_events.sql`
- **Fields Used:** `city_name`, `datetime`, `precipitation_sum` (mm), `wind_gusts_10m_max` (km/h), `wind_speed_10m_max` (km/h)
- **Goal:** Filter and count severe weather days (precipitation > 100mm/day or wind gusts > 60 km/h) per city and year.

### Query 5: Window Function — Ranking City Annual Rainfall per Year
- **Filename:** `sql/05_city_rainfall_ranking_window.sql`
- **Fields Used:** `city_name`, `year`, `precipitation_sum` (mm), `DENSE_RANK()` / `ROW_NUMBER()`
- **Goal:** Use SQL Window functions (`DENSE_RANK() OVER (PARTITION BY year ORDER BY sum_rain DESC)`) to rank the top 5 wettest cities for every individual year from 2010 to 2019.

## Deliverables

- 5 executable `.sql` files in `sql/` directory with detailed comments

---

# Phase 7 — Data Visualization

## Objective

Generate publication-ready visualizations using `matplotlib` and `seaborn` with explicit unit labels on all axes and legends.

## Required Charts

### Chart 1: 10-Year Monthly Temperature vs. Apparent Heat Index Trend
- **Filename:** `charts/monthly_temp_apparent_trend.png`
- **Type:** Dual Line Chart with shaded area
- **Y-Axis Unit:** Temperature (°C)
- **Content:** Compares actual mean temperature (`temperature_2m_mean`) against felt apparent temperature (`apparent_temperature_mean`) by month.

### Chart 2: Top 10 Rainiest Cities in the Philippines
- **Filename:** `charts/top_10_rainiest_cities.png`
- **Type:** Vertical Bar Chart with value labels
- **Y-Axis Unit:** Precipitation (mm)
- **Content:** Displays average annual rainfall (mm) for the top 10 wettest Philippine cities.

### Chart 3: Top 10 Hottest Cities by Peak Heat Index
- **Filename:** `charts/top_10_hottest_cities_heat_index.png`
- **Type:** Horizontal Bar Chart (gradient colored)
- **X-Axis Unit:** Apparent Temperature (°C)
- **Content:** Ranks the hottest cities by highest recorded apparent temperature (`apparent_temperature_max`).

### Chart 4: Extreme Weather Event Frequency (Rainfall vs. Wind Gusts)
- **Filename:** `charts/extreme_weather_scatter.png`
- **Type:** Scatter / Bubble Plot
- **X-Axis Unit:** Maximum Wind Gusts (km/h) | **Y-Axis Unit:** Daily Precipitation (mm)
- **Content:** Maps daily precipitation against maximum wind gusts for extreme weather days to visualize tropical storm clusters.

## Deliverables

- `scripts/visualize.py` script
- 4 high-resolution PNG charts saved in `charts/`

---

# Phase 8 — Documentation

## Objective

Create a comprehensive, portfolio-ready GitHub `README.md`.

## README Requirements

1. **Title & Badge:** Clean title with project metadata tags.
2. **Executive Summary:** Overview of the 10-year Philippine weather dataset (500k+ rows, 137 cities) and unit metadata file.
3. **Architecture Diagram:** ASCII or graphic ETL flow diagram.
4. **Data Dictionary:** Formatted table of raw, unit-annotated, and transformed fields.
5. **Key Analytical Insights:** Summarized findings from SQL queries with unit metrics (e.g., °C, mm, km/h).
6. **Visualizations Showcase:** Embedded chart previews with clear unit labels and commentary.
7. **Database Schema & SQL Queries:** Key SQL queries with window functions documented.
8. **Instructions to Run:** Step-by-step setup guide (`pip install`, database creation, script execution order).

---

# Phase 9 — Final Review

## Objective

Validate system end-to-end and clean repository for publication.

## Checklist

- [ ] All code adheres to PEP 8 standard formatting
- [ ] No hardcoded database credentials or secrets (`use environment variables / config`)
- [ ] `.gitignore` accurately ignores raw CSV data and temporary build files
- [ ] Units mapped correctly from `daily_units_2010_to_2019.csv` across pipeline
- [ ] Database ingestion verified (exact row count check: 500,324 rows)
- [ ] All 5 SQL scripts execute cleanly without errors
- [ ] All 4 charts generated successfully at 300 DPI with correct unit labels
- [ ] `README.md` is complete with clear setup instructions and embedded images

---

# Timeline

## Week 1: Core Pipeline & Database
- Days 1–2: Setup environment, explore CSV dataset & units file, write `extract.py` & `transform.py`
- Days 3–4: Design PostgreSQL schema, write `load.py`, execute batch loading for 500k rows
- Day 5: Validate database integrity and index performance

## Week 2: SQL Analysis, Visualization & Portfolio
- Days 6–7: Write and test 5 SQL analysis scripts (including window functions)
- Days 8–9: Create `visualize.py` and generate high-res matplotlib/seaborn charts with unit labels
- Days 10: Write `README.md`, perform code audit, and push project to GitHub

---

# Success Criteria

- Complete ETL execution: `Extract` -> `Transform` -> `Load` -> `Analyze` -> `Visualize`
- 500,324 weather rows successfully cleaned and loaded into PostgreSQL with parsed unit metadata
- 5 SQL query files answering specific weather analytics questions
- At least one advanced SQL window function (`DENSE_RANK()`, `AVG() OVER()`)
- 4 publication-grade visualization PNGs with explicit unit annotations
- Complete, impressive GitHub portfolio repository

---

# Future Enhancements

- **Automated Workflow Orchestration:** Schedule daily pipeline runs using Apache Airflow or Prefect.
- **Modern Data Stack Integration:** Use **dbt** for data transformations and unit validation tests within PostgreSQL.
- **Containerization:** Wrap PostgreSQL and Python ETL scripts in Docker & Docker Compose.
- **Interactive Dashboard:** Build a Streamlit or Metabase web application for interactive filtering across the 137 Philippine cities.
- **Live Weather API Ingestion:** Integrate Open-Meteo or PAGASA live APIs for real-time daily weather updates.
