import pandas as pd
import psycopg2
from psycopg2 import sql

# Read cleaned data
df = pd.read_csv('../data/data_jobs_cleaned.csv')

# Add industry column (will be filled later)
df['industry'] = None

# Convert boolean columns
df['job_work_from_home'] = df['job_work_from_home'].map({'True': True, 'False': False})
df['job_no_degree_mention'] = df['job_no_degree_mention'].map({'True': True, 'False': False})
df['job_health_insurance'] = df['job_health_insurance'].map({'True': True, 'False': False})

# Read domain/industry data
domain = pd.read_csv('../data/company_domain.csv')
domain.columns = ['company_name', 'industry']

# Merge industry data
df = df.merge(domain, on='company_name', how='left', suffixes=('_x', ''))
if 'industry_x' in df.columns:
    df.drop('industry_x', axis=1, inplace=True)

# Database connection parameters
DB_PASSWORD = "tiger"
DB_CONFIG = {
    'dbname': 'ds_jobs',
    'user': 'postgres',
    'password': DB_PASSWORD,
    'host': 'localhost',
    'port': 5432
}

# Connect to database
conn = None
cur = None
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    print("Database connection successful!")
    
    # Check if table exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename = 'jobs'
        );
    """)
    table_exists = cur.fetchone()[0]
    
    if table_exists:
        print("Table 'jobs' already exists in the database.")
    else:
        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE jobs (
                id SERIAL PRIMARY KEY,
                job_title_short VARCHAR(100),
                job_location VARCHAR(1000),
                job_via VARCHAR(500),
                job_schedule_type VARCHAR(500),
                job_work_from_home BOOLEAN,
                search_location VARCHAR(1000),
                job_posted_date TIMESTAMP,
                job_no_degree_mention BOOLEAN,
                job_health_insurance BOOLEAN,
                job_country VARCHAR(300),
                salary_year_avg INT,
                company_name VARCHAR(1000),
                job_skills VARCHAR(3000),
                job_type_skills VARCHAR(5000),
                industry VARCHAR(1000)
            );
        """)
        conn.commit()
        print("Table 'jobs' created successfully!")
    
    # Insert data into table
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO jobs (
                job_title_short, job_location, job_via, job_schedule_type,
                job_work_from_home, search_location, job_posted_date,
                job_no_degree_mention, job_health_insurance, job_country,
                salary_year_avg, company_name, job_skills, job_type_skills, industry
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['job_title_short'], row['job_location'], row['job_via'],
            row['job_schedule_type'], row['job_work_from_home'],
            row['search_location'], row['job_posted_date'],
            row['job_no_degree_mention'], row['job_health_insurance'],
            row['job_country'], row['salary_year_avg'], row['company_name'],
            row['job_skills'], row['job_type_skills'], row['industry']
        ))
    
    conn.commit()
    print(f"Successfully inserted {len(df)} rows into 'jobs' table!")
    
    # Verify insertion
    cur.execute("SELECT COUNT(*) FROM jobs;")
    count = cur.fetchone()[0]
    print(f"Total rows in 'jobs' table: {count}")
    
except psycopg2.Error as e:
    print(f"Database error: {e}")
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
