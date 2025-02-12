from sqlalchemy import create_engine

def generate_connection_string_sqlalchemy(server=None, database=None, username=None, password=None, driver="mssql+pyodbc"):
    """
    Generates a connection string for SQLAlchemy using the specified parameters.

    Args:
        driver (str): The database driver to use. Default is 'mssql+pyodbc'.
        server (str): The server address of the database.
        database (str): The name of the database.
        username (str): The username to access the database.
        password (str): The password for the given username.

    Returns:
        str: A connection string formatted for use with SQLAlchemy.

    Raises:
        ValueError: If any of 'server', 'database', 'username', or 'password' are not provided.
    """

    if not all([server, database, username, password]):
        raise ValueError("Parameters 'server', 'database', 'username', and 'password' for connection string not found.")

    return f"{driver}://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"


def get_sqlalchemy_engine(server: str, database: str, username: str, password: str, driver="mssql+pyodbc"):
    """
    Creates a SQLAlchemy Engine object using the specified parameters.

    Args:
        server (str): The server address of the database.
        database (str): The name of the database.
        username (str): The username to access the database.
        password (str): The password for the given username.
        driver (str): The database driver to use. Default is 'mssql+pyodbc'.

    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy Engine object.

    Raises:
        ValueError: If any of 'server', 'database', 'username', or 'password' are not provided.
    """

    connection_string = generate_connection_string_sqlalchemy(server, database, username, password, driver)
    return create_engine(connection_string)