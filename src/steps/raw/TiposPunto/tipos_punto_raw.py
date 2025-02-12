import os

def run(base_parameters):

    sql_database = base_parameters.get("sql_database")
    sql_schema = base_parameters.get("sql_schema")
    sql_table = base_parameters.get("sql_table")
    sql_string = base_parameters.get("sql_string")
    source_bucket = base_parameters.get("source_bucket")
    fields = base_parameters.get("fields")

    print(f"Base de datos: {sql_database}")
    print(f"Esquema: {sql_schema}")
    print(f"Tabla: {sql_table}")
    print(f"Cadena SQL: {sql_string}")
    print(f"Bucket de origen: {source_bucket}")

    print("Fields:")
    for field_name, field_info in fields.items():
        description = field_info.get('description', 'empty')
        type_pandas = field_info.get('type_pandas', 'empty')
        print(f"- Field: {field_name}, Description: {description}, Type: {type_pandas}")

    sql_password = os.getenv("SQL_PASSWORD")
    sql_user = os.getenv("SQL_USER")
    print(f"SQL_USER: {sql_user}")
    print(f"SQL_PASSWORD: {sql_password}")