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