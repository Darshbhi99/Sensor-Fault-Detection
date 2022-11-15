'''
This is the code for Data Ingestion component i.e it will provide code for Ingestion of Data
'''
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sensor.constant.database import COLLECTION_NAME
from sklearn.model_selection import train_test_split
from pandas import DataFrame 
import os, sys

class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            # Initialising the Data Ingestion Config Class 
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        '''
        This function will export data from Mongodb collection into 
        feature store directory as Dataframe
        '''
        try:
            logging.info('Exporting Data from Mongodb into feature store')
            # Initialising the Sensor Data Class
            self.sensor_data = SensorData()
            # Getting the Dataframe from the Sensor Data Class
            self.dataframe = self.sensor_data.export_collection_as_dataframe(
                                        collection_name=COLLECTION_NAME)
            # Getting the filepath for the feature Directory
            self.feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Getting the Directory name for the feature store file
            self.dir_path = os.path.dirname(self.feature_store_file_path)
            # Creating the directory
            os.makedirs(self.dir_path, exist_ok=True)
            # Converting the dataframe into csv and storing it into feature_store_file_path
            self.dataframe.to_csv(self.feature_store_file_path, index=False, header=True)
            return self.dataframe
        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self, dataframe:DataFrame) -> None:
        '''
        This function will split the feature stored Dataset into train and test
        Transfer the Train and Test Dataset to their file path
        '''
        try:
            train_set, test_set = train_test_split(dataframe, 
                                                test_size=self.data_ingestion_config.test_split_ratio)
            logging.info("Performed Train Test Split on the dataframe")
            logging.info("Exited from the train_test_split method of Data Ingestion Class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exporting Training and Testing Data")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info('Exported the Train and Test Data Successfully')
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        '''
        This function will perform the ingestion operation which will output 
        Data Ingestion Artifact
        '''
        try:
            self.dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(self.dataframe)
            DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                    test_file_path=self.data_ingestion_config.testing_file_path)
            return DataIngestionArtifact
        except Exception as e:
            raise SensorException(e, sys)


