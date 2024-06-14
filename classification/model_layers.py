import tensorflow as tf
from tensorflow.keras import layers, models, utils
from keras.layers import Layer
import keras.backend as K

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5, # 5
    mode='min', 
    restore_best_weights=True
)

def add_2d_cnn_part(model, FRAME_COUNT, FRAME_SIZE):
    
    model.add(tf.keras.Input(shape=(FRAME_COUNT, FRAME_SIZE, FRAME_SIZE, 3)))
    model.add(layers.TimeDistributed(layers.Conv2D(filters=64, kernel_size=(5,5), strides=(2,2))))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    
    model.add(layers.TimeDistributed(layers.Conv2D(filters=32, kernel_size=(4,4), strides=(2,2))))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    
    model.add(layers.TimeDistributed(layers.Conv2D(filters=32, kernel_size=(3,3), strides=(2,2))))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    
    model.add(layers.TimeDistributed(layers.Conv2D(filters=16, kernel_size=(3,3))))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))
    
    return model

def add_3d_cnn_part(model, FRAME_COUNT, FRAME_SIZE):
    model.add(tf.keras.Input(shape=(FRAME_COUNT, FRAME_SIZE, FRAME_SIZE, 3)))
    model.add(layers.Conv3D(filters=32, kernel_size=(5, 5, 5), strides=(2,2,2)))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    # model.add(layers.MaxPooling3D((2,2,2)))
    # model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))

    model.add(layers.Conv3D(filters=16, kernel_size=(4, 4, 4), strides=(2,2,2)))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    # model.add(layers.MaxPooling3D((2,2,2)))
    # model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))

    model.add(layers.Conv3D(filters=16, kernel_size=(3, 3, 3)))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    # model.add(layers.MaxPooling3D((1,2,2)))
    # model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))

    model.add(layers.Conv3D(filters=8, kernel_size=(3, 3, 3)))
    model.add(layers.BatchNormalization(axis=2))
    model.add(layers.Activation('relu'))
    # model.add(layers.MaxPooling3D((2,2,2)))
    # model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))

    return model

def add_rnn_part(model, return_sequences=False):
    model.add(layers.SimpleRNN(16, return_sequences=return_sequences))
    return model

def add_lstm_part(model, return_sequences=False):
    model.add(layers.LSTM(16, return_sequences=return_sequences))
    return model

def add_dense_part(model, CLASS_COUNT):
    model.add(layers.Dense(CLASS_COUNT*2, activation='relu'))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(CLASS_COUNT, activation='softmax'))
    return model

class attention(Layer):
    def init(self,kwargs):
        super(attention,self).init(kwargs)

    def build(self,input_shape):
        self.W=self.add_weight(name='attention_weight', shape=(input_shape[-1],1), 
                               initializer='random_normal', trainable=True)
        self.b=self.add_weight(name='attention_bias', shape=(input_shape[1],1), 
                               initializer='zeros', trainable=True)
        super(attention, self).build(input_shape)

    def call(self,x):
        # Alignment scores. Pass them through tanh function
        e = K.tanh(K.dot(x,self.W)+self.b)
        # Remove dimension of size 1
        e = K.squeeze(e, axis=-1)
        # Compute the weights
        alpha = K.softmax(e)
        # Reshape to tensorFlow format
        alpha = K.expand_dims(alpha, axis=-1)
        # Compute the context vector
        context = x * alpha
        context = K.sum(context, axis=1)
        return context