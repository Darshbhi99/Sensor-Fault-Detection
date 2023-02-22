''' 
In this file  all function which will perform data ingestion are written
Finally a initialization function is called in training pipeline
'''
import os
import sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sensor.constant.training_pipeline import SCHEMA_DROP_COLS, SCHEMA_FILE_PATH
from sensor.data_access.sensor_data import SensorData
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.entity.config_entity import DataIngestionConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file
import warnings
warnings.filterwarnings('ignore')

class DataIngestion:
    '''
    Gets all the data ingestion configurations from the entity --> config_entity file
    '''
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   Convert the MongodB Data into Dataframe and saves it in the feature Store folder 
        
        Output      :   Folder is created in the system with Data in Dataframe form
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        try:
            logging.info(f"Exporting data from mongodb")
            # Calling the class from data_access folder which will connect MongodB Server
            sensor_data = SensorData()
            # Calling the function from the sensor data class to convert data into dataframe
            dataframe = sensor_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name)
            # Getting the data 
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            # Getting the filepath with filename where csv file to be stored
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Getting the directory name for this filepath
            dir_path = os.path.dirname(feature_store_file_path)
            # Create the directory 
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            # Saving the file in the filepath
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe
        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.test_split_ratio)

            logging.info(f"Performed train test split with train shape {train_set.shape} and test shape {test_set.shape}")

            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True)

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True)

        except Exception as e:
            raise SensorException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            # Calling the export feature store function  
            dataframe = self.export_data_into_feature_store()
            # Getting the dataframe
            logging.info("Got the data from mongodb")
            # reading the schema yaml file from main_utils file in utils folder
            _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            # Dropping the columns from the dataframe
            dataframe = dataframe.drop(_schema_config[SCHEMA_DROP_COLS], axis=1)
            # Calling the split function inside the dataframe
            self.split_data_as_train_test(dataframe)
            # Done with splitting and saving the data 
            logging.info("Performed train test split on the dataset")
            # Completed the data ingestion processes
            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,)

            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys) from e
