import sys
from typing import Optional

import numpy as np
import pandas as pd

from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException

class SensorData:
    '''
    This class will export whole mongodb data as pandas dataframe
    '''
    def __init__(self):
        '''
        Connect the Mongodb with code
        '''
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e, sys)
    
    def export_collection_as_dataframe(self, collection_name:str,
                                        database_name: Optional[str]=None) -> pd.DataFrame:
        try:
            '''
            Return entire collection as dataframe
            '''
            if database_name is None:
                self.collection = self.mongo_client.database[collection_name]
            else:
                self.collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(self.collection.find()))

            if '_id' in df.columns.to_list():
                df.drop(columns=['_id'], axis=1)
            df.replace({'na': np.nan}, inplace=True)
            return df
        except Exception as e:
            raise SensorException(e, sys)