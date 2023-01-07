import os, sys
import pandas as pd
import numpy as np
from premium.logger import logging
from premium.exception import PremiumException
from premium.utils import load_object
from premium.entity import config_entity, artifact_entity
from premium.model_resolver import ModelResolver
from sklearn.metrics import r2_score,mean_squared_error
from premium.config import TARGET_COLUMN

class ModelEvaluation:
    def __init__(self, 
    model_eval_config:config_entity.ModelEvaluationConfig, 
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
    data_transformation_artifact:artifact_entity.DataTransformationArtifact,
    model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
    ):
        try:
            logging.info(f"|{'-'*50}||Model Evaluation||{'-'*50}|")
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


            # Fetch location of transformer and model
            logging.info("Fetch location of transformer and model")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()

            # Load previous trained model objects
            logging.info("Load previous trained objects of transformer, model and target encoder")
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)

            # Model trained in current run.
            logging.info("Load previous trained objects of transformer, model and target encoder")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transformer_object_dir)
            current_model = load_object(file_path=self.model_trainer_artifact.model_dir)

            # load "test.csv" for evaluation of both models
            logging.info('load "test.csv" for evaluation of both models')
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]

            # accuracy using previous trained model
            input_feature_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            logging.info(f"Prediction using previous model: {y_pred[:5]}")

            previous_model_accuracy_score = round((r2_score(y_true = target_df,y_pred= y_pred))*100,3)
            previous_model_root_mean_squared_error = np.sqrt(mean_squared_error(y_true = target_df,y_pred= y_pred))
            
            logging.info(f"previously trained model accuracy score:{previous_model_accuracy_score} and root mean squared error: {previous_model_root_mean_squared_error}")

            # accuracy using current trained model
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            logging.info(f"Prediction using current model: {y_pred[:5]}")

            current_model_accuracy_score = round((r2_score(y_true = target_df,y_pred= y_pred))*100,3)
            previous_model_root_mean_squared_error = np.sqrt(mean_squared_error(y_true = target_df,y_pred= y_pred))
            
            logging.info(f"currently trained model accuracy score:{current_model_accuracy_score} and root mean squared error: {previous_model_root_mean_squared_error}")

            # Compare both accuracies 
            logging.info("Compare both accuracies")
            if current_model_accuracy_score<=previous_model_accuracy_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_accuracy_score-previous_model_accuracy_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
        
        except Exception as e:
            raise PremiumException(e, sys)

