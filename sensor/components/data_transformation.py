import sys, os
import pandas as pd
import numpy  as np
# This simple imputer for missing values
from sklearn.impute import SimpleImputer
# This robust scaler for scaling the data in IQR method
from sklearn.preprocessing import RobustScaler
# This SMOTETomek for filling the minority with non duplicate data for imbalalancing the data
from imblearn.combine import SMOTETomek
# This pipeline for running the process in steps
from sklearn.pipeline import Pipeline

from sensor.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.utils.main_utils import save_numpy_array_data, save_object
from sensor.ml.model.estimator import TargetValueMapping
import warnings
warnings.filterwarnings('ignore')


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, 
                        data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise SensorException(e, sys)
    
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            raise SensorException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            robust = RobustScaler()
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            preprocessor = Pipeline(steps=[
                ('imputer', simple_imputer),
                ('scaler', robust)])
            return preprocessor
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_trained_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            preprocessor = self.get_data_transformer_object()
            
            logging.info('Seperating the Independent and Dependent Data')
            # Splitting Training Data into Input and Target Data
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            # Converting the categorical Target columns into numerical
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())
            
            # Splitting Testing Data into Input and Target Data
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            # Converting the categorical Target columns into numerical
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())
            
            logging.info('Fitting the preprocessing pipeline to the data')
            # Fitting the Pipeline for both train and test data
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            logging.info('Balancing the Data using SMOTETomek')
            # Fitting the train and test data to balance the data
            smt = SMOTETomek(sampling_strategy='minority')
            input_feature_train_final, target_feature_train_final = smt.fit_resample(transformed_input_train_feature, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(transformed_input_test_feature, target_feature_test_df)
            
            # Concatinating the array from the balanced data
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]

            logging.info('Saving the Transformed Data')
            # Saving the transformed data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)
            
            logging.info(f'Transformed Data Array saved at {self.data_transformation_config.data_transformation_dir} \
                and Preproccessing object at {self.data_transformation_config.transformed_object_file_path}')
            # Data Transformation Artifact 
            data_transformation_artifact = DataTransformationArtifact(
                                            transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                                            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                                            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path)
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)