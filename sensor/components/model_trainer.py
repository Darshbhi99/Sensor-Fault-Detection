from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.utils.main_utils import load_numpy_array_data, save_object, load_object
from sensor.ml.metrics.classification_metrics import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.exception import SensorException
from sensor.logger import logging
from xgboost import XGBClassifier
import numpy as np
import sys, os
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer():
    def __init__(self, data_transformation_artifact:DataTransformationArtifact,
                model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise SensorException(e, sys)
    
    def train_model(self, x_train:np.array, y_train:np.array):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train, y_train)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_training(self) ->ModelTrainerArtifact:
        try:
            logging.info('Loading the Train Array and Test Array')
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            logging.info('Splitting the data into Dependent and Independent Data')
            X_train, y_train, X_test, y_test = (train_arr[:,:-1], train_arr[:, -1], test_arr[:, :-1], test_arr[:, -1])
            
            logging.info('Training the Model')
            model = self.train_model(X_train, y_train)
            
            logging.info('Predicting using the model')
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            
            logging.info('Calculating the Accuracy')
            cls_train_metric = get_classification_score(y_true=y_train, y_pred=train_pred)
            
            logging.info('Checking the training accuracy with expected accuracy')
            if cls_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise SensorException('The Accuracy of the model is less than the expected accuracy')
            # Get the test data accuracy 
            cls_test_metric = get_classification_score(y_true=y_test, y_pred=test_pred)
            
            logging.info('Checking if model is Overfitting or Underfitting')
            diff = abs(cls_train_metric.f1_score - cls_test_metric.f1_score)
            if diff>=self.model_trainer_config.over_fitting_under_fitting_threshold:
                raise Exception('Model is not good try to do more experimentation')
            
            # Loading the Preprocessor and Model Prediction Class
            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
            sensor_model = SensorModel(model=model, preprocessor=preprocessor)
            
            #Saving the model into directory in which a prediction function will be used further
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            save_object(self.model_trainer_config.trained_model_file_path, sensor_model)
            logging.info(f'Saved the Model at {self.model_trainer_config.trained_model_file_path}')

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                            train_metric_artifact=cls_train_metric, 
                                                            test_metric_artifact=cls_test_metric)
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)