from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from os import environ
from dotenv import load_dotenv; load_dotenv()
from typing import Optional
from icecream import ic
from bson import ObjectId

class MongoDB:
    def __init__(self):
        try:
            password = environ.get("MONGODB_PASSWORD")
            user = environ.get("MONGODB_USER")
            cluster = environ.get("MONGODB_CLUSTER")

            if not all([password, user, cluster]):
                raise ValueError("Missing environment variables")
            self.uri = f"mongodb+srv://{user}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority"

        except ValueError as e:
            self.client = None
            print(e)

    def connect(self, database_name:str = "saathi") -> bool:
        try:
            if not self.uri:
                raise Exception("MongoDB connection failed")

            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.database = self.client[database_name]

            # Test connection
            self.client.admin.command('ping')
            print("Connected to MongoDB successfully!")
            return True

        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            return False

        except Exception as e:
            print(e)
            return False

    def create_index(self, collection_name: str, field_name: str, index_type: int = 1):
        try:
            self.database[collection_name].create_index([(field_name, index_type)])
            print(f"Index created on {collection_name}.{field_name}")
        except Exception as e:
            print(f"Error creating index: {e}")

    def aggregate(self, collection_name: str, pipeline: list) -> Optional[list]|None:
        # to execute an agregation on a collection
        try:
            return list(self.database[collection_name].aggregate(pipeline))
        except Exception as e:
            print(f"Error in aggregation: {e}")
            return None

    def insert(self, collection_name, doc) -> Optional[ObjectId]|None:
        try:
            doc_dict = doc.model_dump()
            result = self.database[collection_name].insert_one(doc_dict)
            if result.acknowledged:
                ic(result.inserted_id)
                return result.inserted_id  # Returns the ObjectId
            return None
        except Exception as e:
            print("Exception while inserting data in mongo db\nException in utils/dbHandler.py insert function")
            print(e)
            return None
    
    def find(self, collection_name, query):
        cursor = self.database[collection_name].find(query)
        return list(cursor)
    
    def find_one(self, collection_name, query):
        return self.database[collection_name].find_one(query)
    
    def find_with_sort(self, collection_name: str, query: dict = {}, sort_field: str = None, skip: int = None, limit: int = None):
        try:
            cursor = self.database[collection_name].find(query)
            if sort_field:
                # Sort in descending order
                cursor = cursor.sort(sort_field, -1)
            
            if skip:
                # for pagination
                cursor = cursor.skip(skip)

            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"Error fetching sorted documents: {e}")
            return None

    def update(self, collection_name, query, data):
        try:
            # Update the document with the new data
            self.database[collection_name].update_one(query, {"$set": data})
            ic("Document updated successfully!")
            return True
        except Exception as e:
            print("Exception while updating data in MongoDB\nException in utils/dbHandler.py update function")
            print(e)
            return False
    
    def delete_many(self, collection_name: str, query: dict) -> bool:
        try:
            result = self.database[collection_name].delete_many(query)
            return result.acknowledged
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False
    
    def close(self):
        self.client.close()



if __name__ == "__main__":
    db = MongoDB()
    db.connect()