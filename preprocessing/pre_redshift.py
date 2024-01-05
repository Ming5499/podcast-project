import boto3
import psycopg2
from utils.constants import *


def connect_to_redshift():
    redshift = boto3.client('redshift')
    response = redshift.describe_clusters()
    cluster_info = response['Clusters'][0]

    host = AWS_REDSHIFT_HOST
    database = AWS_REDSHIFT_DATABASE
    user = AWS_REDSHIFT_USER
    password = AWS_REDSHIFT_PASSWORD

    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    return conn


def create_redshift_tables():
    conn = connect_to_redshift()
    cur = conn.cursor()

    try:
        # Create the customer dimension table
        cur.execute('''
          CREATE TABLE IF NOT EXISTS dimCustomer (
            customer_id INT PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            age INT,
            address VARCHAR(100),
            phone VARCHAR(100),
            email VARCHAR(100)
          );
        ''')

        # Create the podcast dimension table
        cur.execute('''
          CREATE TABLE IF NOT EXISTS dimPodcast (
            podcast_id INT PRIMARY KEY,
            podcast_name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2)
          );
        ''')

        # Create the order fact table
        cur.execute('''
          CREATE TABLE IF NOT EXISTS factOrder (
            order_id INT PRIMARY KEY,
            customer_id INT NOT NULL,
            order_date DATE,
            total_price DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES dimCustomer(customer_id),
            FOREIGN KEY (podcast_id) REFERENCES dimPodcast(podcast_id)
          );
        ''')

        conn.commit()
        print("Tables created successfully")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating tables: {e}")
    finally:
        cur.close()
        conn.close()


def copy_data_to_redshift():
    conn = connect_to_redshift()
    cur = conn.cursor()

    try:
        # Copy the data from the customer table to the customer dimension table
        cur.execute('''
        COPY dimCustomer (customer_id, customer_name, age, address, phone, email)
        FROM STDIN;
        ''')
        with open('podcast-project/data/fake_customer_data_batch_1.csv', 'r') as f:
            cur.copy_from(f, 'dimCustomer', null='')

        # Copy the data from the podcast table to the podcast dimension table
        cur.execute('''
        COPY podcast_dim (podcast_id, podcast_name, price)
        FROM STDIN;
        ''')
        with open('podcast-project/data/fake_podcast_data.csv', 'r') as f:
            cur.copy_from(f, 'podcast_dim', null='')

        # Copy the data from the orders table to the order fact table
        cur.execute('''
        COPY order_fact (order_id, customer_id, order_date, total_price)
        FROM STDIN;
        ''')
        with open('podcast-project/data/fake_orders_detail_data.csv', 'r') as f:
            cur.copy_from(f, 'order_fact', null='')

        conn.commit()
        print("Data copied to Redshift successfully")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error copying data: {e}")
    finally:
        cur.close()
        conn.close()