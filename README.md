# Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles

## Overview
This project is designed to help data science job aspirants improve their hiring chances by analyzing job postings, salary trends, and in-demand skills. It leverages SQL queries to extract insights from a PostgreSQL database and uses Python scripts for data cleaning, merging, and normalization workflows.

## Project Structure
- **scripts/**
  - **clean_scraped_data.py**: Cleans raw scraped job data using pandas.
  - **fill_domain.py**: Uses OpenAI API to identify company industries/domains.
  - **merge_push_data.py**: Merges cleaned data and pushes it to the "jobs" table.
  - **merge_push_data_3nf.py**: Normalizes data into Third Normal Form (3NF) and updates related tables.
  - **report_3nf.ipynb**: Jupyter notebook with interactive visualizations and analysis.
  - **query_commands.sql**: Contains SQL queries for data insights and reporting.
- **dags/**
  - **dsjobs_dag.py**: Apache Airflow DAG for orchestrating the ETL pipeline.
- **data/**: Stores raw and cleaned CSV data.
- **output/**: Contains generated visualizations and reports.
- **README.md**: Provides project documentation and usage instructions.

## Workflow
1. Run `clean_scraped_data.py` to preprocess and clean the raw data.
2. Execute `fill_domain.py` to enrich data with company industry information using OpenAI API.
3. Run `merge_push_data_3nf.py` to normalize the data into job postings, skills, skill categories, and job-skill mapping tables.
4. Open and execute `report_3nf.ipynb` to generate interactive visualizations and analysis reports.
5. Optionally, use Apache Airflow to automate the entire pipeline via `dsjobs_dag.py`.

## Requirements
- **PostgreSQL Database** ("ds_jobs")
- **Python 3.8+** with packages listed in `requirements.txt`:
  - pandas
  - numpy
  - psycopg2-binary
  - sqlalchemy
  - matplotlib
  - seaborn
  - plotly
  - openai
  - jupyter
  - apache-airflow (optional)
- **CSV data files** in the **data/** folder

## Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
createdb ds_jobs
```

## Usage

### Method 1: Manual Execution
Run scripts sequentially:
```bash
cd scripts
python clean_scraped_data.py
python fill_domain.py
python merge_push_data_3nf.py
jupyter notebook report_3nf.ipynb
```

### Method 2: Airflow Automation
```bash
# Set Airflow home directory
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize Airflow (first time only)
airflow db init

# Start Airflow scheduler and webserver
airflow scheduler &
airflow webserver

# Trigger the DAG
airflow dags trigger ds_jobs
```

## Database Schema (3NF)
- **jobpostings**: Core job posting information (job title, location, salary, company, etc.)
- **skills_table**: Unique list of skills with skill_id
- **skill_categories**: Maps skills to categories (programming, databases, cloud, etc.)
- **job_skill_mapping**: Many-to-many relationship between jobs and skills

## Analysis Features
The project answers 5 key questions:
1. **What are the main technologies?** - Top 20 most in-demand skills
2. **What is the median salary for each job title?** - Salary benchmarking by role
3. **Which industry fields are hiring?** - Industry distribution analysis
4. **How does location relate to salary?** - Geographic salary trends
5. **Does remote work pay less?** - Remote vs on-site salary comparison

## Visualizations
All visualizations are saved to `output/`:
- `top20_skills.png` - Most in-demand skills
- `top10_skill_cat.png` - Skills by category
- `med_salary_role.png` - Median salaries by role
- `top20skill_salary_cat.png` - Skills vs salary analysis
- `map.png` - Geographic distribution (if geocoding enabled)

## Tech Stack
- **Language**: Python 3.8+
- **Data Processing**: pandas, numpy
- **Database**: PostgreSQL, psycopg2, SQLAlchemy
- **Visualization**: matplotlib, seaborn, plotly
- **AI Enhancement**: OpenAI GPT-4o-mini API
- **Orchestration**: Apache Airflow
- **Reporting**: Jupyter Notebook

## Configuration
Update database credentials in Python scripts:
```python
DB_CONFIG = {
    'dbname': 'ds_jobs',
    'user': 'postgres',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432
}
```

Update OpenAI API key in `fill_domain.py`:
```python
client = OpenAI(api_key="your_api_key_here")
```

## License
This project is provided as-is for educational and analytical purposes.