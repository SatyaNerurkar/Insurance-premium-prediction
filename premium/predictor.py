import os, sys
import pandas as pd
import numpy as np
from premium.logger import logging
from premium.exception import PremiumException
from premium.utils import load_object
from premium.model_resolver import ModelResolver


class PremiumData:
    def __init__(
        self, 
        age:int, 
        sex:str, 
        bmi:float, 
        children:int, 
        smoker:str, 
        region:str, 
        expenses:float=None):

        try:
            self.age = age
            self.sex = sex
            self.bmi = bmi
            self.children = children
            self.smoker = smoker
            self.region = region
            self.expenses = expenses

        except Exception as e:
            print(e)
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

    def __init__(self):
        self.model_registry="saved_models"

    def predict(self, X):
        try:
            model_resolver = ModelResolver(model_registry=self.model_registry)

            logging.info(f"Loading transformer to transform dataset")
            transformer = load_object(file_path=model_resolver.get_latest_transformer_path())

            logging.info(f"Loading model to make prediction")
            model = load_object(file_path=model_resolver.get_latest_model_path())

            X = transformer.transform(X)

            expenses = model.predict(X)

            print(np.round(expenses,2))
            return np.round(expenses,2)
        except Exception as e:
            raise PremiumException(e, sys)