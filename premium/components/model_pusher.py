import os,sys
from premium.logger import logging
from premium.exception import PremiumException
from premium.utils import load_object, save_object
from premium.entity import config_entity, artifact_entity
from premium.model_resolver import ModelResolver


class ModelPusher:

    def __init__(self, 
    model_pusher_config:config_entity.ModelPusherConfig, 
    data_transformation_artifact:artifact_entity.DataTransformationArtifact, 
    model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise PremiumException(e, sys)

    def initiate_model_pusher(self)->artifact_entity.ModelPusherArtifact:
        try:
            # load objects
            logging.info("Loading transformer and model object")
            transformer = load_object(file_path=self.data_transformation_artifact.transformer_object_dir)
            model = load_object(file_path=self.model_trainer_artifact.model_dir)

            # model pusher dir
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)

            #saved model dir
            logging.info(f"Saving model in saved model dir")
            model_path = self.model_resolver.get_latest_saved_model_path()
            transformer_path = self.model_resolver.get_latest_saved_transformer_path()

            save_object(file_path=model_path , obj=model)
            save_object(file_path=transformer_path, obj=transformer)

            logging.info("Preparing model pusher artifact")
            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.model_pusher_dir,
             saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")

            return model_pusher_artifact

        except Exception as e:
            raise PremiumException(e, sys)