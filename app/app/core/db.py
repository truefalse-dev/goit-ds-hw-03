import os
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

class DbConnection:

    __instance = None
    
    class Singleton:

        client = None

        def __init__(self):
            # Initialise mongo client
           try:
                self.client = MongoClient(
                    os.getenv('MONGODB'),
                    server_api=ServerApi('1')
                )
           except errors.ConfigurationError as e:
               print(e)
               exit()

    def __init__(self):
        if not DbConnection.__instance:
            DbConnection.__instance = DbConnection.Singleton()

    def __getattr__(self, item):
        return getattr(self.__instance, item)
    
    def __setattr__(self, item, value):
        return setattr(self._iInstance, item, value)