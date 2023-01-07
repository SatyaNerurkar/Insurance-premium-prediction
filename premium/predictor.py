import os, sys
import pandas as pd
import numpy as np
from premium.logger import logging
from premium.exception import PremiumException


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

    def __init__(self, model_resolver:ModelResolver):
        self.model_resolver = model_resolver

    def predict(self, X):
        try:
            model_path = self.get_latest_save_model_path()
            model = load_object(file_path=model_path)
            expenses = model.predict(X)
            return np.round(expenses,2)
        except Exception as e:
            raise PremiumException(e, sys)