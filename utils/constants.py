import configparser

parser = configparser.ConfigParser()
parser.read('/config/config.conf')

#MongoDB
MONGODB_HOST = parser.get('mongo', 'database_host')
MONGODB_PORT = parser.get('mongo', 'database_port')

#Postgres
DATABASE_HOST =  parser.get('database', 'database_host')
DATABASE_NAME =  parser.get('database', 'database_name')
DATABASE_PORT =  parser.get('database', 'database_port')
DATABASE_USER =  parser.get('database', 'database_username')
DATABASE_PASSWORD =  parser.get('database', 'database_password')

#AWS
AWS_ACCESS_KEY_ID = parser.get('aws', 'aws_access_key_id')
AWS_ACCESS_KEY = parser.get('aws', 'aws_secret_access_key')
AWS_REGION = parser.get('aws', 'aws_region')
AWS_BUCKET_NAME = parser.get('aws', 'aws_bucket_name')
AWS_REDSHIFT_HOST = parser.get('aws', 'aws_redshift_host')
AWS_REDSHIFT_DATABASE = parser.get('aws', 'aws_redshift_database')
AWS_REDSHIFT_USER = parser.get('aws', 'aws_redshift_database')
AWS_REDSHIFT_PASSWORD = parser.get('aws', 'aws_redshift_database')



INPUT_PATH = parser.get('file_paths', 'input_path')
OUTPUT_PATH = parser.get('file_paths', 'output_path')



