'''
This python file provides you code for starting/execution of whole Training pipeline i.e
Data Ingestion, Data Validation, Data Transformation, Model Training, Data Evaluation and Model Pusher
'''
from sensor.entity.config_entity import (DataIngestionConfig, DataValidationConfig, 
                                        DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, 
                                        ModelPusherConfig)
from sensor.exception import SensorException
from sensor.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, 
                                        ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact)
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evalution import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
from sensor.logger import logging
import sys
import warnings
warnings.filterwarnings('ignore')


# Training pipeline class will be called by main file
class TrainingPipeline:
    is_pipeline_running = False
    def __init__(self):
        # Initializing the Data Configuration from the  entity --> config_entity file
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

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

    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info('Starting the Model Training')
            model_trainer = ModelTrainer(model_trainer_config = self.model_trainer_config, 
                                    data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_training()
            logging.info('Model Training Completed')
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_evaluation(self, model_trainer_artifact:ModelTrainerArtifact,
                                    data_validation_artifact:DataValidationArtifact) -> ModelEvaluationArtifact:
        try:
            logging.info('Starting the Model Evaluation')
            model_evaluation = ModelEvaluation(model_evaluation_config=self.model_evaluation_config,
                                            data_validation_artifact=data_validation_artifact, 
                                            model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info('Model Evaluation Completed')
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e,sys)
    
    def start_model_pusher(self, model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            logging.info('Starting the Model Pusher')
            model_pusher = ModelPusher(model_pusher_config=self.model_pusher_config, 
                                        model_evaluation_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info('Model Pusher Ended')
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running = True
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact = self.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact:ModelEvaluationArtifact = self.start_data_evaluation(model_trainer_artifact, 
                                                                                    data_validation_artifact)
            model_pusher_artifact:ModelPusherArtifact = self.start_model_pusher(model_evaluation_artifact)
            TrainingPipeline.is_pipeline_running = False
            return model_pusher_artifact
        except Exception as e:
            TrainingPipeline.is_pipeline_running = False
            raise SensorException(e,sys)