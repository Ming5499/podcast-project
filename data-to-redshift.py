import boto3
import psycopg2

redshift = boto3.client('redshift')
response = redshift.describe_clusters()
cluster_info = response['Clusters'][0]

host = 'redshift-cluster-2.ctlwvzbuur6m.ap-north-1.redshift.amazonaws.com'
database = 'podcast'
user = 'anhminh'
password = 'Password123'

conn = psycopg2.connect(host=host, database=database, user=user, password=password)
cur = conn.cursor()
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