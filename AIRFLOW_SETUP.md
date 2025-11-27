# Apache Airflow Setup Guide

This guide will help you set up Apache Airflow to automatically run the data pipeline on a schedule.

## What is Airflow?

Apache Airflow is a workflow orchestration tool that will automatically run your data pipeline (clean data → fill domain → load to database → generate report) on a schedule.

## Installation Steps

### 1. Install Airflow

```powershell
# Install Apache Airflow
pip install apache-airflow

# Install PostgreSQL provider for Airflow
pip install apache-airflow-providers-postgres
```

### 2. Initialize Airflow

```powershell
# Set Airflow home directory (run this from project root)
$env:AIRFLOW_HOME = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\airflow"

# Create the directory
New-Item -ItemType Directory -Force -Path $env:AIRFLOW_HOME

# Initialize the Airflow database
airflow db init
```

### 3. Create Airflow User

```powershell
# Create an admin user
airflow users create `
    --username admin `
    --firstname Admin `
    --lastname User `
    --role Admin `
    --email admin@example.com `
    --password admin
```

### 4. Configure DAGs Folder

```powershell
# Copy the DAG file to Airflow's dags folder
Copy-Item "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\dags\dsjobs_dag.py" `
    -Destination "$env:AIRFLOW_HOME\dags\" -Force
```

Or update `airflow.cfg` to point to your dags folder:
```
dags_folder = d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\dags
```

### 5. Start Airflow

Open **two separate PowerShell terminals**:

**Terminal 1 - Start the Web Server:**
```powershell
$env:AIRFLOW_HOME = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\airflow"
airflow webserver --port 8080
```

**Terminal 2 - Start the Scheduler:**
```powershell
$env:AIRFLOW_HOME = "d:\yogpro\Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main\airflow"
airflow scheduler
```

### 6. Access Airflow UI

1. Open your browser and go to: **http://localhost:8080**
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. Find the `ds_jobs` DAG in the list
4. Toggle it **ON** to enable automatic scheduling

## Current Schedule

The DAG is currently set to run **daily at midnight**. 

### To Change the Schedule:

Edit `dags/dsjobs_dag.py` and change the `schedule_interval`:

```python
# Common schedules:
schedule_interval='@daily',        # Every day at midnight
schedule_interval='@weekly',       # Every Sunday at midnight
schedule_interval='@monthly',      # First day of month at midnight
schedule_interval='0 9 * * 1',     # Every Monday at 9 AM
schedule_interval='0 0 * * 0',     # Every Sunday at midnight
schedule_interval='0 0 1 * *',     # First day of every month
```

## Pipeline Tasks

The DAG runs 4 tasks in sequence:

1. **clean_data** - Cleans the raw job posting data
2. **fill_domain** - Fills company industry information using OpenAI API
3. **merge_push** - Normalizes data to 3NF and loads into PostgreSQL
4. **jupyter_notebook_report** - Generates HTML report with visualizations

## Important Notes

### Set OpenAI API Key

Before running, set your OpenAI API key as an environment variable:

```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

To make it permanent, add it to your system environment variables.

### Manual Trigger

You can also manually trigger the DAG from the Airflow UI:
1. Click on the `ds_jobs` DAG
2. Click the **Play** button (▶) on the top right
3. Select "Trigger DAG"

## Troubleshooting

### DAG not showing up?
- Make sure the scheduler is running
- Check that the DAG file is in the correct `dags` folder
- Refresh the Airflow UI page

### Tasks failing?
- Check the logs in the Airflow UI by clicking on the failed task
- Verify PostgreSQL is running
- Ensure all Python dependencies are installed
- Check that file paths are correct

### Stop Airflow
Press `Ctrl+C` in both terminal windows (webserver and scheduler)

## Production Tips

For production use:
1. Use a proper database (PostgreSQL) instead of SQLite for Airflow metadata
2. Set up proper authentication
3. Configure email alerts for task failures
4. Use environment variables for sensitive data
5. Consider using Docker for deployment
