# CNN2 : using flow_from_directory, 
# class 'tensorflow.python.keras.preprocessing.image.DirectoryIterator'

import os
import datetime
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import util, CNN_MODEL

DATA_PATH = os.getcwd() + '/DATA/'
BATCH_SIZE = 16
IMG_SIZE_RATIO = 0.9
EPOCH = 100
#(DATA_HEIGHT, DATA_WIDTH) = util.get_ModifiedAverageSize(DATA_PATH, IMG_SIZE_RATIO)
(DATA_HEIGHT, DATA_WIDTH) = util.get_MinimalSize(DATA_PATH)

image_generator = ImageDataGenerator( 
    horizontal_flip=True, 
    rotation_range=5,
    brightness_range=(0.2, 0.8),
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

model = CNN_MODEL.get_CNN_model1((DATA_HEIGHT, DATA_WIDTH, 1))

startTime = datetime.datetime.now()
history = model.fit(train_ds, epochs=EPOCH, validation_data=val_ds)
util.save_HistoryResult('CNN', startTime, model, history)