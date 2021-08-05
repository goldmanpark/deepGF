# ref
# https://076923.github.io/posts/Python-opencv-8/
# https://keras.io/examples/vision/image_classification_from_scratch/
# https://sayak.dev/tf.keras/data_augmentation/image/2020/05/10/augmemtation-recipes.html

import os
import cv2
import random
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

    print('data count : ' + str(len(images)))
    print('avg height : ' + str(dataHeight))
    print('avg width : ' + str(dataWidth))
    return (int(dataHeight * 0.5), int(dataWidth * 0.5))

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

def getLabelClassIndex(classNames, numpyArr):
    i = 0
    for n in numpyArr:
        if n == 1.:
            return classNames[i]
        i += 1
    return 'ERROR'

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"), cmap='gray', vmin = 0, vmax = 255)
        plt.title(getLabelClassIndex(train_ds.class_names, labels[i].numpy()))
        plt.axis("off")
plt.show()

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

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Val'], loc='upper left')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Val'], loc='upper left')
plt.show()