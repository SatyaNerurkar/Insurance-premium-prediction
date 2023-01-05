# Define output for each component as artifact.
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformer_object_dir:str
    transformed_train_dir:str
    transformed_test_dir:str

@dataclass
class ModelTrainerArtifact:
    model_dir:str
    train_root_mean_squared_error:float
    test_root_mean_squared_error:float
    model_accuracy:float
    train_accuracy_score:float
    test_accuracy_score:float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float

class ModelPusherArtifact:...