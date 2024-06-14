import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/SurvDB'
    NOTIFICATIONS_SECRET_KEY = os.environ.get('NOTIFICATIONS_SECRET_KEY') or 'my_super_secret_notifications_token'
    NOTIFICATIONS_EVENTS = ["CricketShot"]
    NOTIFICATIONS_URL = os.environ.get('NOTIFICATIONS_URL') or 'http://localhost:5555'
    STORAGE_URL = os.environ.get('STORAGE_URL') or 'http://localhost:5566'
    STORAGE_SECRET_KEY = os.environ.get('STORAGE_SECRET_KEY') or 'my_super_secret_storage_token'
    AUTH_URL = os.environ.get('AUTH_URL') or 'http://localhost:5577'
    AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY') or 'my_super_secret_auth_token'