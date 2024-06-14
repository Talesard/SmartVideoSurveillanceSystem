from utils import read_and_preprocess_data
from utils import read_label_encoder
import pickle
import cv2
import time
import numpy as np

def save_camera_data_dump(class_count, frame_count, frame_size, data, labels):
     data = {
         'class_count': class_count,
         'frame_count': frame_count,
         'frame_size': frame_size,
         'data': data,
         'labels': labels
     }
     with open("../shared/camera_data_dump.pickle", "wb") as file:
         pickle.dump(data, file)

def read_camera_data_dump():
    with open("../shared/camera_data_dump.pickle", "rb") as file:
        loaded_data = pickle.load(file)
    return loaded_data

def load_camera_data():
    data = read_camera_data_dump()
    return data['class_count'], data['frame_count'], data['frame_size'], data['data'], data['labels']

class Camera:
    def __init__(self, data_path, frame_size, load_dump):
        self.frame_size = frame_size
        self.data_path = data_path
        print('init camera simulator...')
        if load_dump:
            print('loading camera dump')
            self.class_count, self.frame_count, self.frame_size, self.data, self.labels = load_camera_data()
        else:
            self.class_count, self.frame_count, self.frame_size, _, _, self.data, _, _, self.labels = read_and_preprocess_data(data_path, frame_size)
            # save_camera_data_dump(self.class_count, self.frame_count, self.frame_size, self.data, self.labels)
        self.last_clip_id = 0
        self.clip_count = self.data.shape[0]
        self.label_encoder = read_label_encoder()


    def get_clip(self):
        self.last_clip_id += 1
        if self.last_clip_id >= self.clip_count:
            self.last_clip_id = 0
        print('camera simulator gets clip:', self.label_encoder.inverse_transform([self.labels[self.last_clip_id]]))
        return self.data[self.last_clip_id]
    
    def get_clip_real_cam(self, duration=2, fps=6, frame_size=(128, 128)):
        print("Camera: New fragment")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video device.")
            return None
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
        num_frames = int(duration * fps)
        frames = []
        for _ in range(num_frames):
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                return None
            resized_frame = cv2.resize(frame, frame_size)
            frames.append(resized_frame)
            time.sleep(1 / fps)
        cap.release()
        cv2.destroyAllWindows()
        if len(frames) == num_frames:
            video_array = np.array(frames, dtype=np.float32)
            video_array /= 255.0
            return video_array
        else:
            print("Captured frames less than expected.")
            return None