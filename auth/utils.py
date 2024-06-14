import requests
from werkzeug.security import generate_password_hash, check_password_hash
import re
from config import Config

def check_token(token):
    return token == Config.AUTH_SECRET_KEY

def validate_password(password):
    is_valid = True
    is_valid = is_valid and (len(password) > 5)
    is_valid = is_valid and password.lower() != password and password.upper() != password
    return is_valid

def validate_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return re.match(regex, email) != None

def check_invitation_token(invitation_token):
    return invitation_token in Config.INVITATION_TOKENS

def check_password(password, hash):
    return check_password_hash(hash, password)

def has_password(password):
    return generate_password_hash(password)

def get_user(username):
    url = f'{Config.STORAGE_URL}/get_user'
    data = {
        "token": Config.STORAGE_SECRET_KEY,
        "username": username
    }
    response = requests.post(url, json=data)
    return response.json()["data"]

def save_user(username, password, password2, email, invitation_token):
    if not validate_password(password): return "Invalid password"
    if not validate_email(email): return "Invalid email"
    if not password == password2: return "Pass1 != Pass2"
    if not check_invitation_token(invitation_token): return "Invalid invitation token"
    url = f'{Config.STORAGE_URL}/save_user'
    data = {
        "token": Config.STORAGE_SECRET_KEY,
        "username": username,
        "password_hash": generate_password_hash(password),
        "email": email
    }
    response = requests.post(url, json=data)
    print(response)
    error_message = response.json()["error_message"]
    if (error_message != ""):
        return error_message

def login(username, password):
    user = get_user(username)
    if (user):
        if check_password(password, user["password"]):
            pass
        else:
            return "Wrong password"
    else:
        return "User not found"