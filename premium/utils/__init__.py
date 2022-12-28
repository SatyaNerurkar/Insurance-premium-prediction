import pymongo
import os, sys
from premium.logger import logging
from premium.exception import PremiumException
import pandas as pd
import numpy as np
from premium.config import mongo_client

def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        # Extracting all the records from mongoDB collection converting it into a list and creating a dataframe out of it.
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}.")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns:{list(df.columns)}")

        # Dropping "_id" column from dataframe if exists.
        if "_id" in df.columns:
            logging.info(f"Dropping '_id' column from dataframe.")
            df = df.drop("_id", axis=1)
        
        logging.info(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except Exception as e:
        raise PremiumException(e, sys)

