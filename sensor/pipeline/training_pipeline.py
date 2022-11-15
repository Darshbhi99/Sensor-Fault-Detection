'''
This python file provides you code for starting/execution of whole Training pipeline i.e
Data Ingestion, Data Validation, Data Transformation, Model Training, Data Evaluation and Model Pusher
'''
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.exception import SensorException
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.logger import logging
import sys, os

# Training pipeline 
class TrainingPipeline:
    def __init__(self):
        # Initialising the Training pipeline config class
        training_pipeline_config = TrainingPipelineConfig()
        # Getting the configuration for training data
        self.training_pipeline_config = training_pipeline_config

    def start_data_ingestion(self) ->DataIngestionArtifact: 
        try:
            logging.info('Starting Data Ingestion')
            # Initialising the Data Ingestion Config class 
            self.data_ingestion_config = DataIngestionConfig(
                    training_pipeline_config= self.training_pipeline_config)
            # Initialising the Data Ingestion Class
            self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            # Starting the data Ingestion 
            self.data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
            logging.info(f'Data Ingestion Completed with {self.data_ingestion_config.feature_store_file_path}')
            return self.data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
            self.data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e:
            raise SensorException(e,sys)