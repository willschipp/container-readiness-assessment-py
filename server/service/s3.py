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