# Define input for each component as config.
import os, sys
from datetime import datetime
from premium.exception import PremiumException

FILE_NAME = "InsurancePremium.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            # Creating "artifact" directory and within that creating a folder with name as timestamp.
            self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise PremiumException(e, sys)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            # Define database name and collection name.
            self.database_name = "Insurance"
            self.collection_name = "InsurancePremium"

            # creating "data_ingestion" directory within "artifact".
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")

            # creating "feature_store" directory within "data_ingestion" to store CSV file extracted from MongoDB.
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)

            # creating "dataset" directory within "data_ingestion" to store train and test file created after traintestsplit.
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e:
            raise PremiumException(e, sys)

    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise PremiumException(e, sys)

class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            # Define "data_validation" directory within "artifact".
            self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_validation")

            # Define "report.yaml" file inside "data_validation" directory.
            self.reprt_file_dir=os.path.join(self.data_validation_dir,"report.yaml")

            # Define base file path.
            self.base_file_dir=os.path.join("/config/workspace/insurance-premium-prediction-csv/insurance.csv")
            
        except Exception as e:
            raise PremiumException(e, sys)

class DataTransformationConfig:...

class ModelTrainerConfig:...

class ModelEvaluationConfig:...

class ModelPusherConfig:...