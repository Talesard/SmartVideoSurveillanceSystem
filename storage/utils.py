from config import Config

def check_token(token):
    return token == Config.STORAGE_SECRET_TOKEN