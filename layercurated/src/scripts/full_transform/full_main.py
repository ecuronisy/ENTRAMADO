from io import BytesIO
import pandas as pd
import datetime

from scripts.dbutils.minioutils import upload_parquet_from_bytes, get_object_list, get_object_content
from scripts.datautils.dateutils import get_last_execution_date, set_last_execution_date

def run(base_parameters):
    source_fields = base_parameters.get("source_fields")

    source_bucket = base_parameters.get("source_bucket")
    target_bucket = base_parameters.get("target_bucket")

    # Last execution date
    last_execution_date = get_last_execution_date(source_bucket)
    print(f"Last execution date: {last_execution_date}")
    last_execution_date_no_hour = last_execution_date.strftime('%Y-%m-%d')

    # Get object list from last execution date to now
    start_date = datetime.datetime.strptime(last_execution_date_no_hour, '%Y-%m-%d').date()
    print(f"Start date: {start_date}")
    today = datetime.date.today()
    print(f"Today: {today}")
    days = (today - start_date).days
    objects = []
    while days >= 0:
        start_date = start_date + datetime.timedelta(days=1)
        days -= 1
        str_date = start_date.strftime('%Y-%m-%d')
        objects += get_object_list(f"{source_bucket}/{str_date}/", last_execution_date)
        print(f"Objects: {len(objects)}")
        for object in objects:
            print(f"Object: {object.object_name}")

    for obj in objects:
        obj_data = get_object_content(obj.object_name)
        df_raw = pd.read_csv(obj_data, encoding='utf-8')

        df = pd.DataFrame({
            field_name: pd.Series(dtype=field_info['type_pandas'])
            for field_name, field_info in source_fields.items()
        })
    
        # Add data to DataFrame
        for field_name, field_info in source_fields.items():
            if field_name in df_raw.columns:
                print(f"Adding field: {field_name}")
                df[field_name] = df_raw[field_name].astype(field_info['type_pandas'], errors='ignore')

        # TODO: Process DataFrame


        # Get latest file modification date
        file_name = (obj.object_name).split(".")[0]
        file_date = file_name[-17:]
        latest_date = pd.to_datetime(file_date, format='%Y-%m-%d_%H%M%S')
        date = latest_date.strftime('%Y-%m-%d %H%M%S')

        # Save DataFrame to parquet
        try:
            dateday = pd.to_datetime(date).strftime('%Y-%m-%d')
            datename = pd.to_datetime(date).strftime('%Y-%m-%d_%H%M%S')
            target_path = f"{target_bucket}/{dateday}/" # TODO: Replace with target bucket in S3
            print(f"Saving to: {target_path}")

            parquet_buffer = BytesIO()
            df.to_parquet(parquet_buffer)
            parquet_buffer.seek(0)
            file_name = f"{target_bucket}_curated{datename}.parquet"
            upload_parquet_from_bytes(parquet_buffer, f"{target_path}{file_name}")

            datelog = pd.to_datetime(date).strftime('%Y-%m-%d %H:%M:%S.%f')
            #Update most recent file modification date in execution log
            if get_last_execution_date(source_bucket) < pd.to_datetime(datelog):
                set_last_execution_date(source_bucket, datelog)
        except Exception as e:
            raise Exception(f"CURATED STORAGE ERROR: {e}")