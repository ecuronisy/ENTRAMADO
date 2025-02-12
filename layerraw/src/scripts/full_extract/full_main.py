import os

from io import BytesIO
import pandas as pd

from scripts.dbutils.sqlutils import get_sqlalchemy_engine
from scripts.dbutils.minioutils import upload_csv_from_bytes
from scripts.datautils.dateutils import get_last_execution_date, set_last_execution_date

def run(base_parameters):

    sql_database = base_parameters.get("sql_database")
    sql_schema = base_parameters.get("sql_schema")
    sql_table = base_parameters.get("sql_table")
    #sql_string = base_parameters.get("sql_string")
    fields = base_parameters.get("fields")

    sql_server = os.getenv("SQL_SERVER")
    sql_user = os.getenv("SQL_USER")
    sql_password = os.getenv("SQL_PASSWORD")

    # Connect to SQL Server
    try:
        engine = get_sqlalchemy_engine(sql_server, sql_database, sql_user, sql_password)
    except Exception as e:
        raise Exception(f"SQL Server CONNECTION ERROR: {e}")

    # Last execution date
    last_execution_date = get_last_execution_date(sql_table)
    print(f"Last execution date: {last_execution_date}")

    # Query
    query = f"SELECT * FROM {sql_schema}.{sql_table}"
    try:
        # SQL data to DataFrame
        with engine.connect() as conn:
            df_raw = pd.read_sql(query, conn)
        if df_raw.empty:
            raise Exception("No new data to process.")
    except Exception as e:
        raise Exception(f"SQL Server QUERY ERROR: {e}")
    finally:
        conn.close()
        print("Closed conection.")

    # Create DataFrame from fields
    df = pd.DataFrame({
        field_name: pd.Series(dtype=field_info['type_pandas'])
        for field_name, field_info in fields.items()
    })

    # Add data to DataFrame
    for field_name, field_info in fields.items():
        if field_name in df_raw.columns:
            print(f"Adding field: {field_name}")
            df[field_name] = df_raw[field_name].astype(field_info['type_pandas'], errors='ignore')

    # Get latest file modification date
    """ latest_date = df['fechaUltimaModificacion'].max()
    date = latest_date.strftime('%Y-%m-%d %H%M%S.%f') """ # TODO: Use this when all tables have the fechaUltimaModificacion column

    # Save DataFrame to CSV
    try:
        date = pd.to_datetime('now').strftime('%Y-%m-%d %H%M%S.%f')
        dateday = pd.to_datetime(date).strftime('%Y-%m-%d')
        datename = pd.to_datetime(date).strftime('%Y-%m-%d_%H%M%S')
        target_path = f"{sql_table}/{dateday}/" # TODO: Replace with target bucket in S3
        print(f"Saving to: {target_path}")

        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        csv_buffer.seek(0)
        file_name = f"{sql_table}_raw{datename}.csv"
        upload_csv_from_bytes(csv_buffer, f"{target_path}{file_name}")
        
        datelog = pd.to_datetime(date).strftime('%Y-%m-%d %H:%M:%S.%f')
        set_last_execution_date(sql_table, datelog)
    except Exception as e:
        raise Exception(f"RAW STORAGE ERROR: {e}")