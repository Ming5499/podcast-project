import psycopg2
import csv
from utils.constants import *

db_params = {
    'host': 'localhost',
    'database': 'podcast',
    'user': 'postgres',
    'password': '123456',
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
try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)

    # Load CSV files into PostgreSQL tables
    load_csv_to_postgres('csv/fake_customer_data_batch_1.csv', 'Customer', conn)
    load_csv_to_postgres('csv/fake_podcast_data.csv', 'Podcast', conn)
    load_csv_to_postgres('csv/fake_orders_data_batch_1.csv', 'Orders', conn)
    load_csv_to_postgres('csv/fake_orders_detail_data.csv', 'Orders_Detail', conn)

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()

