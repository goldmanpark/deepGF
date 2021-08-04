# ref
# https://076923.github.io/posts/Python-opencv-8/
# https://keras.io/examples/vision/image_classification_from_scratch/
# https://sayak.dev/tf.keras/data_augmentation/image/2020/05/10/augmemtation-recipes.html

import os
import cv2
import random
import datetime
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# global
gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']
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
    return (dataHeight, dataWidth)
    # for img in images:
    #     if img.shape[0] < dataHeight and img.shape[1] < dataWidth:
    #         adjustedImgList.append(cv2.resize(img, dsize=(dataWidth, dataHeight), interpolation=cv2.INTER_CUBIC))
    #     else:
    #         adjustedImgList.append(cv2.resize(img, dsize=(dataWidth, dataHeight), interpolation=cv2.INTER_AREA))

# Main
dataSize = get_dsize()

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

# plt.figure(figsize=(10, 10))
# for images, labels in train_ds.take(1):
#     for i in range(9):
#         ax = plt.subplot(3, 3, i + 1)
#         plt.imshow(images[i].numpy().astype("uint8"))
#         plt.axis("off")
# plt.show()


model = keras.Sequential()
model.add(layers.experimental.preprocessing.RandomFlip('horizontal', input_shape=(dataSize[0], dataSize[1], 1)))
model.add(layers.experimental.preprocessing.RandomRotation(0.1))
model.add(layers.experimental.preprocessing.RandomZoom(0.1))
model.add(layers.Flatten(input_shape=dataSize))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(6, activation='softmax'))
model.summary()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)
history = model.fit(train_ds, epochs=15, validation_data=val_ds)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()