# ref
# https://076923.github.io/posts/Python-opencv-8/
# https://keras.io/examples/vision/image_classification_from_scratch/

import os
import cv2
import random
import datetime
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# global
gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']
dataHeight = 0
dataWidth = 0
train_ds = {}
val_ds = {}

# directory
DATA_PATH = os.getcwd() + '/DATA/'

def get_dsize():
    # get images and label
    totalHeight = 0
    totalWidth = 0
    images = []
    start = datetime.datetime.now()
    for member in gfMembers_ENG:
        dirPath = DATA_PATH + member +'/'
        imgPaths = os.listdir(dirPath)        
        for path in imgPaths:
            img = cv2.imread(dirPath + path, cv2.IMREAD_GRAYSCALE)
            images.append(img)
            totalHeight += img.shape[0]
            totalWidth += img.shape[1]
    
    # uniform image size
    dataHeight = totalHeight // len(images)
    dataWidth = totalWidth // len(images)
    end = datetime.datetime.now()

    print('data count : ' + str(len(images)))
    print('avg height : ' + str(dataHeight))
    print('avg width : ' + str(dataWidth))
    print('time consumption : ' + str(end - start))

    # for img in images:
    #     if img.shape[0] < dataHeight and img.shape[1] < dataWidth:
    #         adjustedImgList.append(cv2.resize(img, dsize=(dataWidth, dataHeight), interpolation=cv2.INTER_CUBIC))
    #     else:
    #         adjustedImgList.append(cv2.resize(img, dsize=(dataWidth, dataHeight), interpolation=cv2.INTER_AREA))

# Main
get_dsize()

seed = random.randint(1, 1000)
train_ds = keras.preprocessing.image_dataset_from_directory(
    directory=DATA_PATH,
    image_size=(dataWidth, dataHeight),
    color_mode='grayscale',
    smart_resize=True,
    validation_split=0.2,
    subset='training',
    seed=seed
)
val_ds = keras.preprocessing.image_dataset_from_directory(
    directory=DATA_PATH,
    image_size=(dataWidth, dataHeight),
    color_mode='grayscale',
    smart_resize=True,
    validation_split=0.2,
    subset='validation',
    seed=seed
)
model = keras.Sequential()
model.add(layers.Flatten(input_shape=[dataWidth, dataHeight]))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(6, activation='softmax'))
model.summary()
model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

history = model.fit(train_ds, epochs=10, validation_data=val_ds)