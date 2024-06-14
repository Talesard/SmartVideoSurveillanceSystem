import os

class Config:
    AUTH_PORT = os.environ.get('AUTH_PORT') or 5577
    AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY') or "my_super_secret_auth_token"
    STORAGE_URL = os.environ.get('STORAGE_URL') or 'http://localhost:5566'
    STORAGE_SECRET_KEY = os.environ.get('STORAGE_SECRET_KEY') or 'my_super_secret_storage_token'
    INVITATION_TOKENS = ["inv-token-1", "inv-token2", "Invitation token from Admin"]
