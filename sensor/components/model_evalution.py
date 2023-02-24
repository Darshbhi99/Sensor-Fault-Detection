from sensor.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from sensor.entity.config_entity import ModelEvaluationConfig
from sensor.ml.metrics.classification_metrics import get_classification_score
from sensor.utils.main_utils import load_object, write_yaml_file, load_numpy_array_data
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.ml.model.estimator import SensorModel, ModelResolver, TargetValueMapping
import pandas as pd
import os,sys
import warnings
warnings.filterwarnings('ignore')

class ModelEvaluation:
    def __init__(self,model_evaluation_config:ModelEvaluationConfig,data_validation_artifact:DataValidationArtifact, 
                    model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)


    def initiate_model_evaluation(self):
        try:
            logging.info('Loading the Valid Train data')
            test_file_path = self.data_validation_artifact.valid_test_file_path
            
            # Seperating the Dependent and Independent Data 
            test_df = pd.read_csv(test_file_path)
            
            logging.info('Splitting the data into Dependent and Independent Data')
            # X_train, y_train = (train_arr[:,:-1], train_arr[:, -1])
            X = test_df.drop(TARGET_COLUMN, axis=1)
            y = test_df[TARGET_COLUMN].replace(TargetValueMapping().to_dict())
            
            # Current Model File path
            current_model_file_path:str = self.model_trainer_artifact.trained_model_file_path

            # Initializing the Function which will find the previous pushed model
            model_exist = ModelResolver()
            is_model_accepted:bool = True
            
            # Checking if any previous model is pushed
            if not model_exist.is_model_exist():
                model_evaluation_artifact = ModelEvaluationArtifact(
                                                        is_model_accepted=is_model_accepted,
                                                        improved_accuracy = None,
                                                        best_model_file_path=current_model_file_path,
                                                        trained_model_path=current_model_file_path,
                                                        train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                                                        best_model_metric_artifact=None)
                logging.info('Current Model is the Best Model')
            else:
                logging.info('Checking the Best Model between Latest and Previous Trained Model')
                # Get Latest Previous Model from the Model Directory 
                latest_model_path = model_exist.get_latest_model_path()
                
                # Load the previous latest Model Saved
                latest_model = load_object(latest_model_path)
                current_model = load_object(current_model_file_path)
                
                # Loading the Preprocessor and Model Prediction Class
                # preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
                # latest_model = SensorModel(model=latest_model, preprocessor=preprocessor)
                # current_model = SensorModel(model=current_model, preprocessor=preprocessor)

                # Predicting the Model
                current_pred = current_model.predict(X)
                latest_pred = latest_model.predict(X)
                
                # Get the Metrics
                current_metrics = get_classification_score(y_true=y.values, y_pred=current_pred)
                latest_metrics = get_classification_score(y_true=y.values, y_pred=latest_pred)
                
                # Finding the Difference between the Accuracy
                improved_accuracy = current_metrics.f1_score-latest_metrics.f1_score
                
                # Checking if Sufficient Diffference in accuracy exist
                if (improved_accuracy)>=self.model_evaluation_config.model_evaluation_train_threshold:
                    is_model_accepted = True
                    best_model_file_path = current_model_file_path
                else:
                    is_model_accepted = False
                    best_model_file_path = latest_model_path
                
                logging.info(f'The Difference Between Current and Latest Models is {improved_accuracy}')
                
                # Saving the Model Evaluation Artifact
                model_evaluation_artifact = ModelEvaluationArtifact(
                                                        is_model_accepted=is_model_accepted,
                                                        improved_accuracy = float(improved_accuracy),
                                                        best_model_file_path=best_model_file_path,
                                                        trained_model_path=current_model_file_path,
                                                        train_model_metric_artifact=current_metrics,
                                                        best_model_metric_artifact=latest_metrics)
                logging.info('Saving the report for Evaluation')
            
            # Converting the Artifact into Dictionary
            model_eval_report = model_evaluation_artifact.__dict__
            
            # Saving the evaluation report in yaml file
            os.makedirs(self.model_evaluation_config.model_evaluation_dir, exist_ok=True)
            write_yaml_file(self.model_evaluation_config.model_evaluation_report_file_path, 
                                content=model_eval_report, replace=True)
            
            return model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)