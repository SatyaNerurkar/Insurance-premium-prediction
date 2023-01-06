import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from premium.pipeline.training_pipeline import start_training_pipeline

if __name__=="__main__":
     try:
          # initiate training pipeline
          start_training_pipeline()
     except Exception as e:
          raise PremiumException(e, sys)