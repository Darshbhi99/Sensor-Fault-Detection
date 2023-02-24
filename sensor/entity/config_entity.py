'''
This provides configuration of all stages of Training pipeline i.e all the values needed at 
every stage
'''
import os
from dataclasses import dataclass
from datetime import datetime
from sensor.constant.training_pipeline import PIPELINE_NAME, ARTIFACT_DIR
from sensor.constant.training_pipeline import DATA_INGESTION_DIR_NAME, DATA_INGESTION_FEATURE_STORE_DIR
from sensor.constant.training_pipeline import FILE_NAME, DATA_INGESTION_FEATURE_STORE_DIR, TRAIN_FILE_NAME
from sensor.constant.training_pipeline import DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
from sensor.constant.training_pipeline import DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO, DATA_INGESTION_COLLECTION_NAME
from sensor.constant.training_pipeline import DATA_VALIDATION_DIR_NAME, DATA_VALIDATION_VALID_DIR, DATA_VALIDATION_INVALID_DIR
from sensor.constant.training_pipeline import DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
from sensor.constant.training_pipeline import (DATA_TRANSFORMATION_DIR_NAME, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, 
                                                DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_OBJECT_FILE_NAME)
from sensor.constant.training_pipeline import (MODEL_TRAINER_DIR_NAME, MODEL_TRAINER_MODEL_DIR, MODEL_FILE_NAME,
                                                MODEL_TRAINER_EXPECTED_SCORE, MODEL_TRAINER_THRESHOLD)
from sensor.constant.training_pipeline import (MODEL_EVALUATION_DIR_NAME, MODEL_EVALUATION_REPORT_FILE_NAME, 
                                                MODEL_EVALUATION_TRAINED_THRESHOLD_SCORE)
from sensor.constant.training_pipeline import (MODEL_PUSHER_DIR_NAME, MODEL_PUSHER_MODEL_NAME, SAVED_MODEL_DIR_NAME)

timestamp:str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

""" Training pipeline configuration class which contain 
    class attributes converted into object attribute using 
    @dataclass which adds __init__() and __repr__() functions
    to the class"""
@dataclass
class TrainingPipelineConfig:
    pipeline_name:str = PIPELINE_NAME 
    artifact_dir:str = os.path.join(ARTIFACT_DIR, timestamp)
    timestamp = timestamp

# Initialization of Training Pipeline config class
training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig()

# This class will be called in the Data Ingestion file
@dataclass
class DataIngestionConfig:
# artifact folder ---> timestamp ---> data ingestion folder
    data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
# artifact folder ---> timestamp ---> data ingestion folder ---> feature store folder ---> sensor.csv 
    feature_store_file_path: str = os.path.join(
            data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
# artifact folder ---> timestamp ---> data ingestion folder ---> ingested ---> train.csv
    training_file_path: str = os.path.join(
            data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
# artifact folder ---> timestamp ---> data ingestion folder ---> ingested ---> test.csv
    testing_file_path: str = os.path.join(
            data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
# train test split ratio 
    test_split_ratio:float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
# Data ingestion collection name i.e name of collection in mongodB
    collection_name:str = DATA_INGESTION_COLLECTION_NAME

# This class will be called in Data Validation File
@dataclass
class DataValidationConfig:
# artifact folder ---> data_validation folder
    data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
# artifact folder ---> data_validation_dir ---> data_validation_valid_folder
    data_validation_valid_dir: str = os.path.join(
            data_validation_dir, DATA_VALIDATION_VALID_DIR)
# artifact folder --> data_validation_dir ---> data_validation_invalid_folder
    data_validation_invalid_dir: str = os.path.join(
            data_validation_dir, DATA_VALIDATION_INVALID_DIR)
# artifact folder --> data_validation_dir ---> data_validation_valid_dir ---> valid_train_file
    valid_train_file_path: str = os.path.join(
            data_validation_valid_dir, TRAIN_FILE_NAME)
# artifact folder --> data_validation_dir ---> data_validation_valid_dir ---> valid_test_file
    valid_test_file_path: str = os.path.join(
            data_validation_valid_dir, TEST_FILE_NAME)
# artifact folder --> data_validation_dir ---> data_validation_invalid_dir ---> invalid_train_file
    invalid_train_file_path: str = os.path.join(
            data_validation_invalid_dir, TRAIN_FILE_NAME)
# artifact folder --> data_validation_dir ---> data_validation_invalid_dir ---> invalid_test_file
    invalid_test_file_path: str = os.path.join(
            data_validation_invalid_dir, TEST_FILE_NAME)
# artifact folder --> data_validation_dir ---> drift_report
    drift_report_file_path: str = os.path.join(
            data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR, 
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

# This class will be called in Data Transformation file in component folder
@dataclass
class DataTransformationConfig:
# artifact folder ---> data_transformation folder
    data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
# artifact folder ---> data_transformation ---> transformed folder ---> train.npy file
    transformed_train_file_path: str = os.path.join(
            data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TRAIN_FILE_NAME.replace('csv', 'npy'))
# artifact folder ---> data_transformation ---> transformed folder ---> test.npy file
    transformed_test_file_path: str = os.path.join(
            data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TEST_FILE_NAME.replace('csv', 'npy'))
# artifact folder --> data_transformation ---> transformed_object folder ---> object.pkl file
    transformed_object_file_path: str = os.path.join(
            data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_OBJECT_FILE_NAME)

# This class will be called in Model Trainer File
@dataclass
class ModelTrainerConfig:
# artifact folder ---> model_trainer folder
    model_trainer_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
# artifact folder --> model_trainer folder --> trained_model folder --> trained model pkl file
    trained_model_file_path: str = os.path.join(
        model_trainer_dir, MODEL_TRAINER_MODEL_DIR, MODEL_FILE_NAME)
# Accuracy with which model will be checked
    expected_accuracy:float = MODEL_TRAINER_EXPECTED_SCORE
# Accuracy with which overfitting and underfitting will be checked
    over_fitting_under_fitting_threshold:float = MODEL_TRAINER_THRESHOLD

# This data will be called in Model Evaluation File
@dataclass
class ModelEvaluationConfig:
# artifact folder ---> model_evaluation
    model_evaluation_dir: str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_EVALUATION_DIR_NAME)
# artifact folder ---> model_evaluation ---> report.yaml
    model_evaluation_report_file_path:str = os.path.join(
        model_evaluation_dir, MODEL_EVALUATION_REPORT_FILE_NAME)
# Model evaluation trained threshold 
    model_evaluation_train_threshold:float = MODEL_EVALUATION_TRAINED_THRESHOLD_SCORE

# This data will be called in Model Pusher File
@dataclass
class ModelPusherConfig:
# artifact folder ---> model_pusher folder
    model_pusher_dir:str = os.path.join(
        training_pipeline_config.artifact_dir, MODEL_PUSHER_DIR_NAME)
# artifact folder ---> model_pusher folder ---> model.pkl
    pushed_model_file_path:str = os.path.join(
        model_pusher_dir, MODEL_PUSHER_MODEL_NAME)
# saved_model folder ---> timestamp
    saved_model_dir:str = os.path.join(SAVED_MODEL_DIR_NAME, timestamp)
# saved_model folder ---> timestamp folder ---> model.pkl
    saved_model_file_path:str = os.path.join(
        saved_model_dir, MODEL_FILE_NAME)