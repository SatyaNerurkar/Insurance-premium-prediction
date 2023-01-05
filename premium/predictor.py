import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from premium.utils import load_object
from premium.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME

class PremiumData:
    def ___init__(
        self, age:int, sex:str, bmi:float, children:int, smoker:str, region:str, expenses:float=None):
        try:
            self.age = age
            self.sex = sex
            self.bmi = bmi
            self.children = children
            self.smoker = smoker
            self.region = region
            self.expenses = expenses
        except Exception as e:
            raise PremiumException(e, sys)

    def get_input_data_frame(self):
        try:
            input_dict = self.get_input_data_dict()
            return pd.DataFrame(input_dict)
        except Exception as e:
            raise PremiumException(e, sys)

    def get_input_data_dict(self):
        try:
            input_data = {
                "age": [self.age],
                "sex": [self.sex],
                "bmi": [self.bmi],
                "children": [self.children],
                "smoker": [self.smoker],
                "region": [self.region]}
                
            return input_data
        except Exception as e:
            raise PremiumException(e, sys)


class Predictor:
    def __init__(self, model_registry:str = "saved_models", 
    transformer_dir_name="transformer",
    model_dir_name="model"):
        logging.info(f"|{'-'*50}||Model Trainer||{'-'*50}|")
        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.model_dir_name=model_dir_name

    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_dir_path(self):
        """
        Description: This function will fetch latest directory name 
        =====================================================================================
        returns latest directory
        """
        try:
            # convert sub-folder names into integer for comparison.
            logging.info("Convert sub-folder names into integer for comparison.")
            folder_name = list(map(int, os.listdir(self.model_registry)))

            # Exctract latest model directory from all saved models.
            logging.info("Exctract latest model directory from all saved models.")
            latest_model_dir = os.path.join(self.model_registry, f"{max(folder_name)}")

            return latest_model_dir
        except Exception as e:
            raise PremiumException(e, sys)

    def predict(self, X):
        try:
            model_path = self.get_latest_save_model_path()
            model = load_object(file_path=model_path)
            expenses = model.predict(X)
            return np.round(expenses,2)
        except Exception as e:
            raise PremiumException(e, sys) from e