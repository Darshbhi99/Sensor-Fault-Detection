from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.exception import SensorException
import sys, os
# from sensor.configuration.mongo_db_connection import MongoDBClient
# from sensor.logger import logging
# from from_root import from_root
# from sensor.entity.config_entity import (TrainingPipelineConfig, DataIngestionConfig, 
#                                         DataValidationConfig)
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


if __name__ == '__main__':
    try:
        training = TrainingPipeline()
        training.run_pipeline()
    except Exception as e:
        raise SensorException(e, sys)
    