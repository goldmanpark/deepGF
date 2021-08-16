# ref
# https://076923.github.io/posts/Python-opencv-8/
# https://keras.io/examples/vision/image_classification_from_scratch/
# https://sayak.dev/tf.keras/data_augmentation/image/2020/05/10/augmemtation-recipes.html

import os
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import util

DATA_PATH = os.getcwd() + '/DATA/'
dataSize = util.get_ModifiedAverageSize(DATA_PATH, 0.8)
seed = random.randint(1, 1000)

train_ds = keras.preprocessing.image_dataset_from_directory(
    directory=DATA_PATH,
    subset='training',
    label_mode='categorical',
    validation_split=0.2,
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
    image_size=dataSize,
    color_mode='grayscale',
    smart_resize=True,
    seed=seed
)
util.show_Sample_from_Dataset(train_ds, width=4, height=3)
model = keras.Sequential()
model.add(layers.experimental.preprocessing.RandomFlip('horizontal', input_shape=(dataSize[0], dataSize[1], 1)))
model.add(layers.experimental.preprocessing.RandomRotation(0.25))
model.add(layers.Flatten(input_shape=dataSize))
model.add(layers.Dense(6 * 128, activation='relu'))
model.add(layers.Dense(6 * 64, activation='relu'))
model.add(layers.Dense(6 * 32, activation='relu'))
model.add(layers.Dense(6 * 16, activation='relu'))
model.add(layers.Dense(6 * 8, activation='relu'))
model.add(layers.Dense(6 * 4, activation='relu'))
model.add(layers.Dense(6 * 2, activation='relu'))
model.add(layers.Dense(6, activation='softmax'))
model.summary()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)
history = model.fit(train_ds, epochs=50, validation_data=val_ds)
util.draw_HistoryResult(history)