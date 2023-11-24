from airflow import DAG

from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from preprocessing.pre_postgres import *
from etls.postgres_etl import *
from etls.mongodb_etl import *
from etls.podcast_etl import *

# Define your DAG's default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 15),
    'retries': 1,
}

# Create the Airflow DAG
dag = DAG(
    'load_data_all',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  
    catchup=False,
)


create_postgres_fakedata = PythonOperator(
    task_id='create_postgres_fakedata',
    python_callable=create_fakedata,
    dag=dag
)

load_postgres = PythonOperator(
    task_id='load_postgres',
    python_callable=load_csv_to_postgres,
    dag=dag
)

load_mongo = PythonOperator(
    task_id='load_mongo',
    python_callable=process_podcast_data,
    dag=dag
)



create_postgres_fakedata >> load_postgres
load_mongo

