import airflow
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.models.baseoperator import chain

from datetime import datetime

import os

# below step is necessary for airflow to know which userlist and webserver config to use
# export AIRFLOW_HOME=`pwd`/airflow do this in Project directory

# define default arguments
args = {
    'owner': 'vis_tmz',
    'start_date': airflow.utils.dates.days_ago(2),
    #'depends_on_past': False,
    #'start_date': datetime(2025, 1, 1),
    #'retries': 1,
}
# Initialize the DAG 
dag = DAG(
    dag_id='ds_jobs',
    default_args=args,
    schedule_interval='@daily',  # Run daily at midnight (change to '@weekly' or '0 0 * * 0' for weekly)
    # schedule_interval='0 0 28-31 * *',  # Uncomment this to run at month end
    catchup=False,  # Don't run for past dates
)
# Define the 4 tasks - Now using Python scripts instead of R
A = BashOperator(
    task_id='clean_data',
    bash_command='cd d:/yogpro/Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main/scripts && python clean_scraped_data.py',
    dag=dag,
    )
B = BashOperator(
    task_id='fill_domain',
    bash_command='cd d:/yogpro/Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main/scripts && python fill_domain.py',
    dag=dag,
    )
C = BashOperator(
    task_id='merge_push',
    bash_command='cd d:/yogpro/Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main/scripts && python merge_push_data_3nf.py',
    dag=dag,
    )
D = BashOperator(
    task_id='jupyter_notebook_report',
    bash_command='cd d:/yogpro/Improve-Your-Hiring-Chance-For-Data-Science-Related-Roles-main/scripts && jupyter nbconvert --to html --execute report_3nf.ipynb',
    dag=dag,
    )

# Define the task dependencies
chain(A, B, C, D)