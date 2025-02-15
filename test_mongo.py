import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
import pandas as pd


MONGO_DB_URL=os.getenv("MONGO_DB_URL")

client = MongoClient(MONGO_DB_URL)
db = client["MLPROJECT"]
collection = db["NetworkData"]

print("Count of records in collection:", collection.count_documents({}))
df=pd.DataFrame(list(collection.find()))
print(df.shape)