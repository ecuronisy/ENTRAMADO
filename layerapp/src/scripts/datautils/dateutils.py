import json
import datetime

def get_last_execution_date(table: str) -> datetime.datetime:
    """
    Read the last execution date for a given table from the executionlog.json file

    Args:
        table (str): The name of the table

    Returns:
        datetime.datetime: last execution date

    Raises:
        Exception: If there is an error reading the last execution date.
    """
    
    try:
        with open("./src/executionlog.json", "r") as archivo:
            data = json.load(archivo)

        last_execution_date = data.get(table, None)
        return datetime.datetime.strptime(last_execution_date, "%Y-%m-%d %H:%M:%S.%f")
    except Exception as e:
        raise e
    
def set_last_execution_date(table: str, last_execution_date: str) -> None:
    """
    Saves the last execution date of a table in the executionlog.json file

    Args:
        table (str): The name of the table
        last_execution_date (str): The last execution date of the table in the format '%Y-%m-%d %H:%M:%S.%f'

    Raises:
        Exception: If there is an error saving the last execution date.
    """
    
    try:
        with open("./src/executionlog.json", "r") as archivo:
            data = json.load(archivo)

        data[table] = last_execution_date
        with open("./src/executionlog.json", "w") as archivo:
            json.dump(data, archivo, indent=4)
    except Exception as e:
        raise e