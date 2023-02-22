from sensor.exception import SensorException
from sensor.logger import logging
import numpy as np
import sys, os
import yaml
import dill
import warnings
warnings.filterwarnings('ignore')


# This function will be called in data ingestion file in components folder
def read_yaml_file(file_path:str) ->dict:
    '''
    This function will read the schema.yaml file 
    '''
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SensorException(e, sys)


def write_yaml_file(file_path:str, content:object, replace:bool=False) ->None:
    '''This function will be used in data validation for data drift report writing
        keep replace = True if directory is not created 
    ''' 
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                yaml.dump(content, file)
    except Exception as e:
        raise SensorException(e, sys)


def save_object(file_path:str, obj:object) -> None:
    '''
    Save the transformation object as pickle file
    '''
    logging.info('Entering the save object method of main_utils class')
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            dill.dump(obj, f)
        logging.info('Exiting from the save object method of main_utils class')
    except Exception as e:
        raise SensorException(e, sys)


def save_numpy_array_data(file_path:str, array: np.array) -> None:
    '''
    Save the csv data into numpy array
    '''
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            np.save(f, array)
    except Exception as e:
        raise SensorException(e, sys)


def load_numpy_array_data(file_path:str) -> np.array:
    '''
    load the csv data into numpy array
    '''
    try:
        with open(file_path, 'rb') as f:
            return np.load(f)
    except Exception as e:
        raise SensorException(e, sys)
