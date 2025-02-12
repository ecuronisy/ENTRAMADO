import os

from pymongo import MongoClient
import pandas as pd

def connect_to_mongo():

    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    client = MongoClient(connection_string)
    return client

def insert_dataframe_to_mongo(client, database_name, collection_name, df):

    db = client[database_name]
    collection = db[collection_name]
    
    # Convertir DataFrame a lista de diccionarios
    records = df.to_dict(orient='records')
    
    if records:
        collection.insert_many(records)
        print(f"{len(records)} records inserted into '{collection_name}' in '{database_name}'.")
    else:
        print("Empty DataFrame.")