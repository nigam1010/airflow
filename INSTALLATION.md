# Installation Instructions

## All visual errors have been fixed!

The remaining "import could not be resolved" warnings are expected and will disappear once you install the required packages.

## Quick Setup

### 1. Install Python dependencies:
```powershell
pip install -r requirements.txt
```

### 2. Set up PostgreSQL database:
```powershell
# Create the database (if psql is installed)
createdb ds_jobs

# Or using pgAdmin or SQL:
# CREATE DATABASE ds_jobs;
```

### 3. Update database credentials (if needed):
Edit these files and update the password:
- scripts/merge_push_data.py
- scripts/merge_push_data_3nf.py
- scripts/report_3nf.ipynb

Change:
```python
DB_PASSWORD = "muix7pcj"  # <- Update this
```

### 4. Update OpenAI API key:
Edit `scripts/fill_domain.py` and update:
```python
client = OpenAI(api_key="your_actual_api_key_here")
```

## Run the Project

### Option 1: Run scripts manually
```powershell
cd scripts
python clean_scraped_data.py
python fill_domain.py
python merge_push_data_3nf.py
jupyter notebook report_3nf.ipynb
```

### Option 2: Use Airflow (automated)
```powershell
# Set environment variable
$env:AIRFLOW_HOME = "$(pwd)/airflow"

# Initialize (first time only)
airflow db init
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Start Airflow
airflow scheduler &
airflow webserver

# Trigger the DAG via web UI at http://localhost:8080
```

## ✅ All Code Issues Fixed:
- Variable initialization errors in merge_push_data.py - FIXED
- Variable initialization errors in merge_push_data_3nf.py - FIXED
- Matplotlib import issues in notebook - FIXED
- FuncFormatter usage in notebook - FIXED
- Unused imports warnings - FIXED

The project is now ready to run once you install the dependencies!
