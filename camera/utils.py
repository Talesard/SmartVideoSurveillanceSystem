import os
import cv2
import numpy as np
import tensorflow as tf
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pickle

def save_label_encoder(label_encoder):
    with open("../shared/label_encoder.picle", "wb") as file:
        pickle.dump(label_encoder, file)

def read_label_encoder():
    with open("../shared/label_encoder.picle", "rb") as file:
        loaded_data = pickle.load(file)
    return loaded_data

def format_frame(frame, output_size):
  frame = tf.image.convert_image_dtype(frame, tf.float32)
  frame = tf.image.resize_with_pad(frame, *output_size)
  return frame

def read(path, FRAME_SIZE):
    videos = []
    labels = []
    for _, dirs, _ in os.walk(path):
        for dir in dirs:
            print(dir)
            for _, _, files in os.walk(os.path.join(path, dir)):
                for file in files:
                    frames = []
                    video_path = os.path.join(path, dir, file)
                    cap = cv2.VideoCapture(video_path)
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if ret == False:
                            break
                        frames.append(format_frame(frame, (FRAME_SIZE, FRAME_SIZE)))
                    videos.append(np.array(frames, dtype=np.float32))
                    labels.append(dir)
    return {'videos': videos, 'labels': labels}

def get_med_frame_count(videos):
    return np.median(np.array([v.shape[0] for v in videos]))

def padding(data, size):
    size = int(size)
    for i in range(len(data['videos'])):
        if data['videos'][i].shape[0] >= size:
            data['videos'][i] = data['videos'][i][:size]
        else:
            sh = list(data['videos'][i].shape)
            sh[0] = size - data['videos'][i].shape[0]
            data['videos'][i] = np.concatenate((data['videos'][i], np.zeros(tuple(sh), dtype=np.float32)), axis=0)
    return data

def read_and_preprocess_data(DATA_PATH, FRAME_SIZE, pad32=False):
    print('reading...')
    data = read(DATA_PATH, FRAME_SIZE)
    CLASS_COUNT = len(set(data['labels']))
    print('class count =', CLASS_COUNT)
    med_frame_count = get_med_frame_count(data['videos'])
    print('med frame count =', med_frame_count)
    print('padding...')
    if (not pad32):
        data = padding(data, med_frame_count)
    else:
        data = padding(data, 32)
    print('Labels encoding...')
    data['videos'] = np.array(data['videos'])
    data['labels'] = np.array(data['labels'])
    le = preprocessing.LabelEncoder()
    le.fit(data['labels'])

    # save_label_encoder(le) # dangerous!

    print(le.get_params())
    data['labels'] = le.transform(data['labels'])
    print(data['labels'].shape, data['videos'].shape)
    print('norm...')
    data['videos'] = (data['videos']-data['videos'].min())/(data['videos'].max()-data['videos'].min())
    print('Train-val-test split...')
    X_train, X_test, y_train, y_test = train_test_split(data['videos'], data['labels'], test_size=0.3, random_state=42)
    X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.3, random_state=42)
    print('Train:', X_train.shape, y_train.shape)
    print('Val:', X_val.shape, y_val.shape)
    print('Test:', X_test.shape, y_test.shape)
    FRAME_COUNT = X_train.shape[1]
    return CLASS_COUNT, FRAME_COUNT, FRAME_SIZE, X_train, X_val, X_test, y_train, y_val, y_test
