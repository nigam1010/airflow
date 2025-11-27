import pandas as pd
import numpy as np
import json
import psycopg2
from psycopg2 import sql

# Read cleaned data
df = pd.read_csv('../data/data_jobs_cleaned.csv')

# Add industry column (will be filled later)
df['industry'] = None

# Convert boolean columns
df['job_work_from_home'] = df['job_work_from_home'].astype(str).map({'True': True, 'False': False})
df['job_no_degree_mention'] = df['job_no_degree_mention'].astype(str).map({'True': True, 'False': False})
df['job_health_insurance'] = df['job_health_insurance'].astype(str).map({'True': True, 'False': False})

# Read domain/industry data
domain = pd.read_csv('../data/company_domain.csv')
domain.columns = ['company_name', 'industry']

# Merge industry data
df = df.merge(domain, on='company_name', how='left', suffixes=('_x', ''))
if 'industry_x' in df.columns:
    df.drop('industry_x', axis=1, inplace=True)

# Normalize to 3NF form
# Replace single quotes with double quotes for JSON parsing
df['skill_type_json'] = df['job_type_skills'].str.replace("'", '"')

# Add job ID
df['jobid'] = range(1, len(df) + 1)

# Create skill type table by parsing JSON
skill_type_list = []
for idx, row in df.iterrows():
    jobid = row['jobid']
    try:
        skill_dict = json.loads(row['skill_type_json'])
        for skill_category, skills in skill_dict.items():
            if skills:  # Only process if skills list is not empty
                for skill in skills:
                    skill_type_list.append({
                        'jobid': jobid,
                        'skill_category': skill_category,
                        'skills': skill
                    })
    except json.JSONDecodeError:
        print(f"Error parsing JSON for jobid {jobid}")
        continue

skill_type_table = pd.DataFrame(skill_type_list)

# Handle multi-category skills
multiE = ["mongodb", "sas", "ruby", "firebase"]

# Remove mongodb/mongo from programming category (it's in databases)
skill_type_table = skill_type_table[
    ~((skill_type_table['skill_category'] == 'programming') & 
      (skill_type_table['skills'].isin(['mongodb', 'mongo'])))
]

# Rename ruby in webframeworks to ruby on rails
skill_type_table.loc[
    (skill_type_table['skill_category'] == 'webframeworks') & 
    (skill_type_table['skills'] == 'ruby'), 
    'skills'
] = 'ruby on rails'

# Rename sas in analyst_tools to sas tool
skill_type_table.loc[
    (skill_type_table['skill_category'] == 'analyst_tools') & 
    (skill_type_table['skills'] == 'sas'), 
    'skills'
] = 'sas tool'

# Rename firebase in cloud to firebase cloud
skill_type_table.loc[
    (skill_type_table['skill_category'] == 'cloud') & 
    (skill_type_table['skills'] == 'firebase'), 
    'skills'
] = 'firebase cloud'

# Remove duplicates
skill_type_table.drop_duplicates(inplace=True)

# Create unique skills table
skills_table = skill_type_table[['skills']].drop_duplicates().reset_index(drop=True)
skills_table.columns = ['skill']
skills_table['skill_id'] = range(1, len(skills_table) + 1)

# Create skill categories table
skill_categories = skill_type_table.merge(skills_table, left_on='skills', right_on='skill')[['skill_id', 'skill_category']].drop_duplicates()

# Create job-skill mapping
job_skill_mapping = skill_type_table.merge(skills_table, left_on='skills', right_on='skill')[['jobid', 'skill_id']].drop_duplicates()

# Create jobs table (without normalized fields)
jobs_table = df.drop(['job_skills', 'job_type_skills', 'skill_type_json', 'jobid'], axis=1)

print(f"Jobs table rows: {len(jobs_table)}")
print(f"Skills table rows: {len(skills_table)}")
print(f"Skill categories rows: {len(skill_categories)}")
print(f"Job-skill mapping rows: {len(job_skill_mapping)}")

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
    print("\nDatabase connection successful!")
    
    # ===== Create and populate jobpostings table =====
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename = 'jobpostings'
        );
    """)
    table_exists = cur.fetchone()[0]
    
    if table_exists:
        print("Table 'jobpostings' already exists.")
    else:
        cur.execute("""
            CREATE TABLE jobpostings (
                jobid SERIAL PRIMARY KEY,
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
                industry VARCHAR(1000)
            );
        """)
        conn.commit()
        print("Table 'jobpostings' created!")
    
    # Insert jobpostings data
    for index, row in jobs_table.iterrows():
        cur.execute("""
            INSERT INTO jobpostings (
                job_title_short, job_location, job_via, job_schedule_type,
                job_work_from_home, search_location, job_posted_date,
                job_no_degree_mention, job_health_insurance, job_country,
                salary_year_avg, company_name, industry
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    conn.commit()
    print(f"Inserted {len(jobs_table)} rows into 'jobpostings'")
    
    # ===== Create and populate skills_table =====
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename = 'skills_table'
        );
    """)
    table_exists = cur.fetchone()[0]
    
    if table_exists:
        print("Table 'skills_table' already exists.")
    else:
        cur.execute("""
            CREATE TABLE skills_table (
                skill VARCHAR(1000),
                skill_id INT PRIMARY KEY
            );
        """)
        conn.commit()
        print("Table 'skills_table' created!")
    
    # Insert skills_table data
    for index, row in skills_table.iterrows():
        cur.execute("""
            INSERT INTO skills_table (skill, skill_id)
            VALUES (%s, %s)
        """, (row['skill'], row['skill_id']))
    conn.commit()
    print(f"Inserted {len(skills_table)} rows into 'skills_table'")
    
    # ===== Create and populate skill_categories =====
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename = 'skill_categories'
        );
    """)
    table_exists = cur.fetchone()[0]
    
    if table_exists:
        print("Table 'skill_categories' already exists.")
    else:
        cur.execute("""
            CREATE TABLE skill_categories (
                skill_id INT PRIMARY KEY,
                skill_category VARCHAR(500)
            );
        """)
        conn.commit()
        print("Table 'skill_categories' created!")
    
    # Insert skill_categories data
    for index, row in skill_categories.iterrows():
        cur.execute("""
            INSERT INTO skill_categories (skill_id, skill_category)
            VALUES (%s, %s)
        """, (row['skill_id'], row['skill_category']))
    conn.commit()
    print(f"Inserted {len(skill_categories)} rows into 'skill_categories'")
    
    # ===== Create and populate job_skill_mapping =====
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename = 'job_skill_mapping'
        );
    """)
    table_exists = cur.fetchone()[0]
    
    if table_exists:
        print("Table 'job_skill_mapping' already exists.")
    else:
        cur.execute("""
            CREATE TABLE job_skill_mapping (
                jobid INT NOT NULL,
                skill_id INT NOT NULL,
                PRIMARY KEY (jobid, skill_id)
            );
        """)
        conn.commit()
        print("Table 'job_skill_mapping' created!")
    
    # Insert job_skill_mapping data
    for index, row in job_skill_mapping.iterrows():
        cur.execute("""
            INSERT INTO job_skill_mapping (jobid, skill_id)
            VALUES (%s, %s)
        """, (int(row['jobid']), int(row['skill_id'])))
    conn.commit()
    print(f"Inserted {len(job_skill_mapping)} rows into 'job_skill_mapping'")
    
    print("\n✓ All tables created and populated successfully!")
    
except psycopg2.Error as e:
    print(f"Database error: {e}")
    if conn:
        conn.rollback()
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
