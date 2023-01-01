import pymongo
import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from premium import utils
import pandas as pd
import numpy as np
import yaml
import dill
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

def write_yaml_file(file_path, data:dict):
    """
    Description: This function will generate a data validation report as yaml file.
    ===============================================================================
    Params:
    file_path: file path to store the report
    data: Dictionary conaining data validation checks in key value pair
    """
    try:
        # creating directory to store the yaml file.
        logging.info("creating directory to store the yaml file.")
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)

        # write all the data generated in "validation_error" dict in yaml file.
        logging.info("write all the data generated in 'validation_error' dict in yaml file.")
        with open(file_path,"w") as file_writer:
            yaml.dump(data, file_writer) 

    except Exception as e:
        raise PremiumException(e, sys)

def save_object(file_path: str, obj: object) -> None:
    """
    Description: This function will store models/objects in pickle file format.
    """
    try:
        # Create a directory to save the object.
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Dump the object data into the file path.
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise PremiumException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Description: Save numpy array data to file
    ============================================
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise PremiumException(e, sys) from e