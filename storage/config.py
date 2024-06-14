import os

class Config:
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/SurvDB'
    STORAGE_SECRET_TOKEN = os.environ.get('STORAGE_SECRET_TOKEN') or 'my_super_secret_storage_token'
    STORAGE_PORT = os.environ.get('STORAGE_PORT') or 5566
