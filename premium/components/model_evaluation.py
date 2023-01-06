import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from premium.entity import config_entity, artifact_entity
from premium.predictor import Predictor, ModelResolver

class ModelEvaluation:
    def __init__(self, 
    model_eval_config:config_entity.ModelEvaluationConfig, 
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
    data_transformation_artifact:artifact_entity.DataTransformationArtifact,
    model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
    ):
        try:
            logging.info(f"|{'-'*50}||Model Trainer||{'-'*50}|")
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise PremiumException(e, sys)


    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            # If saved model is present do a quick comparison of which one is best trained model.
            logging.info("Comparing trined model")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                # There is no model available for comparison. Setting method output parameters to none
                logging.info("There is no model available for comparison. Setting method output parameters to none")
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                return model_eval_artifact
        
        except Exception as e:
            raise PremiumException(e, sys)

