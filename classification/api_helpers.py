from config import config
import requests
from datetime import datetime
from PIL import Image
import imageio
import io
import base64

class API:
    def __init__(self):
        self.config = config
        self.jwt_token = ""
    
    def login(self):
        headers = {
            'Content-Type': 'application/json'
        }
        json = {
            'username': self.config["api_username"],
            'password': self.config["api_password"],
        }
        response = requests.post(self.config["api_login"], json=json, headers=headers)
        if response.status_code in [200, 201]:
            self.jwt_token = response.json().get('access_token')
            print("Successful login")
            print(self.jwt_token)
        else:
            print("Failed to login!")

    def save_log (self, base_json, video_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jwt_token}'
        }
        base_json["video_id"] = video_id
        response = requests.post(self.config["api_logs"], json=base_json, headers=headers)
        if response.status_code not in [200, 201]:
            print('Failed to post log!')

    def make_gif(self, frames):
        frames = frames[0]
        # frames = frames * 255
        gif_buffer = io.BytesIO()
        imageio.mimsave(gif_buffer, frames, format='GIF', fps=6)
        gif_buffer.seek(0)
        return base64.b64encode(gif_buffer.read()).decode('utf-8')

    def save_fragment(self, frames):
        base64_gif = self.make_gif(frames)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jwt_token}'
        }
        json = {
            'file_base64': base64_gif
        }
        response = requests.post(self.config["api_fragments"], json=json, headers=headers)
        if response.status_code == 200:
            data = response.json()
            fragment_id = data["video_id"]
            return fragment_id

