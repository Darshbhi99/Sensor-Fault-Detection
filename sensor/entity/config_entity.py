'''
This provides configuration of all stages of Training pipeline i.e all the values needed at 
every stage
'''
import os
from datetime import datetime
from sensor.constant.training_pipeline import PIPELINE_NAME, ARTIFACT_DIR
from sensor.constant.training_pipeline import DATA_INGESTION_DIR_NAME, DATA_INGESTION_FEATURE_STORE_DIR
from sensor.constant.training_pipeline import FILE_NAME, DATA_INGESTION_FEATURE_STORE_DIR, TRAIN_FILE_NAME
from sensor.constant.training_pipeline import DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
from sensor.constant.training_pipeline import DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO, DATA_INGESTION_COLLECTION_NAME

# Training pipeline configuration class
class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.pipeline_name:str = PIPELINE_NAME 
        timestamp:str = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_dir:str = os.path.join(ARTIFACT_DIR, timestamp)
        self.timestamp = timestamp

# Data Ingestion configuration class
class DataIngestionConfig:
    def __init__(self, training_pipeline_config = TrainingPipelineConfig):
# training folder ---> artifact folder ---> data ingestion folder
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
# training folder ---> artifact folder ---> data ingestion folder ---> feature store folder ---> sensor.csv
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
# training folder ---> artifact folder ---> data ingestion folder ---> train.csv
        self.training_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
# training folder ---> artifact folder ---> data ingestion folder ---> test.csv
        self.testing_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
# train test split ratio 
        self.test_split_ratio:float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
# Data ingestion collection name
        self.collection_name:str = DATA_INGESTION_COLLECTION_NAME
