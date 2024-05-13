import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

class DbConnection:

    __instance = None
    
    class Singleton:
        def __init__(self):
            # Initialise mongo client
            self.client = MongoClient(
                os.getenv('MONGODB'),
                server_api=ServerApi('1')
            )

    def __init__(self):
        if not DbConnection.__instance:
            DbConnection.__instance = DbConnection.Singleton()

    def __getattr__(self, item):
        return getattr(self.__instance, item)
    
    def __setattr__(self, item, value):
        return setattr(self._iInstance, item, value)