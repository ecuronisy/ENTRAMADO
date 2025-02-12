from sqlalchemy import create_engine

def generate_connection_string_sqlalchemy(driver="mssql+pyodbc", server=None, database=None, username=None, password=None):

    if not all([server, database, username, password]):
        raise ValueError("Parameters 'server', 'database', 'username', and 'password' for connection string not found.")

    return f"{driver}://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"


def get_sqlalchemy_engine(server, database, username, password, driver="mssql+pyodbc"):

    connection_string = generate_connection_string_sqlalchemy(driver, server, database, username, password)
    return create_engine(connection_string)