from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact
from sensor.entity.config_entity import ModelPusherConfig
import shutil
import os,sys
import warnings
warnings.filterwarnings('ignore')


class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                    model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_evalaution_artifact = model_evaluation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_pusher(self) ->ModelPusherArtifact:
        try:
            trained_model_file_path:str = self.model_evalaution_artifact.best_model_file_path
            logging.info("Creating the Model Pusher Directory")
            # This is the model pusher directory in artifact folder
            os.makedirs(self.model_pusher_config.model_pusher_dir, exist_ok=True)
            # Copying the model from the evaluation to model pusher folder
            shutil.copy(trained_model_file_path, self.model_pusher_config.model_pusher_dir)
            
            # Directory for all the final models
            logging.info('Creating the Saved Model Directory')
            # Saving the Model in Save Model Directory
            if self.model_evalaution_artifact.is_model_accepted == True:
                os.makedirs(self.model_pusher_config.saved_model_dir, exist_ok=True)
                shutil.copy(trained_model_file_path, self.model_pusher_config.saved_model_dir)
                logging.info("Saving the Model")
            model_pusher_artifact = ModelPusherArtifact(
                                        saved_model_path=self.model_pusher_config.saved_model_file_path,
                                        model_path=self.model_pusher_config.pushed_model_file_path)
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)