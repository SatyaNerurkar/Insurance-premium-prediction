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

class ModelTrainerArtifact:...

class ModelEvaluationArtifact:...

class ModelPusherArtifact:...