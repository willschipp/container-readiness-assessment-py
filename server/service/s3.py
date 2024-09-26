from minio import Minio
from minio.error import S3Error

def save(file_path, bucket_name, object_name, url, key, secret, secure=False):
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

def get(file_path,bucket_name,object_name,url,key, secret, secure=False):
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

def getBuckets(url,key,secret,secure=False):
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

def listFiles(bucket_name,url,key,secret,secure=False):
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