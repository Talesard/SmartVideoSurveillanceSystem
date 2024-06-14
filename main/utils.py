import datetime
import requests
from config import Config

def turn_on_alarm_notification(event_name):
    url = f'{Config.NOTIFICATIONS_URL}/start_alarm'
    data = {
        "event_name": event_name,
        "secret_token": Config.NOTIFICATIONS_SECRET_KEY
    }
    response = requests.post(url, json=data)
    return response.status_code

def turn_on_alarm_notification_conditional(event_name):
    if event_name in Config.NOTIFICATIONS_EVENTS:
        turn_on_alarm_notification(event_name)

def turn_off_alarm_notification():
    url = f'{Config.NOTIFICATIONS_URL}/start_alarm'
    data = {
        "secret_token": Config.NOTIFICATIONS_SECRET_KEY
    }
    response = requests.post(url, json=data)
    return response.status_code

def get_all_logs():
    url = f'{Config.STORAGE_URL}/get_all_logs'
    data = {
        "token": Config.STORAGE_SECRET_KEY
    }
    response = requests.post(url, json=data)
    return response.json()["data"]

def save_log(type, video_id):
    url = f'{Config.STORAGE_URL}/save_log'
    data = {
        "token": Config.STORAGE_SECRET_KEY,
        "type": type,
        "video_id": video_id
    }
    response = requests.post(url, json=data)
    return response.status_code

def get_all_fragments():
    url = f'{Config.STORAGE_URL}/get_all_fragments'
    data = {
        "token": Config.STORAGE_SECRET_KEY
    }
    response = requests.post(url, json=data)
    return response.json()["data"]

def save_fragment(file_base64):
    url = f'{Config.STORAGE_URL}/save_fragment'
    data = {
        "token": Config.STORAGE_SECRET_KEY,
        "file_base64": file_base64
    }
    response = requests.post(url, json=data)
    return response.json()["id"]

def get_fragment(id):
    url = f'{Config.STORAGE_URL}/get_fragment_by_id'
    data = {
        "token": Config.STORAGE_SECRET_KEY,
        "id": id
    }
    response = requests.post(url, json=data)
    return response.json()["data"]["file_base64"]

def save_user(username, password, password2, email, invitation_token):
    url = f'{Config.AUTH_URL}/save_user'
    data = {
        "token": Config.AUTH_SECRET_KEY,
        "username": username,
        "password": password,
        "password2": password2,
        "email": email,
        "invitation_token": invitation_token
    }
    response = requests.post(url, json=data)
    error_message = response.json()["error_message"]
    if error_message != " ":
        return error_message

def login(username, password):
    url = f'{Config.AUTH_URL}/login'
    data = {
        "token": Config.AUTH_SECRET_KEY,
        "username": username,
        "password": password,
    }
    response = requests.post(url, json=data)
    error_message = response.json()["error_message"]
    if error_message != " ":
        return error_message