'''
This file contain class and functions which will be used only in Machine Learning Model Training 
'''
from sensor.exception import SensorException
from sensor.constant.training_pipeline import SAVED_MODEL_DIR_NAME, MODEL_FILE_NAME
import numpy as np
import os, sys
import warnings
warnings.filterwarnings('ignore')


class TargetValueMapping:
    def __init__(self):
        self.neg:int = 0
        self.pos:int = 1

    def to_dict(self)->dict:
        return self.__dict__
    
    def reverse_mapping(self) -> dict:
        mapping_response:dict = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


# This class is the prediction class which will be called in the model trainer file
class SensorModel:
    def __init__(self, model, preprocessor):
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise SensorException(e, sys)
        
    def predict(self, X) ->np.array:
        try:
            X_transform = self.preprocessor.transform(X)
            y_hat = self.model.predict(X_transform)
            return y_hat
        except Exception as e:
            SensorException(e, sys)


# This class will be used in model_evalaution file
class ModelResolver:
    def __init__(self, model_dir=SAVED_MODEL_DIR_NAME):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SensorException(e, sys)
    
    def get_latest_model_path(self) ->str:
        try:
            timestamps = list(map(int, os.listdir(self.model_dir)))
            latest_timestamp = np.argmax(timestamps)
            latest_model = os.path.join(self.model_dir, f'{os.listdir(self.model_dir)[latest_timestamp]}', MODEL_FILE_NAME)
            return latest_model
        except Exception as e:
            raise SensorException(e, sys)

    def is_model_exist(self) ->bool:
        try:
            # Directory exist or not
            if os.path.exists(self.model_dir):
                # Models in directory exist or not
                timestamp = os.listdir(self.model_dir)
                if len(timestamp)==0:
                    return False
                else:
                    return True
        except Exception as e:
            raise SensorException(e, sys)