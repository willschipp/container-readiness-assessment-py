import io

from loguru import logger

# s3 libraries
from minio import Minio
from minio.error import S3Error

from server.configuration import settings

# logger = logging.getLogger("service.s3")

s3_client = Minio(
    endpoint=settings.s3_url,
    access_key=settings.s3_access_key_id,
    secret_key=settings.s3_secret_access_key,
    secure=False,
)

def get_file_names_from_object_names(object_names: list, prefix: bool = False) -> list:
    file_names = []
    if prefix:
        file_names = [  
            name.split("/")[1] for name in object_names if not name.endswith("/")
        ]
    else:
        file_names = [  # 'test.json'
            name.split("/")[0] for name in object_names if not name.endswith("/")
        ]
    return file_names

def get_folder_names_from_object_names(object_names: list) -> list:
    folder_names = [name.split("/")[0] for name in object_names if name.endswith("/")]
    return folder_names


# helper function for names
def filter_names_with_content_after_backslash(names):
    return [name.split('/')[1] for name in names if '/' in name and name.split('/')[-1]]

def filter_names_with_no_content_after_backslash(names):
    return [name for name in names if '/' not in name or not name.split('/')[-1]]

def put_file(file_path: str, object_name: str, bucket_name=None) -> object:
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(
        f"bucket_name={bucket_name}, file_path={file_path}, object_name={object_name}"
    )

    try:
        create_bucket(bucket_name)

        result = s3_client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
        )
        logger.debug(
            "Created {0} object; etag: {1}, version-id: {2}".format(
                result.object_name,
                result.etag,
                result.version_id,
            ),
        )

        return result
    except Exception as err:
        logger.error(err)
        raise err



def get_file(object_name, file_path, bucket_name=None):
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(
        f"bucket_name={bucket_name}, object_name={object_name}, file_path={file_path}"
    )

    try:
        s3_client.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
        )
    except Exception as err:
        logger.error(err)
        raise err      

def list_buckets() -> list:
    try:
        buckets = s3_client.list_buckets()

        bucket_names = []
        for bucket in buckets:
            bucket_names.append(bucket.name)
        logger.debug(f"bucket_names={bucket_names}")

        return bucket_names
    except Exception as err:
        logger.error(err)
        raise err


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
    except Exception as err:
        logger.error("get_buckets " + err.args[0])         

def list_files(bucket_name=None) -> list:
    """
    Retrieves a list of file names from a S3 bucket at root level.

    object_names=['test.json', '71895f5cdd754eba9b276202f4a734b2/', 'c9421a00ea0e4123bfee492a9517f285/', 'c94a88ebcdf3413a8b24cef4eba2c107/']
    file_names=['test.json']

    Args:
        bucket_name (str, optional): The name of the S3 bucket. Defaults to settings.s3_bucket_name.

    Returns:
        list: A list of file names.

    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}")

    try:
        objects = s3_client.list_objects(bucket_name=bucket_name, recursive=False)

        object_names = []
        object_count = 0
        for object in objects:
            object_count += 1
            logger.debug(
                f"object_count={object_count}, object_name={object.object_name}"
            )
            object_names.append(object.object_name)

        return get_file_names_from_object_names(object_names)
    except Exception as err:
        logger.error(err)
        raise err

def remove_file(object_name, bucket_name=None):
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}, object_name={object_name}")

    try:
        s3_client.remove_object(
            bucket_name=bucket_name,
            object_name=object_name,
        )
        logger.debug(f"object_name={object_name} removed")
    except Exception as err:
        logger.error(err)
        raise err


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
    except Exception as err:
        logger.error("clean_up " + err.args[0])      


def create_bucket(bucket_name=None):
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}")

    try:
        if not s3_client.bucket_exists(bucket_name):
            s3_client.make_bucket(bucket_name)
            logger.debug(f"bucket_name={bucket_name} created")
        else:
            logger.debug(f"bucket_name={bucket_name} found")
    except Exception as err:
        logger.error(err)
        raise err

def put_folder(folder_name, bucket_name=None):
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}, folder_name={folder_name}")

    try:
        if not s3_client.bucket_exists(bucket_name):
            raise NameError(f"bucket_name={bucket_name} not found")

        s3_client.put_object(bucket_name, folder_name + "/", io.BytesIO(b""), 0)

        logger.debug(f"folder_name={folder_name} created")
    except Exception as err:
        logger.error(err)
        raise err

def list_folders(bucket_name=None) -> list:
    """
    Retrieves a list of folders in a S3 bucket at root level.

    Args:
        bucket_name (str, optional): The name of the bucket. Defaults to settings.s3_bucket_name.

    Returns:
        list: A list of folder names.

    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}")

    try:
        objects = s3_client.list_objects(bucket_name=bucket_name, recursive=False)

        object_names = []
        object_count = 0
        for object in objects:
            object_count += 1
            logger.debug(
                f"object_count={object_count}, object_name={object.object_name}"
            )
            object_names.append(object.object_name)

        folder_names = get_folder_names_from_object_names(object_names)
        logger.debug(f"folder_names={folder_names}")
        return folder_names
    except Exception as err:
        logger.error(err)
        raise err


def remove_folder(prefix, bucket_name=None):
    """
    Empties and removes a folder from a S3 bucket.

    Args:
        prefix (str): Prefix of the folder to create.
        bucket_name (str, optional): The name of the S3 bucket. Defaults to settings.s3_bucket_name.

    Raises:
        NameError: If the specified bucket does not exist.
        Exception: If an error occurs during the creation of the folder.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}, prefix={prefix}")

    try:
        if not s3_client.bucket_exists(bucket_name):
            raise NameError(f"bucket_name={bucket_name} not found")

        objects = s3_client.list_objects(bucket_name, prefix=prefix, recursive=True)
        for object in objects:
            s3_client.remove_object(bucket_name, object.object_name)
            logger.debug(f"object_name={object.object_name} removed")
    except Exception as err:
        logger.error(err)
        raise err


def put_file_to_folder(file_path, prefix, file_name, bucket_name=None) -> object:
    """
    Puts a file in a specified folder in an S3 bucket.

    Args:
        file_path (str): The path to the file.
        prefix (str): The prefix of the folder in the S3 bucket.
        file_name (str): The name of the file.
        bucket_name (str, optional): The name of the S3 bucket. Defaults to settings.s3_bucket_name.

    Returns:
        object: The result of the file upload.

    Raises:
        Exception: If an error occurs during the file upload.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(
        f"bucket_name={bucket_name}, file_path={file_path}, prefix={prefix}, file_name={file_name}"
    )

    try:
        create_bucket(bucket_name)

        object_name = f"{prefix}/{file_name}"
        logger.debug(f"Put object_name={object_name}")

        # Save object data from file_path
        return s3_client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
        )
    except Exception as err:
        logger.error(err)
        raise err


def is_file_in_folder(prefix, file_name, bucket_name=None):
    """
    Check if a file exists in a folder in an S3 bucket.

    Args:
        prefix (str): The prefix of the folder in the S3 bucket.
        file_name (str): The name of the file.
        bucket_name (str, optional): The name of the S3 bucket. Defaults to settings.s3_bucket_name.

    Returns:
        bool: True if the file exists, False otherwise.

    Raises:
        S3Error: If an S3 error occurs.
        Exception: If an error occurs.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}, prefix={prefix}, file_name={file_name}")

    try:
        # Get object information
        object_name = f"{prefix}/{file_name}"
        s3_client.stat_object(bucket_name=bucket_name, object_name=object_name)
        logger.debug(f"object_name={object_name} found")
        return True
    except S3Error as err:
        if err.code == "NoSuchKey":
            logger.debug(f"object_name={object_name} not found")
            return False
        else:
            logger.debug(err)
            raise err
    except Exception as err:
        logger.debug(err)
        raise err


def get_file_from_folder(prefix, file_name, file_path, bucket_name=None):
    """
    Downloads a file from a specified folder in an S3 bucket and saves it to the specified file path.

    Args:
        prefix (str): The prefix of the folder in the S3 bucket.
        file_name (str): The name of the file.
        file_path (str): The path to the file where the object will be saved.
        bucket_name (str, optional): The name of the S3 bucket. Defaults to settings.s3_bucket_name.

    Raises:
        Exception: If an error occurs during the file download.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(
        f"bucket_name={bucket_name}, prefix={prefix}, file_name={file_name}, file_path={file_path}"
    )

    try:
        # Download object data to file_path
        s3_client.fget_object(
            bucket_name=bucket_name,
            object_name=f"{prefix}/{file_name}",
            file_path=file_path,
        )
        logger.debug(f"Retrieved into {file_path}")
    except Exception as err:
        logger.error(err)
        raise err


def list_files_in_folder(prefix, bucket_name=None) -> list:
    """
    Retrieves a list of object names from a folder in an S3 bucket.

    object_names=['c9421a00ea0e4123bfee492a9517f285/', 'c9421a00ea0e4123bfee492a9517f285/test.json']
    file_names=['c9421a00ea0e4123bfee492a9517f285']

    Args:
        prefix (str): The prefix to filter the object names.
        bucket_name (str, optional): The name of the S3 bucket. Defaults to settings.s3_bucket_name.

    Returns:
        list: A list of file names.

    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}, prefix={prefix}")

    try:
        objects = s3_client.list_objects(
            bucket_name=bucket_name, prefix=prefix, recursive=True
        )

        object_names = []
        object_count = 0
        for object in objects:
            object_count += 1
            logger.debug(
                f"object_count={object_count}, object_name={object.object_name}"
            )
            object_names.append(object.object_name)

        return get_file_names_from_object_names(object_names, True)
    except Exception as err:
        logger.error(err)
        raise err


def remove_file_from_folder(prefix, file_name, bucket_name=None):
    """
    Removes a file from a specified folder in an S3 bucket.

    Args:
        prefix (str): The prefix of the folder in the S3 bucket.
        file_name (str): The name of the file.
        bucket_name (str, optional): The name of the S3 bucket. Defaults to settings.s3_bucket_name.

    Raises:
        Exception: If an error occurs during the file download.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}, prefix={prefix}, file_name={file_name}")

    try:
        object_name = f"{prefix}/{file_name}"
        s3_client.remove_object(
            bucket_name=bucket_name,
            object_name=object_name,
        )
        logger.debug(f"object_name={object_name} removed")
    except Exception as err:
        logger.error(err)
        raise err


def remove_bucket(bucket_name=None):
    """
    Empties and removes a bucket.

    This function retrieves a list of all objects in a bucket and deletes each object. It then removes
    the bucket.

    Args:
        bucket_name (str, optional): The name of the bucket. Defaults to settings.s3_bucket_name.

    Raises:
        Exception: If an error occurs during the cleanup process.
    """
    if bucket_name is None:
        bucket_name = settings.s3_bucket_name
    logger.debug(f"bucket_name={bucket_name}")

    try:
        objects = s3_client.list_objects(bucket_name, recursive=True)
        for object in objects:
            s3_client.remove_object(bucket_name, object.object_name)
            logger.debug(f"object_name={object.object_name} removed")
        s3_client.remove_bucket(bucket_name)
        logger.debug(f"bucket_name={bucket_name} removed")
    except Exception as err:
        logger.error(err)
        raise err


def remove_all_buckets():
    """
    Empties and removes all buckets.

    This function retrieves a list of buckets and iterates over each one. It then retrieves a list of all
    objects in the bucket and deletes each object. It then removes the bucket.

    Raises:
        Exception: If an error occurs during the cleanup process.
    """
    logger.debug("")

    try:
        buckets = s3_client.list_buckets()
        for bucket in buckets:
            files = s3_client.list_objects(bucket.name, recursive=True)
            for file in files:
                s3_client.remove_object(bucket.name, file.object_name)
                logger.debug(f"object_name={object.object_name} removed")
            s3_client.remove_bucket(bucket.name)
            logger.debug(f"bucket_name={bucket.name} removed")
        logger.debug("All buckets removed")
    except Exception as err:
        logger.error(err)
        raise err


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
    except Exception as err:
        logger.error("create_folder " + err.args[0])      

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
        # now trim out everything after the backslash
        return file_names
    except Exception as err:
        logger.error("list_folder_files " + err.args[0])


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
    except Exception as err:
        logger.error("save_file_in_folder " + err.args[0])   

def get_file_in_folder(file_path,folder_name,bucket_name,object_name,url,key, secret, secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:
        # append name
        get_name = folder_name + '/' + object_name

        client.fget_object(
            bucket_name=bucket_name,
            object_name=get_name,
            file_path=file_path)
    except Exception as err:
        logger.error("get_file_in_folder " + err.args[0])        

def get_folders(bucket_name,url,key, secret, secure=False):
    client = Minio(
        url,
        access_key=key,
        secret_key=secret,
        secure=secure
    )

    try:
        # append name
        files = client.list_objects(bucket_name,recursive=True)
        # loop and turn into a list to return
        file_names = []
        for file in files:
            file_names.append(file.object_name)

        file_names = filter_names_with_no_content_after_backslash(file_names)
        return file_names

    except Exception as err:
        logger.error("get_folders " + err.args[0])           