import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from premium.utils import get_collection_as_dataframe
from premium.entity import config_entity
from premium.components.data_ingestion import DataIngestion

if __name__=="__main__":
     try:
          #test_logger_and_exception()
          #get_collection_as_dataframe(database_name="Insurance", collection_name="InsurancePremium")
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          logging.info(data_ingestion_config.to_dict())
          #print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          logging.info(data_ingestion.initiate_data_ingestion())
          #print(data_ingestion.initiate_data_ingestion())
     except Exception as e:
          print(e)