import os
import datetime
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import util

DATA_PATH = os.getcwd() + '/DATA/'
BATCH_SIZE = 16
IMG_SIZE_RATIO = 0.75
EPOCH = 50

dataSize = util.get_ModifiedAverageSize(DATA_PATH, IMG_SIZE_RATIO)
seed = random.randint(1, 1000)

train_ds = keras.preprocessing.image_dataset_from_directory(
    directory=DATA_PATH,
    subset='training',
    label_mode='categorical',
    validation_split=0.2,
    batch_size=BATCH_SIZE,
    image_size=dataSize,
    color_mode='grayscale',
    smart_resize=True,
    seed=seed
)
val_ds = keras.preprocessing.image_dataset_from_directory(
    directory=DATA_PATH,
    subset='validation',
    label_mode='categorical',
    validation_split=0.2,
    batch_size=BATCH_SIZE,
    image_size=dataSize,
    color_mode='grayscale',
    smart_resize=True,
    seed=seed
)
#util.draw_Sample(train_ds, width=4, height=4)

model = keras.Sequential()
# model.add(layers.experimental.preprocessing.RandomFlip('horizontal', input_shape=(dataSize[0], dataSize[1], 1)))
# model.add(layers.experimental.preprocessing.RandomRotation(0.2))
model.add(layers.Conv2D(16, (10, 10), activation='relu', padding='same', input_shape=(dataSize[0], dataSize[1], 1)))
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
train_ds = train_ds.prefetch(buffer_size=BATCH_SIZE)
val_ds = val_ds.prefetch(buffer_size=BATCH_SIZE)

startTime = datetime.datetime.now()
history = model.fit(train_ds, epochs=EPOCH, validation_data=val_ds)
util.save_HistoryResult('CNN', startTime, model, history)