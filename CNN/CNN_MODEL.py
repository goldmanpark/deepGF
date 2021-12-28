import os
import datetime
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import util

def get_CNN_model1(inputShape):
    model = keras.Sequential()
    model.add(layers.InputLayer(inputShape))
    model.add(layers.Conv2D(16, (10, 10), activation='relu', padding='same'))
    model.add(layers.MaxPool2D())
    model.add(layers.Conv2D(32, (8, 8), activation='relu', padding='same'))
    model.add(layers.MaxPool2D())
    model.add(layers.Conv2D(64, (5, 5), activation='relu', padding='same'))
    model.add(layers.MaxPool2D())
    model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPool2D())
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(6, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# VGG
def get_CNN_model2(inputShape):
    model = keras.Sequential()
    model.add(layers.InputLayer(inputShape))
    model.add(layers.Conv2D(64, 3, activation='relu', padding='same'))
    model.add(layers.Conv2D(64, 3, activation='relu', padding='same'))
    model.add(layers.MaxPooling2D())
    model.add(layers.Conv2D(128, 3, activation='relu', padding='same'))
    model.add(layers.Conv2D(128, 3, activation='relu', padding='same'))
    model.add(layers.MaxPooling2D())
    model.add(layers.Conv2D(256, 3, activation='relu', padding='same'))
    model.add(layers.Conv2D(256, 3, activation='relu', padding='same'))
    model.add(layers.Conv2D(256, 3, activation='relu', padding='same'))
    model.add(layers.MaxPooling2D())
    model.add(layers.Flatten())
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(6, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model