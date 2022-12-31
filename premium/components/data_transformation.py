import os, sys
import pandas as pd
import numpy as np
from premium import utils
from premium.logger import logging
from premium.exception import PremiumException
from premium.entity import config_entity, artifact_entity

class DataTransformation:
    
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig, data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"|{'-'*50}|| Data Trasnformation ||{'-'*50}|")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise PremiumException(e, sys)

    
    