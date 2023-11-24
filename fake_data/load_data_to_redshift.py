import boto3
import psycopg2
from preprocessing.pre_postgres import *
from utils.constants import *

redshift = boto3.client('redshift')
response = redshift.describe_clusters()
cluster_info = response['Clusters'][0]

host = DATABASE_HOST
database = 'podcast'
user = 'anhminh'
password = 'Password123'

conn = psycopg2.connect(host=host, database=database, user=user, password=password)
cur = conn.cursor()


# Copy the data from the customer table to the customer dimension table
cur.execute('''
COPY dimCustomer (customer_id, customer_name, age, address, phone, email)
FROM STDIN;
''')

with open('customer.csv', 'r') as f:
    cur.copy_from(f, 'dimCustomer', null='')

# Copy the data from the podcast table to the podcast dimension table
cur.execute('''
COPY podcast_dim (podcast_id, podcast_name, price)
FROM STDIN;
''')

with open('podcast.csv', 'r') as f:
    cur.copy_from(f, 'podcast_dim', null='')

# Copy the data from the orders table to the order fact table
cur.execute('''
COPY order_fact (order_id, customer_id, order_date, total_price)
FROM STDIN;
''')

with open('orders.csv', 'r') as f:
    cur.copy_from(f, 'order_fact', null='')