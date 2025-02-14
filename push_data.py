import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # Ensure correct spelling
if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not set in environment variables.")

print("MongoDB URL:", MONGO_DB_URL)  # Debugging

class NetworkDataExtract():
    def __init__(self):
        try:
            self.mongo_client = MongoClient(MONGO_DB_URL, server_api=ServerApi('1'))  # Fix connection issue
        except Exception as e:
            raise NetworkSecurityException(str(e), sys)

    def csv_to_json(self, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            print("Loading file:", os.path.abspath(file_path))  # Debugging

            data = pd.read_csv(file_path)
            if data.empty:
                raise ValueError("CSV file is empty!")

            records = list(json.loads(data.T.to_json()).values())
            print(f"Loaded {len(records)} records.")  # Debugging
            return records

        except Exception as e:
            raise NetworkSecurityException(str(e), sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            if not records:
                raise NetworkSecurityException("No records found to insert into MongoDB.", sys)

            db = self.mongo_client[database]
            col = db[collection]

            inserted = col.insert_many(records)
            print(f"Inserted {len(inserted.inserted_ids)} records into MongoDB.")

            return len(inserted.inserted_ids)

        except Exception as e:
            raise NetworkSecurityException(str(e), sys)

if __name__ == '__main__':
    FILE_PATH = os.path.join("Network_Data", "phisingData.csv")  # Fix file path handling
    DATABASE = "MLPROJECT"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json(file_path=FILE_PATH)

    print('Processing Data...')
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)

    print(no_of_records, 'records successfully pushed to MongoDB!')
