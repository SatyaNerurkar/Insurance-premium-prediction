import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from premium import utils
from premium.logger import logging
from premium.exception import PremiumException
from premium.entity import config_entity
from premium.entity import artifact_entity

class DataIngestion:
    def __init__(self, data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"|{'-'*50}|| Data Ingestion ||{'-'*50}|")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise PremiumException(e, sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            # Exporting collection data as pandas dataframe
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)

            # Save data in feature store
            logging.info("Save data in feature store")
            logging.info("Create feature store folder if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)

            # Create feature store folder if not available
            os.makedirs(feature_store_dir,exist_ok=True)

            # Save df to feature store folder
            logging.info("Save dataframe to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            # Split dataset into train and test set
            logging.info("split dataset into train and test set")
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
            
            # create dataset directory folder if not available.
            logging.info("create dataset directory folder if not available")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            # Save train and test dataframe to feature store folder
            logging.info("Save df to feature store folder")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            # Prepare artifact
            logging.info("Preparing artifact (output)")
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise PremiumException(e, sys)
        