from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from etls.postgres_etl import load_all_csv_to_postgres
from etls.mongodb_etl import process_podcast_data_mongo
from etls.aws_etl import upload_s3_pipeline, save_join_data_s3
from preprocessing.pre_postgres import create_fakedata_tables
from preprocessing.pre_redshift import create_redshift_tables, copy_data_to_redshift

# Define your DAG's default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 15),
    'email': ['npam5499l@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# Create the Airflow DAG
with DAG('podcast_summary',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:

        start = PythonOperator(
            task_id="start",
            python_callable = lambda: print("Jobs started"),
            dag=dag
        )

        join_data = PostgresOperator(
                task_id='join_data',
                postgres_conn_id = "postgres_conn",
                sql= '''SELECT c.customer_name,
                        c.age, 
                        c.address, 
                        c.phone, 
                        c.email, 
                        o.order_date, 
                        od.quantity, 
                        o.total_price 
                        FROM customer c 
                        JOIN orders o 
                        ON c.customer_id = o.customer_id 
                        JOIN orders_detail od 
                        ON o.order_id = od.order_id                                      
                ;
                '''
            )

        load_join_data = PythonOperator(
            task_id= 'load_join_data',
            python_callable=save_join_data_s3
            )

        end = PythonOperator(
            task_id="end",
            python_callable = lambda: print("Jobs completed successfully"),
            dag=dag
        )

        with TaskGroup(group_id = 'podcast_processing', tooltip= "Extract_podcast") as group_podcast:
            create_postgres_fakedata = PythonOperator(
                task_id='create_postgres_fakedata',
                python_callable=create_fakedata_tables,
                dag=dag
            )
            
            create_redshift = PythonOperator(
                task_id='create_redshift',
                python_callable=create_redshift_tables,
                dag=dag
            )
            
            copy_redshift = PythonOperator(
                task_id='copy_redshift',
                python_callable=copy_data_to_redshift,
                dag=dag
            )

            truncate_table = PostgresOperator(
                task_id='truncate_table',
                sql= ''' TRUNCATE TABLE Customer, Podcast, Order, Orders_Detail;
                    '''
            )

            upload_to_s3 = PythonOperator(
                task_id='upload_to_s3',
                python_callable=upload_s3_pipeline,
                dag=dag
            )


            load_files_postgres = PythonOperator(
                task_id='load_files_postgres',
                python_callable=load_all_csv_to_postgres,
                dag=dag
            )

            load_mongo = PythonOperator(
                task_id='load_mongo',
                python_callable=process_podcast_data_mongo,
                dag=dag
            )

    # Set task dependencies
            create_postgres_fakedata >> truncate_table >> load_files_postgres
            load_mongo
            upload_to_s3
            create_redshift >> copy_redshift
        start >> group_podcast >> join_data >> load_join_data >> end