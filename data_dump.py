import pymongo
import pandas as pd
import json
import os
from mice.config import mongo_client
# Provide the mongodb localhost url to connect python to mongodb.

DATA_FILE_PATH = "/config/workspace/mïce.csv"
DATABASE_NAME = "mice_preotein"
COLLECTION_NAME = "Mice"


if __name__=="__main__":
    
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    #Convert  dataframe to json so that we can dump these record into mongo database
    df.reset_index(drop=True,inplace = True)
    
    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    #Insert converted json record to mongo db
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
