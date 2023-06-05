import pymongo

class DatabaseManager:
    def __init__(self, db_uri, db_name, collection_name):
        self.mongo_client = pymongo.MongoClient(db_uri)
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]

    def insert_command(self, command_object):
        self.collection.insert_one(command_object)
