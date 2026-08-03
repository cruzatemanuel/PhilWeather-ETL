# PhilWeather Analytics Roadmap

## Project Goal

Build a small, portfolio-ready ETL project that demonstrates fundamental Data Engineering skills by processing Philippine weather data from a CSV dataset.

The finished project should:

- Read a real-world weather dataset (PSA/PAGASA)
- Clean and transform the data using pandas
- Load the cleaned data into PostgreSQL
- Perform SQL analysis
- Generate charts using matplotlib
- Document the project professionally on GitHub

**Target Completion:** 2 Weeks

---

# Tech Stack

- Python
- pandas
- PostgreSQL
- SQLAlchemy
- SQL
- matplotlib
- Git
- GitHub

---

# Project Structure

```text
philweather-analytics/

├── data/
│   ├── raw/
│   └── cleaned/
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── visualize.py
│
├── sql/
│   ├── query_01.sql
│   ├── query_02.sql
│   ├── query_03.sql
│   ├── query_04.sql
│   └── query_05.sql
│
├── charts/
│
├── notebooks/
│
├── README.md
├── ROADMAP.md
├── requirements.txt
└── .gitignore
```

---

# Project Workflow

```text
PSA / PAGASA CSV
        │
        ▼
Python
(Read CSV)
        │
        ▼
pandas
(Clean Data)
        │
        ▼
PostgreSQL
(Load Data)
        │
        ▼
SQL Analysis
        │
        ▼
matplotlib Charts
        │
        ▼
GitHub Portfolio
```

---

# Phase 1 — Project Setup

## Objective

Prepare the development environment and repository.

## Tasks

- Create GitHub repository
- Create project folder structure
- Create Python virtual environment
- Install dependencies
- Configure PostgreSQL database
- Create `.gitignore`
- Create `requirements.txt`

## Deliverables

- Working repository
- Virtual environment
- PostgreSQL database
- Initial Git commit

---

# Phase 2 — Data Exploration

## Objective

Understand the dataset before writing code.

## Tasks

- Download PSA/PAGASA CSV dataset
- Review documentation (if available)
- Identify columns
- Identify data types
- Check missing values
- Check duplicate rows
- Determine required transformations

## Deliverables

- Data exploration notes
- Initial understanding of the dataset

---

# Phase 3 — Extract

## Objective

Read the raw dataset into Python.

## Tasks

- Create `extract.py`
- Load CSV with pandas
- Validate file path
- Display dataset information
- Save exploration outputs if needed

## Deliverables

- Working extraction script

---

# Phase 4 — Transform

## Objective

Clean and prepare the dataset for analysis.

## Tasks

- Remove duplicates
- Handle missing values
- Rename columns
- Convert data types
- Parse dates
- Standardize column names
- Validate cleaned data
- Export cleaned CSV

## Deliverables

- Clean dataset
- `transform.py`

---

# Phase 5 — Load

## Objective

Load the cleaned dataset into PostgreSQL.

## Tasks

- Create database connection
- Configure SQLAlchemy
- Create weather table
- Load cleaned data
- Verify row count
- Validate imported records

## Deliverables

- Populated PostgreSQL table
- `load.py`

---

# Phase 6 — SQL Analysis

## Objective

Answer analytical questions using SQL.

## Required Queries

### Query 1

Top 10 hottest locations

### Query 2

Average rainfall by province

### Query 3

Monthly average temperature

### Query 4

Highest recorded rainfall

### Query 5

Window Function

Use one of:

- `RANK()`
- `ROW_NUMBER()`
- `DENSE_RANK()`

Example:

Rank provinces by average temperature.

## Deliverables

- Five SQL query files

---

# Phase 7 — Data Visualization

## Objective

Create charts from the analyzed data.

## Required Charts

### Chart 1

Monthly Temperature Trend

(Line Chart)

### Chart 2

Average Rainfall by Province

(Bar Chart)

### Chart 3

Top 10 Hottest Locations

(Horizontal Bar Chart)

## Deliverables

- Three PNG charts
- `visualize.py`

---

# Phase 8 — Documentation

## Objective

Create a professional GitHub repository.

## README Sections

- Project Overview
- Dataset
- Tech Stack
- ETL Workflow
- Database Schema
- SQL Analysis
- Charts
- Key Findings
- Future Improvements
- Installation Guide
- How to Run

## Key Findings

Document at least three meaningful insights discovered through the analysis.

---

# Phase 9 — Final Review

## Objective

Prepare the repository for publication.

## Checklist

- Code follows PEP 8
- Repository is organized
- No unused files
- SQL queries tested
- Charts generated
- README completed
- `.gitignore` configured
- No credentials committed
- Requirements file updated
- Git history is clean

---

# Timeline

## Week 1

- Project setup
- Dataset selection
- Data exploration
- Extract
- Transform
- Load into PostgreSQL

## Week 2

- SQL analysis
- Charts
- README
- Repository cleanup
- Final testing
- Push to GitHub

---

# Success Criteria

By the end of this project, the repository should include:

- A real-world Philippine weather dataset
- Python ETL scripts
- PostgreSQL database integration
- Five SQL analysis queries
- At least one window function
- Three matplotlib charts
- A professional README
- Clean project structure
- Meaningful analytical findings

---

# Future Enhancements

Once this project is complete, future versions could include:

- Scheduled ETL with Apache Airflow
- Data transformations with dbt
- Docker containerization
- Interactive dashboards (Metabase)
- Live weather API ingestion
- Data quality testing
- CI/CD with GitHub Actions
- Cloud deployment

These enhancements are intentionally out of scope for Version 1 to keep the project focused, achievable, and portfolio-ready within two weeks.
