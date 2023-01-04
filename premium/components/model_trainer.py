import os, sys
import numpy as np
from premium.logger import logging
from premium.exception import PremiumException
from premium import utils
from premium.entity import config_entity,artifact_entity
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score,mean_squared_error

class ModelTrainer:
    
    def __init__(self, data_transformation_artifact:artifact_entity.DataTransformationArtifact, model_trainer_config:config_entity.ModelTrainerConfig):
        try:
            logging.info(f"|{'-'*50}||Model Trainer||{'-'*50}|")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model = None
            self.best_params_ = None
            self.x=None
            self.y=None
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
            logging.info("creating Gradient Boosting Regressor object.")
            model = GradientBoostingRegressor()
        
            # Find the best hyperparameters.
            logging.info("Find the best hyperparameters.")
            self.best_params_ = self.fine_tune(model, x, y)
        
            # Train the model with the best hyperparameters
            logging.info("Train the model with the best hyperparameters.")
            logging.info(f"best hyperparameters: {self.best_params_}")
            self.model = model.set_params(**self.best_params_)

            # fit the train data.
            self.model.fit(x, y)

            return model

        except Exception as e:
            raise PremiumException(e, sys)


    def fine_tune(self, model, x, y):
        # Define the hyperparameter grid
        logging.info("Define the hyperparameter grid.")
        param_grid = {
                    'learning_rate': [0.01, 0.05, 0.1, 0.5, 1, 1.5],
                    'n_estimators': [50, 100, 150, 200, 250, 300, 350],
                    'max_depth': [2, 3, 4, 5, 6, 7, 8, 9]}

        # Create a GridSearchCV object
        logging.info("Create a GridSearchCV object.")
        grid_search = GridSearchCV(model, param_grid, cv=5)
        
        # Fit the grid search model
        logging.info("Fit the grid search model.")
        grid_search.fit(x, y)
        
        # Return the best hyperparameters
        return grid_search.best_params_


    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        """
        Description: This function will trigger training machine learning model.
        ====================================================================================
        returns nachine learning model artifact
        """
        try:
            # Loading train and test array.
            logging.info(f"Loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_dir)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_dir)

            # Splitting input and target feature from both train and test arr.
            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            # Train the model
            logging.info(f"Train the model")
            model = self.train_model(x=x_train, y=y_train)

            # Calculating train accuracy score R2
            logging.info(f"Calculating R2 train accuracy score")
            yhat_train = model.predict(x_train)
            train_accuracy_score = round((r2_score(y_true = y_train,y_pred= yhat_train))*100,3)
            train_root_mean_squared_error = np.sqrt(mean_squared_error(y_true = y_train,y_pred = yhat_train))

            # Calculating test accuracy score R2
            logging.info(f"Calculating R2 train accuracy score")
            yhat_test = model.predict(x_test)
            test_accuracy_score = round((r2_score(y_true = y_test,y_pred= yhat_test))*100,3)
            test_root_mean_squared_error = np.sqrt(mean_squared_error(y_true = y_test,y_pred = yhat_test))
            
            logging.info(f"train score:{train_accuracy_score} and tests score {test_accuracy_score}") 
            logging.info(f"train rmse:{train_root_mean_squared_error} and test rmse {test_root_mean_squared_error}")

            # matching current accuracy with the threshold.
            logging.info(f"matching current accuracy with the threshold.")
            if test_accuracy_score<self.model_trainer_config.base_accuracy:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.base_accuracy}: model actual score: {test_accuracy_score}")

            logging.info(f"Current accuracy is better than threshold.")
            # save the trained model
            logging.info(f"Saving model object at {self.model_trainer_config.model_dir}")
            utils.save_object(file_path=self.model_trainer_config.model_dir, obj=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact( 
                model_dir=self.model_trainer_config.model_dir,
                train_root_mean_squared_error=train_root_mean_squared_error,
                test_root_mean_squared_error=test_root_mean_squared_error,
                model_accuracy=test_accuracy_score,
                train_accuracy_score=train_accuracy_score,
                test_accuracy_score=test_accuracy_score)

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
   
        except Exception as e:
            raise PremiumException(e, sys)