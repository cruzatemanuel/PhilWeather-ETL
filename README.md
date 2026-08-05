# PhilWeather ETL

## Setup Instructions

### 1. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Create PostgreSQL Database
```bash
createdb philweather_db
# Or via psql: CREATE DATABASE philweather_db;
```

### 5. Test Database Connection
```bash
python scripts/test_connection.py
```