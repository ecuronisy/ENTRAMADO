import datetime
from minio import Minio
from io import BytesIO

minio = Minio(
    "miniomrw:9000",
    access_key="K3if7FoVkgFEN5toBj8L",
    secret_key="YAeIYbQepV87bmhvHeCq9m0dwIuwBCFHtABQ1RZD",
    secure=False
)

def upload_csv_from_bytes(csv_buffer: BytesIO, object_name_p: str, bucket_name_p: str = "app") -> None:
    """
    Uploads a csv from a BytesIO to a Minio bucket.

    Args:
        csv_buffer (BytesIO): The csv data to be uploaded.
        object_name_p (str): The name of the object in the bucket.
        bucket_name_p (str, optional): The name of the bucket. Defaults to "app".

    Raises:
        Exception: If there is a problem with the upload.
    """

    try:
        print("Checking")
        # Check if the bucket exists, if not, create it
        if not minio.bucket_exists(bucket_name_p):
            minio.make_bucket(bucket_name_p)
            print(f"Bucket '{bucket_name_p}' created successfully.")
        else:
            print(f"Bucket '{bucket_name_p}' exists.")
        
        # Upload csv to the bucket
        minio.put_object(
            bucket_name=bucket_name_p,
            object_name=object_name_p,
            data=csv_buffer,
            length=csv_buffer.getbuffer().nbytes,
            content_type="text/csv"
        )
        print(f"File '{object_name_p}' uploaded in bucket '{bucket_name_p}'.")
    except Exception as e:
        raise Exception(f"Minio upload error: {e}")
    
def get_object_list(path: str, date_filter: str, bucket_name: str = "curated") -> list:
    """
    Retrieves a list of objects from a Minio bucket, filtered by a date.

    Args:
        path (str): The prefix path to filter the objects in the bucket.
        date_filter (str): The date filter in the format '%Y-%m-%d_%H%M%S'. Only objects
                           with a date greater than this will be returned.
        bucket_name (str, optional): The name of the bucket to list objects from. 
                                     Defaults to "curated".

    Returns:
        list: A list of Minio objects filtered by the specified date.

    Raises:
        Exception: If there is an error listing objects from the Minio bucket.
    """

    try:
        print(f"Date filter {date_filter}")
        print("Path: " + path)
        objects = minio.list_objects(bucket_name, prefix=path)
        filtered_objects = []
        for obj in objects:
            file_name = obj.object_name.split("/")[-1]
            file_name = file_name.split(".")[0]
            file_date = file_name[-17:]
            file_date = datetime.datetime.strptime(file_date, '%Y-%m-%d_%H%M%S')

            if file_date > date_filter:
                filtered_objects.append(obj)

        return filtered_objects
    
    except Exception as e:
        raise Exception(f"Minio list error: {e}")
    
def get_object_content(object_name: str, bucket_name: str = "curated") -> str:
    """
    Retrieves the content of an object from a Minio bucket.

    Args:
        object_name (str): The name of the object to retrieve.
        bucket_name (str, optional): The name of the bucket. Defaults to "curated".

    Returns:
        str: The content of the object as a string.

    Raises:
        Exception: If there is an error retrieving the object from the Minio bucket.
    """

    try:
        object_data = minio.get_object(bucket_name, object_name)
        data = BytesIO(object_data.read())
        return data
    except Exception as e:
        raise Exception(f"Minio get error: {e}")