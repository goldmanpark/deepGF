import os
import datetime
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import util

DATA_PATH = os.getcwd() + '/DATA/'
BATCH_SIZE = 16
IMG_SIZE_RATIO = 0.75
EPOCH = 50
(DATA_HEIGHT, DATA_WIDTH) = util.get_ModifiedAverageSize(DATA_PATH, IMG_SIZE_RATIO)

image_generator = ImageDataGenerator( 
    horizontal_flip=True, 
    rotation_range=10,
    validation_split=0.2
)
seed = random.randint(1, 1000)
train_ds = image_generator.flow_from_directory(
    directory=DATA_PATH,
    subset='training',
    target_size=(DATA_HEIGHT, DATA_WIDTH),
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    shuffle=True,
    seed=seed
)
val_ds = image_generator.flow_from_directory(
    directory=DATA_PATH,
    subset='validation',
    target_size=(DATA_HEIGHT, DATA_WIDTH),
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    shuffle=True,
    seed=seed
)
util.show_Sample_from_DirectoryIterator(train_ds, 4, 4)

model = keras.Sequential()
model.add(layers.Conv2D(16, (10, 10), activation='relu', padding='same', input_shape=(DATA_HEIGHT, DATA_WIDTH, 1)))
model.add(layers.MaxPool2D())
model.add(layers.Conv2D(32, (8, 8), activation='relu', padding='same'))
model.add(layers.MaxPool2D())
model.add(layers.Conv2D(64, (5, 5), activation='relu', padding='same'))
model.add(layers.MaxPool2D())
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPool2D())
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(6, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

startTime = datetime.datetime.now()
history = model.fit(train_ds, epochs=EPOCH, validation_data=val_ds)
util.save_HistoryResult('CNN', startTime, model, history)