import os, sys
import pandas as pd
import numpy as np
from premium import utils
from premium.config import TARGET_COLUMN
from premium.logger import logging
from premium.exception import PremiumException
from premium.entity import config_entity, artifact_entity
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


class DataTransformation:
    
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig, data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"|{'-'*50}|| Data Trasnformation ||{'-'*50}|")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise PremiumException(e, sys)

        
    def get_data_transformer_object(self)-> ColumnTransformer:
        """
        Description: This function will create a data transformer pipeline
        ======================================================
        returns Pipline
        """
        try:
            # reading dataset from feature store to extract numeric columns and categorical columns.
            logging.info("reading dataset from feature store to extract numeric columns and categorical columns.")
            df = pd.read_csv(self.data_ingestion_artifact.feature_store_file_path)
            df = df.drop(TARGET_COLUMN, axis=1)
                  
            # Get a list of the numeric and categorical columns in the DataFrame
            numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            logging.info(f"numerical columns: {numeric_cols}")
            logging.info(f"categorical columns:{categorical_cols}")

            # creating KNNImputer object to handle numerical features.
            logging.info("creating KNNImputer object to handle numerical features.")
            knnimputer = KNNImputer()

            # creating standard scaler object.
            logging.info("creating standard scaler object to scale numerical features.")
            standarscaler = StandardScaler()

            # Creting simple imputer object with strategy as 'constant' to handle categorical features.
            logging.info(f"Creting simple imputer object with strategy as 'constant'")
            simple_imputer = SimpleImputer(strategy="most_frequent")

            # creating OneHotEncoder object to convert categorical columns into numeric.
            logging.info("creating OneHotEncoder object to convert categorical columns into numeric.")
            onehotencoder = OneHotEncoder()

            # creating pipeline for numeric columns.
            logging.info("creating pipeline for numeric columns.")
            numeric_pipeline = Pipeline(steps=[
                ('knnimputer', knnimputer),
                ('standarscaler', standarscaler)])

            # creating pipeline for categorical columns.
            logging.info("creating pipeline for categorical columns.")
            categorical_pipeline = Pipeline(steps=[
                ('simple_imputer', simple_imputer),
                ('onehotencoder', onehotencoder)])

            # Create a transformer that applies the appropriate pipeline to each column.
            logging.info("Create a transformer that applies the appropriate pipeline to each column.")
            transformer = ColumnTransformer(transformers=[
                ('numeric', numeric_pipeline, numeric_cols),
                ('categorical', categorical_pipeline, categorical_cols)])

            return transformer

        except Exception as e:
            raise PremiumException(e, sys)

    def initiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        """
        Description: This function will perform all the data transformation on the train and test dataset.
        """
        try:
            # reading train and test csv file.
            logging.info(f"reading training and testing file for data transformation.")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # selecting input feature for train and test dataframe.
            logging.info(f"selecting input feature for train and test dataframe transformation.")
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)


            # selecting target feature for train and test dataframe.
            logging.info(f"selecting target feature for train and test dataframe transformation.")
            target_feature_train_df = train_df[TARGET_COLUMN]            
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            # fetch data transformation pipeline object.
            transformation_pipeline = self.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            # transforming input features
            logging.info(f"Performing transformation on input features")
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(X=input_feature_test_df)
            
            # create numpy array of transformed dataset.
            logging.info("create numpy array of transformed dataset.")
            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # save numpy array.
            logging.info(f"Storing  train array in {self.data_transformation_config.transformed_train_dir}")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_dir,
                                        array=train_arr)

            logging.info(f"Storing  train array in {self.data_transformation_config.transformed_test_dir}")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_dir,
                                        array=test_arr)

            # Store the pipeline object.
            logging.info(f"Storing  pipeline object in {self.data_transformation_config.transformer_object_dir}")
            utils.save_object(file_path=self.data_transformation_config.transformer_object_dir, obj=transformation_pipeline)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transformer_object_dir=self.data_transformation_config.transformer_object_dir,
                transformed_train_dir = self.data_transformation_config.transformed_train_dir,
                transformed_test_dir = self.data_transformation_config.transformed_test_dir)

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise PremiumException(e, sys)
