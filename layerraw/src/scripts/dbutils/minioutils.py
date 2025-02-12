from minio import Minio
from io import BytesIO

minio = Minio(
    "miniomrw:9000",
    access_key="K3if7FoVkgFEN5toBj8L",
    secret_key="YAeIYbQepV87bmhvHeCq9m0dwIuwBCFHtABQ1RZD",
    secure=False
)

def upload_csv_from_bytes(csv_buffer: BytesIO, object_name: str, bucket_name: str = "raw") -> None:
    """
    Uploads a csv from a BytesIO to a Minio bucket.

    Args:
        csv_buffer (BytesIO): The csv data to be uploaded.
        object_name_p (str): The name of the object in the bucket.
        bucket_name_p (str, optional): The name of the bucket. Defaults to "raw".

    Raises:
        Exception: If there is a problem with the upload.
    """

    try:
        print("Checking")
        # Check if the bucket exists, if not, create it
        if not minio.bucket_exists(bucket_name):
            minio.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' exists.")
        
        # Upload csv to the bucket
        minio.put_object(
            bucket_name="raw",
            object_name=object_name,
            data=csv_buffer,
            length=csv_buffer.getbuffer().nbytes,
            content_type="text/csv"
        )
        print(f"File '{object_name}' uploaded in bucket '{bucket_name}'.")
    except Exception as e:
        raise Exception(f"Minio upload error: {e}")