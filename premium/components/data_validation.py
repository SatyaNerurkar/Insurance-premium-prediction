import os, sys
import pandas as pd
import numpy as np
from premium import utils
from premium.logger import logging
from premium.exception import PremiumException
from premium.entity import config_entity, artifact_entity
from premium.config import TARGET_COLUMN

class DataValidation:

    def __init__(self, 
                 data_validaton_config:config_entity.DataValidationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"|{'-'*50}|| Data Validaton ||{'-'*50}|")
            self.data_validation_config = data_validaton_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error=dict()

        except Exception as e:
            raise PremiumException(e, sys)

    def is_required_column_exists(self, base_df:pd.DataFrame, current_df:pd.DataFrame,report_key_name:str)->bool:
        """
        Description: This function will validate whether all features that are required for predictions are present or not.
        base df: Accepts a pandas dataframe base df as reference.
        current df: Accepts a pandas dataframe base df to be validated.
        =====================================================================================
        returns boolean value if all required columns are available in dataset.
        """
        try:
            missing_column=[]
            base_columns=base_df.columns
            current_columns=current_df.columns
            # iterating through each column in base column.
            for base_column in base_columns:
                if base_column not in current_columns:
                    # If any column is not present in current dataframe reporting it in log file and missing column list.
                    logging.info(f"Column {base_column} is not available in dataset.")
                    missing_column.append(base_column)

            # Adding list of all missing columns in the validation error report.
            if len(missing_column) > 0:
                self.validation_error[report_key_name] = missing_column
                return False
            return True

        except Exception as e:
            raise PremiumException(e, sys)
                
    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str):
        """
        Description: This function will validate whether all features have same categorical data or not.
        ====================================================================================
        base df: Accepts a pandas dataframe base df as reference
        current df: Accepts a pandas dataframe base df to be validated
        """
        try:
            # Define a data drift report dictionary.
            drift_report=dict()

            # Find the categorical columns in both datasets.
            logging.info(f"Find the categorical columns in both datasets.")
            cat_columns_base_df = base_df.select_dtypes(include=['object']).columns.tolist()
            cat_columns_current_df = current_df.select_dtypes(include=['object']).columns.tolist()

            # Check if the categorical columns in both datasets are the same.
            logging.info(f"Check if the categorical columns in both datasets are the same.")
            if set(cat_columns_base_df) == set(cat_columns_current_df):
                logging.info(f"The categorical columns in both datasets are the same.")
                #print("The categorical columns in both datasets are the same.")
            else:
                logging.info(f"The categorical columns in both datasets are not the same.")
                #print("The categorical columns in both datasets are not the same.")

            # Iterate through the categorical columns and check if the values are identical
            logging.info(f"Iterate through the categorical columns and check if the values are identical.")
            for base_column in cat_columns_base_df:
                if set(base_df[base_column]) == set(current_df[base_column]):
                    logging.info(f"The values in the '{base_column}' column are identical in both datasets. check report for more info.")
                    #print(f"The values in the '{base_column}' column are identical in both datasets.")
                    drift_report[base_column]={
                        "Values in base dataset":base_df[base_column].unique().tolist(),
                        "Values in current dataset": current_df[base_column].unique().tolist(),
                        "same_distribution": True
                    }
                else:
                    logging.info(f"The values in the '{base_column}' column are identical in both datasets. check report for more info.")
                    print(f"The values in the '{base_column}' column are not identical in both datasets.")
                    drift_report[base_column]={
                        "Values in base dataset":base_df[base_column].unique().tolist(),
                        "Values in current dataset": current_df[base_column].unique().tolist(),
                        "same_distribution": False
                    }

            self.validation_error[report_key_name]=drift_report
        
        except Exception as e:
            raise PremiumException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        """
        Description: This function will perform all the data validation checks on the new dataset.
        ====================================================================================
        Checks to be performed:
            - Contains all required features
            - data drift report
        """
        try:
            # Reading base dataframe (reference dataframe)
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_dir)

            # Reading train dataframe
            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)

            # Reading test dataframe
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # Validate whether all features are present in train dataframe or not.
            logging.info(f"Are all required columns present in train df")
            train_df_column_status = self.is_required_column_exists(base_df=base_df, 
                                                                    current_df=train_df, 
                                                                    report_key_name="missing_column_within_train_dataset")

            # Validate whether all features are present in test dataframe or not.
            logging.info(f"Are all required columns present in test df")
            test_df_column_status = self.is_required_column_exists(base_df=base_df, 
                                                                   current_df=test_df, 
                                                                   report_key_name="missing_column_within_test_dataset")
                    
            # if all columns are available in train df then detect "data drift" if present.
            if train_df_column_status:
                logging.info(f"As all the columns are available in train df hence detecting 'data drift'")
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name="data_drift_within_train_dataset")

            # if all columns are available in test df then detect "data drift" if present.
            if test_df_column_status:
                logging.info("As all the columns are available in test df hence detecting for 'data drift'") 
                self.data_drift(base_df=base_df, current_df=test_df, report_key_name="data_drift_within_test_dataset")

            # Write the report in yaml file.
            logging.info("Write the data validation report in yaml")
            utils.write_yaml_file(file_path=self.data_validation_config.reprt_file_dir, 
                                  data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.reprt_file_dir)
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise PremiumException(e, sys)