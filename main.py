# from sensor.configuration.mongo_db_connection import MongoDBClient
# from sensor.exception import SensorException
# from sensor.logger import logging
# import sys
# from sensor.constant.env_variable import MONGODB_URL_KEY
# import os
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainingPipeline


if __name__ == '__main__':
    train_pipeline = TrainingPipeline()
    train_pipeline.run_pipeline()

    
    # training_pipline_config = TrainingPipelineConfig()
    # data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipline_config)
    # print(data_ingestion_config.__dict__)

# Exception code working
#     try:
#         test_exception()
#     except Exception as e:
#         print(e)

# Mongodb connection code working without setting env
    # mongodb_client = MongoDBClient() 
    # mongodb_client.database[]
    # print(mongodb_client.database.list_collection_names())

# URL = os.getenv(MONGODB_URL_KEY, None)
# print(URL)

# def test_exception():
#     try :
#         logging.info("We are dividing number by zero")
#         x = 1/0
#     except Exception as e:
#         raise SensorException(e,sys)