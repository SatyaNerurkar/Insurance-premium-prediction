import os, sys
from typing import Optional
from premium.logger import logging
from premium.exception import PremiumException
from premium.utils import load_object
from premium.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME

class ModelResolver:

    def __init__(self, 
                model_registry:str = "saved_models", 
                transformer_dir_name="transformer",
                model_dir_name="model"):
        logging.info(f"|{'-'*50}||Model Resolver||{'-'*50}|")
        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.model_dir_name=model_dir_name

    def get_latest_dir_path(self)->Optional[str]:
        """
        Description: This function will fetch latest directory name 
        =====================================================================================
        returns latest directory:String
        """
        try:
            # List out all the saved models in directory
            dir_names = os.listdir(self.model_registry)

            # Check if directory names are greater than 0
            if len(dir_names)==0:
                return None

            # convert sub-folder names into integer for comparison.
            logging.info("Convert sub-folder names into integer for comparison.")
            folder_name = list(map(int, dir_names))

            # Extract latest model directory from all saved models.
            logging.info("Extract latest model directory from all saved models.")
            return os.path.join(self.model_registry, f"{max(folder_name)}")
        except Exception as e:
            raise PremiumException(e, sys)

    def get_latest_model_path(self):
        """
        Description: This function will fetch latest trained model from model directory 
        =====================================================================================
        returns latest trained model
        """
        try:
            # get latest directory
            latest_dir = self.get_latest_dir_path()

            # return error if directory is not available.
            if latest_dir is None:
                raise Exception(f"Model is not available")

            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise PremiumException(e, sys)

    def get_latest_transformer_path(self):
        """
        Description: This function will fetch latest transformer object from transformer directory.
        =====================================================================================
        returns transformer object
        """
        try:
            # get latest directory
            latest_dir = self.get_latest_dir_path()

            # return error if directory is not available.
            if latest_dir is None:
                raise Exception(f"Transformer is not available")

            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise PremiumException(e, sys)

    def get_latest_saved_dir_path(self)->str:
        """
        Description: This function will fetch latest directory name 
        =====================================================================================
        returns latest directory:String
        """
        try:
            # Fetch the latest directory in "saved_model".
            logging.info("Exctract latest model directory from all saved models.")
            latest_dir = self.get_latest_dir_path()

            # Validate if model registry "saved_model" is present or not.
            if latest_dir == None:
                # model registry is not present thus creating it.
                return os.path.join(self.model_registry, f"{0}")

            # Fetch the final component in the latest model directory from all saved models.
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))

            return os.path.join(self.model_registry,f"{latest_dir_num+1}")
        except Exception as e:
            raise PremiumException(e, sys)

    def get_latest_saved_model_path(self):
        """
        Description: This function will fetch latest saved model from model directory 
        =====================================================================================
        returns latest saved model
        """
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise PremiumException(e, sys)

    def get_latest_saved_transformer_path(self):
        """
        Description: This function will fetch latest transformer object from transformer directory.
        =====================================================================================
        returns transformer object
        """
        try:
            latest_dir = self.get_latest_saved_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise PremiumException(e, sys)