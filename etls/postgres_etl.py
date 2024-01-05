import psycopg2
import csv
from utils.constants import *

db_params = {
    'host': DATABASE_HOST,
    'database': DATABASE_NAME,
    'user': DATABASE_USER,
    'password': DATABASE_PASSWORD,
}

#load CSV into PostgreSQL table
def load_csv_to_postgres(csv_file, table_name, conn, has_header=True):
    try:
        cursor = conn.cursor()
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            if has_header:
                next(file)  # Skip the header row
            cursor.copy_expert(f"COPY {table_name} FROM stdin CSV HEADER", file)
        conn.commit()
        print(f"Data from {csv_file} loaded into {table_name}")
    except Exception as e:
        print(f"Error loading data into {table_name}: {e}")
        


# Define the custom PythonOperator
def load_all_csv_to_postgres():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)

    csv_files = [
        ('data/fake_customer_data_batch_1.csv', 'Customer'),
        ('data/fake_podcast_data.csv', 'Podcast'),
        ('data/fake_orders_data_batch_1.csv', 'Orders'),
        ('data/fake_orders_detail_data.csv', 'Orders_Detail'),
    ]

    # Load CSV files into PostgreSQL tables
    for csv_file, table_name in csv_files:
        load_csv_to_postgres(csv_file, table_name, conn)

    conn.commit()
    print(f"Data from all CSV files loaded into their tables")

    if 'conn' in locals() and conn:
        conn.close()