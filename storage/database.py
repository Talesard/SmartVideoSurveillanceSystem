import datetime
from pymongo import MongoClient
from flask import current_app
from bson import ObjectId

def json_serializable(data):
    if isinstance(data, list):
        return [json_serializable(item) for item in data]
    if isinstance(data, dict):
        return {key: json_serializable(value) for key, value in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data

def get_db():
    client = MongoClient(current_app.config['MONGO_URI'])
    db = client.get_default_database()
    return db

def is_user_exist(username):
    db = get_db()
    users_collection = db.users
    return users_collection.find_one({'username': username}) != None

def save_user(username, password, email):
    new_user = {
        'username': username,
        'password': password,
        'email': email
    }
    db = get_db()
    users_collection = db.users
    users_collection.insert_one(new_user)

def get_user(username):
    db = get_db()
    users_collection = db.users
    return json_serializable (users_collection.find_one({'username': username}))

def save_log(type, video_id):
    db = get_db()
    logs_collection = db.logs
    new_log = {
        'type': type,
        'date': datetime.datetime.now(),
        'video_id': video_id
    }
    logs_collection.insert_one(new_log)

def get_all_logs():
    db = get_db()
    logs_collection = db.logs
    return json_serializable(list(logs_collection.find()))

def get_log_by_id(id):
    db = get_db()
    logs_collection = db.logs
    return json_serializable(logs_collection.find_one({'_id': ObjectId(id)}))

def get_logs_by_dates(start_date, end_date):
    db = get_db()
    logs_collection = db.logs
    return json_serializable(list(logs_collection.find({'date': {'$gte': start_date, '$lte': end_date}})))

def save_fragment(base64):
    db = get_db()
    fragments_collection = db.fragments
    new_fragment = {
        'file_base64': base64
    }
    result = fragments_collection.insert_one(new_fragment)
    return str(result.inserted_id)

def get_all_fragments():
    db = get_db()
    fragments_collection = db.fragments
    return json_serializable(list(fragments_collection.find()))

def get_fragment_by_id(id):
    db = get_db()
    fragments_collection = db.fragments
    return json_serializable(fragments_collection.find_one({'_id': ObjectId(id)}))