import io
from minio import Minio
from minio.error import S3Error

# helper function for names
def filter_names_with_content_after_backslash(names):
    return [name for name in names if '/' in name and name.split('/')[-1]]

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

def create_folder(bucket_name,folder_name,url,key,secret,secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:        
        if not client.bucket_exists(bucket_name):
            raise NameError("bucket doesn't exist")
            return
        client.put_object(bucket_name,folder_name + '/', io.BytesIO(b''),0)
    except S3Error as err:
        print("error ",err)         

def list_folder_files(bucket_name,folder_name,url,key,secret,secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:
        objects = client.list_objects(bucket_name,prefix=folder_name,recursive=True)
        file_names = []
        for object in objects:
            file_names.append(object.object_name)
        # filter
        file_names = filter_names_with_content_after_backslash(file_names)
        return file_names
    except S3Error as err:
        print("error ",err)


def save_file_in_folder(file_path, folder_name, bucket_name, object_name, url, key, secret, secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:        
        if not client.bucket_exists(bucket_name):            
            client.make_bucket(bucket_name)

        # append the folder name to the object name
        save_name = folder_name + '/' + object_name

        result = client.fput_object(
            bucket_name=bucket_name,
            object_name=save_name,
            file_path=file_path,            
        )
        return result
    except S3Error as err:
        print("error ", err)    

