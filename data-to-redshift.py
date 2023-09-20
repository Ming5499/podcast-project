import boto3
import psycopg2

redshift = boto3.client('redshift')
response = redshift.describe_clusters()
cluster_info = response['Clusters'][0]

host = 'redshift-cluster-2.ctlwvzbuur6m.ap-south-1.redshift.amazonaws.com'
database = 'podcast'
user = 'anhminh'
password = 'Password123'

conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)