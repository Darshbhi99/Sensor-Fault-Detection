'''
This python file provides you code for starting/execution of whole Training pipeline i.e
Data Ingestion, Data Validation, Data Transformation, Model Training, Data Evaluation and Model Pusher
'''
from sensor.entity.config_entity import (DataIngestionConfig, DataValidationConfig, DataTransformationConfig)
from sensor.exception import SensorException
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.logger import logging
import sys
import warnings
warnings.filterwarnings('ignore')


# Training pipeline class will be called by main file
class TrainingPipeline:
    def __init__(self):
        # Initializing the Data Configuration from the  entity --> config_entity file
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()

    def start_data_ingestion(self) ->DataIngestionArtifact: 
        try:
            logging.info('Starting Data Ingestion')
            # Initialising the Data Ingestion class from components --> data ingestion file
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            # Starting the data Ingestion process by calling a function from data ingestion file
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info(f'Data Ingestion Completed with {self.data_ingestion_config.feature_store_file_path}')
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info("Starting Data Validation")

            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                                data_validation_config=self.data_validation_config)
            # Starting the Data Validation Process by calling the function from data validation file
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data Validation Completed")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("Starting Data Transformation")

            data_transform = DataTransformation(data_validation_artifact=data_validation_artifact,
                                                data_transformation_config=self.data_transformation_config)
            # Starting the Data Transformation Process by calling the function from the data transformation file
            data_transformed_artifact = data_transform.initiate_data_transformation()

            logging.info("Data Transformation Completed")
            return data_transformed_artifact
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
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
        except Exception as e:
            raise SensorException(e,sys)