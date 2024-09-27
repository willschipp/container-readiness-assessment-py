from minio import Minio
from minio.error import S3Error

def save_file(file_path, bucket_name, object_name, url, key, secret, secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:        
        if not client.bucket_exists(bucket_name):            
            client.make_bucket(bucket_name)

        result = client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,            
        )
        return result
    except S3Error as err:
        print("error ", err)

def get_file(file_path,bucket_name,object_name,url,key, secret, secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:
        client.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path)
    except S3Error as err:
        print("error ", err)

def get_buckets(url,key,secret,secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:
        buckets = client.list_buckets()
        # loop and turn into a list to return
        bucket_names = []
        for bucket in buckets:
            bucket_names.append(bucket.name)

        return bucket_names
    except S3Error as err:
        print("error ",err)      

def list_files(bucket_name,url,key,secret,secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )
    try:
        files = client.list_objects(bucket_name,recursive=True)
        # loop and turn into a list to return
        file_names = []
        for file in files:
            file_names.append(file.object_name)

        return file_names
    except S3Error as err:
        print("error ",err)

def clean_up(url,key,secret,secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )
    try:
        buckets = client.list_buckets()
        # loop and turn into a list to return
        for bucket in buckets:
            files = client.list_objects(bucket.name,recursive=True)
            for file in files:
                client.remove_object(bucket.name,file.object_name)
            client.remove_bucket(bucket.name)
    except S3Error as err:
        print("error ",err)

def create_bucket(bucket_name,url,key,secret,secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:        
        if not client.bucket_exists(bucket_name):            
            client.make_bucket(bucket_name)
    except S3Error as err:
        print("error ",err)            
