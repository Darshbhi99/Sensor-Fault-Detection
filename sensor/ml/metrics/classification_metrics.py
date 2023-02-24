'''
In this file there are function which will be used for model evaluation 
'''
from sensor.entity.artifact_entity import ClassificationMetricArtifact
from sensor.exception import SensorException
from sklearn.metrics import f1_score, precision_score, recall_score
import sys, os
import warnings 
warnings.filterwarnings('ignore')

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        f1_scr = f1_score(y_true, y_pred)
        precs = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        metrics = ClassificationMetricArtifact(f1_score = float(f1_scr), 
                                                precision_score=float(precs), 
                                                recall_score=float(recall))
        return metrics
    except Exception as e:
        raise SensorException(e, sys)