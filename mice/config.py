import pymongo
import pandas as pd 
import json
from dataclasses import dataclass

import os
# Provide the mongodb localhost url to connect python to mongodb

import os

@dataclass
class  EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key_id:str = os.getenv("AWS_SECRET_ACCESS_KEY")


TARGET_COLUMN_MAPPING = {
    "c-CS-m":0,
    "c-SC-m" : 2,
    "c-CS-s" : 1,
    "c-SC-s" : 3, 
    "t-CS-m" : 4, 
    "t-SC-m" : 6,
    "t-CS-s" : 5, 
    "t-SC-s" : 7
}


env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "class"