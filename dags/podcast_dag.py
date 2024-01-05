from airflow import DAG

from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from etls.podcast_etl import create_database, get_episodes, load_episodes, download_episodes


# Define your DAG's default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 15),
    'retries': 1,
}

# Create the Airflow DAG
dag = DAG(
    'podcast_summary',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  
    catchup=False,
)

# Define tasks 
create_database = PythonOperator(
    task_id='create_database',
    python_callable=create_database,
    dag=dag,
)

get_episodes = PythonOperator(
    task_id='get_episodes',
    python_callable=get_episodes,
    dag=dag,
)

load_episodes = PythonOperator(
    task_id='load_episodes',
    python_callable=load_episodes,
    op_args=['podcast_episodes'],
    dag=dag,
)

download_episodes = PythonOperator(
    task_id='download_episodes_task',
    python_callable=download_episodes,
    op_args=[get_episodes.output], 
    dag=dag,
)


# Set task dependencies
create_database >> get_episodes >> [load_episodes, download_episodes] 

