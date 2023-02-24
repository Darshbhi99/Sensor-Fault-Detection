from dataclasses import dataclass

'''
This class gives you input  output of all stages of training pipeline
@dataclass creates an constructor around the class attributes which 
will be used by object of that class as well 
'''
@dataclass
class DataIngestionArtifact:
    trained_file_path:str 
    test_file_path:str 

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_trained_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path:str
    transformed_test_file_path:str
    transformed_object_file_path:str

@dataclass
class ClassificationMetricArtifact:
    f1_score:str
    precision_score:str
    recall_score:str

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float
    best_model_file_path:str
    trained_model_path:str
    train_model_metric_artifact:ClassificationMetricArtifact
    best_model_metric_artifact:ClassificationMetricArtifact

@dataclass
class ModelPusherArtifact:
    saved_model_path:str
    model_path:str
