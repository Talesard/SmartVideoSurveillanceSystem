import os
from pymongo import MongoClient

URL = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/SurvDB'
client = MongoClient(URL)
db = client.get_default_database()
logs_collection = db.logs
logs_collection.delete_many({})
fragments_collection = db.fragments
fragments_collection.delete_many({})
