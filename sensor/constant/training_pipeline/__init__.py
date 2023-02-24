import os
from sensor.constant.s3_bucket import TRAINING_BUCKET_NAME
import warnings
warnings.filterwarnings('ignore')


# Defining common constant variable for training pipeline
TARGET_COLUMN = 'class'
PIPELINE_NAME:str = 'sensor'
ARTIFACT_DIR:str = 'artifact'
FILE_NAME:str = 'sensor.csv'
TRAIN_FILE_NAME:str = 'train.csv'
TEST_FILE_NAME:str = 'test.csv'

PREPROCESSING_OBJECT_FILE_NAME = 'preprocessing.pkl'
MODEL_FILE_NAME = 'model.pkl'
SCHEMA_FILE_PATH = os.path.join('config','schema.yaml')
SCHEMA_DROP_COLS = "drop_columns"

# Data Ingestion related constant start with DATA_INGESTION VAR NAME
DATA_INGESTION_COLLECTION_NAME:str = 'car'
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature store"
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:str = 0.2

# Data Validation related constant start with DATA_VALIDATION VAR NAME
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

# Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object" 

# Model Training related constant start with MOD_TRAINER VAR NAME
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6 
MODEL_TRAINER_THRESHOLD:float = 0.05

# Model Evaluation related constant starts with MODEL_EVALUATION VAR NAME
MODEL_EVALUATION_DIR_NAME:str = "model_evaluation"
MODEL_EVALUATION_TRAINED_THRESHOLD_SCORE:float = 0.02
MODEL_EVALUATION_REPORT_FILE_NAME:str = "report.yaml" 

# Model Pusher related constants starts with MODEL_PUSHER VAR NAME
MODEL_PUSHER_DIR_NAME :str = "model_pusher"
MODEL_PUSHER_MODEL_NAME:str = MODEL_FILE_NAME

# This constant will be used in ml folder model folder estimator file
SAVED_MODEL_DIR_NAME = os.path.join('saved_models')
