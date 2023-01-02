import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from premium import utils
from premium.entity import config_entity,artifact_entity

class ModelTrainer:
    
    def __init__(self, data_transformation_artifact:artifact_entity.data_transformation_artifact, model_trainer_config:config_entity.ModelTrainerConfig):
        try:
            logging.info(f"|{'-'*50}||Model Trainer||{'-'*50}|")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise PremiumException(e, sys)

    def train_model(self, x, y):
        """
        Description: This function will train the machine learning model on training dataset.
        ====================================================================================
        x: Accepts x train array
        y: Accepts y train array
        =====================================================================================
        returns machine learning model
        """
        try:
            # creating Gradient Boosting Regressor object.

            {'learning_rate': 0.05, 'max_depth': 2, 'n_estimators': 200}

            final_model = GradientBoostingRegressor(n_estimators=200, 
                                        max_depth=2,
                                        learning_rate=0.05)
            pass
        except Exception as e:
            raise PremiumException(e, sys)


    def fine_tune(self, model):
        # Define the hyperparameter grid
        param_grid = {
                    'learning_rate': [0.01, 0.05, 0.1, 0.5, 1, 1.5],
                    'n_estimators': [50, 100, 150, 200, 250, 300, 350],
                    'max_depth': [2, 3, 4, 5, 6, 7, 8, 9]}

        # Create a GridSearchCV object
        grid_search = GridSearchCV(model, param_grid, cv=5)
        
        # Fit the model
        grid_search.fit(self.X, self.y)
        
        # Return the best hyperparameters
        return grid_search.best_params_