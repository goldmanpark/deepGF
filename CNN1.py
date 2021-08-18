# CNN1 : using image_dataset_from_directory, 
# class 'tensorflow.python.data.ops.dataset_ops.BatchDataset'

import os
import datetime
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import util, CNN_MODEL

DATA_PATH = os.getcwd() + '/DATA/'
BATCH_SIZE = 16
IMG_SIZE_RATIO = 0.75
EPOCH = 50
(DATA_HEIGHT, DATA_WIDTH) = util.get_ModifiedAverageSize(DATA_PATH, IMG_SIZE_RATIO)

seed = random.randint(1, 1000)
train_ds = keras.preprocessing.image_dataset_from_directory(
    directory=DATA_PATH,
    subset='training',
    label_mode='categorical',
    validation_split=0.2,
    batch_size=BATCH_SIZE,
    image_size=(DATA_HEIGHT, DATA_WIDTH),
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
    image_size=(DATA_HEIGHT, DATA_WIDTH),
    color_mode='grayscale',
    smart_resize=True,
    seed=seed
)
train_ds = train_ds.prefetch(buffer_size=BATCH_SIZE)
val_ds = val_ds.prefetch(buffer_size=BATCH_SIZE)
#util.draw_Sample(train_ds, width=4, height=4)

model = CNN_MODEL.get_CNN_model1((DATA_HEIGHT, DATA_WIDTH, 1))

startTime = datetime.datetime.now()
history = model.fit(train_ds, epochs=EPOCH, validation_data=val_ds)
util.save_HistoryResult('CNN', startTime, model, history)