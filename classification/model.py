import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models, utils
from sklearn.metrics import classification_report, confusion_matrix
from model_layers import *


FRAME_COUNT = 6
FRAME_SIZE = 128
CLASS_COUNT = 2

def create_model():
    model = models.Sequential()
    model = add_2d_cnn_part(model, FRAME_COUNT, FRAME_SIZE)
    model.add(layers.TimeDistributed(layers.Flatten()))
    model = add_lstm_part(model, return_sequences=True)
    model.add(attention())
    model = add_dense_part(model, CLASS_COUNT)

    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                metrics=['accuracy'],
                )
    
    return model

def load_model(path):
    model = tf.keras.models.load_model(path)
    return model

