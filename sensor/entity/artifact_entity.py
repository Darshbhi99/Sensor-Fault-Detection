from dataclasses import dataclass

'''
This class gives you input  output of all stages of training pipeline
'''
@dataclass
class DataIngestionArtifact:
    trained_file_path:str 
    test_file_path:str 