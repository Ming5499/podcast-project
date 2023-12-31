import s3fs
from utils.constants import *
import pandas as pd
import datetime


def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(anon=False,
                               key=AWS_ACCESS_KEY_ID,
                               secret=AWS_ACCESS_KEY)
        return s3
    except Exception as e:
        print(e)
        
        
def create_bucket_if_not_exist(s3: s3fs.S3FileSystem, bucket: str):
    try:
        if not s3.exists(bucket):
            s3.mkdir(bucket)
            print("Bucket created")
        else:
            print("Bucket already exits")
    except Exception as e:
        print(e)
        
        
def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket: str, s3_file_name: str):
    try:
        s3.put(file_path, bucket +'/raw' + s3_file_name)
        print('File uploaded to s3')
    except FileNotFoundError:
        print('File not found')
    
    
def upload_s3_pipeline(ti):
    file_path = ti.xcom_pull(task_ids='truncate_table')
    
    s3 = connect_to_s3()
    create_bucket_if_not_exist(s3, AWS_BUCKET_NAME)
    upload_to_s3(s3, file_path, AWS_BUCKET_NAME, file_path.split('/')[-1])
    
    
    
def save_joined_data_s3(task_instance):
    data = task_instance.xcom_pull(task_ids="join_data")
    df = pd.DataFrame(data, columns = ['customer_name', 'age', 'address', 'phone', 'email', 'order_date', 'quantity','total_price'])
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'joined_weather_data_' + dt_string
    df.to_csv(f"s3://testing-ymlo/{dt_string}.csv", index=False)