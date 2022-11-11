import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()

# This is the class which will connect the mongodb with the code
class MongoDBClient:
    client = None
    def __init__(self, database_name = DATABASE_NAME) ->None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = "mongodb+srv://darsh:darsh1995@cluster0.3qobtiv.mongodb.net/test"
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database_name = database_name
            self.database = self.client[database_name]
        except Exception as e:
            raise e
