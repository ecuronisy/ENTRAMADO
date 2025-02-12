import os
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from steps.dbutils.sqlutils import get_sqlalchemy_engine

def run(base_parameters):

    sql_database = base_parameters.get("sql_database")
    sql_schema = base_parameters.get("sql_schema")
    sql_table = base_parameters.get("sql_table")
    #sql_string = base_parameters.get("sql_string")
    target_bucket = base_parameters.get("target_bucket")
    fields = base_parameters.get("fields")

    sql_server = os.getenv("SQL_SERVER")
    sql_user = os.getenv("SQL_USER")
    sql_password = os.getenv("SQL_PASSWORD")

    # Connect to SQL Server
    try:
        engine = get_sqlalchemy_engine(sql_server, sql_database, sql_user, sql_password)
    except Exception as e:
        raise Exception(f"SQL Server CONNECTION ERROR: {e}")

    query = f"SELECT * FROM {sql_schema}.{sql_table}"
    
    try:
        # SQL data to DataFrame
        with engine.connect() as conn:
            df_raw = pd.read_sql(query, conn)
    except Exception as e:
        raise Exception(f"SQL Server QUERY ERROR: {e}")
    finally:
        conn.close()
        print("Conexión cerrada.")

    # Create DataFrame from fields
    df = pd.DataFrame({
        field_name: pd.Series(dtype=field_info['type_pandas'])
        for field_name, field_info in fields.items()
    })

    # Add data to DataFrame with 
    for field_name, field_info in fields.items():
        if field_name in df_raw.columns:
            print(f"Adding field: {field_name}")
            df[field_name] = df_raw[field_name].astype(field_info['type_pandas'], errors='ignore') 

    try:
        target_path = f"./src{target_bucket}provincias_raw.csv" # TODO: Replace with target bucket in S3
        df.to_csv(target_path, index=False)
    except Exception as e:
        raise Exception(f"RAW STORAGE ERROR: {e}")
