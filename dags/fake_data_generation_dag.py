import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from etls.fake_data_batch import *
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 9, 15),
    'depends_on_past': False,
    'retries': 1,
}
dag = DAG(
    'fake_data_generation',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  
    schedule_interval=None,
)


generate_fake_customer_data = PythonOperator(
    task_id='generate_fake_customer_data',
    python_callable=generate_fake_customer_data,
    op_kwargs={'batch_size': 20000, 'num_batches': 5},
    dag=dag
)

generate_fake_order_data = PythonOperator(
    task_id='generate_fake_order_data',
    python_callable=generate_fake_order_data,
    op_kwargs={'batch_size': 20000, 'num_batches': 5},
    dag=dag
)

generate_fake_podcast_data = PythonOperator(
    task_id='generate_fake_podcast_data',
    python_callable=generate_fake_podcast_data,
    op_kwargs={'max_podcast_id': 50, 'titles_file_path': 'data/titles.csv', 'output_file_path': 'data/fake_podcast_data.csv'},
    dag=dag
)

generate_fake_orders_detail_data = PythonOperator(
    task_id='generate_fake_orders_detail_data',
    python_callable=generate_fake_orders_detail_data,
    op_kwargs={'max_order_id': 20000, 'max_podcast_id': 50, 'output_file_path': 'data/fake_orders_detail_data.csv'},
    dag=dag
)

generate_fake_customer_data >> generate_fake_order_data >> generate_fake_podcast_data >> generate_fake_orders_detail_data