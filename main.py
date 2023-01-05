import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from premium.utils import get_collection_as_dataframe
from premium.entity import config_entity
from premium.components.data_ingestion import DataIngestion
from premium.components.data_validation import DataValidation
from premium.components.data_transformation import DataTransformation
from premium.components.model_trainer import ModelTrainer
from premium.components.model_evaluation import ModelEvaluation

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
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
          logging.info(data_ingestion_artifact)
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation=DataValidation(data_validaton_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
          data_validation_artifact= data_validation.initiate_data_validation()

          #data transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
          data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()

          #model trainer
          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact, model_trainer_config=model_trainer_config)
          model_trainer_artifact = model_trainer.initiate_model_trainer()

          #model evaluation
          model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_eval  = ModelEvaluation(model_eval_config=model_eval_config,
                                        data_ingestion_artifact=data_ingestion_artifact,
                                        data_transformation_artifact=data_transformation_artifact,
                                        model_trainer_artifact=model_trainer_artifact)
          model_eval_artifact = model_eval.initiate_model_evaluation()

     except Exception as e:
          print(e)