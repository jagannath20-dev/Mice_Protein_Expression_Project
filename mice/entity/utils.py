import pandas as pd
from mice.config import mongo_client
from mice.logger import logging
from mice.exception import MiceException
import os, sys

def get_collection_as_dataframe(database_name:str,collection_name:str):
    """
    Description : This Function return collection as dataframe
    ========================================================================
    Params : 
    database_name = database name
    collection_name = collection name
    ========================================================================
    return Pandas Dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {} and collection {}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")

        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis = 1)
            logging.info(f"Row and Columns in df: {df.shape}")
        return df

    except Exception as e:
        raise MiceException(e, sys)
