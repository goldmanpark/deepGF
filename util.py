import os
import cv2
import matplotlib.pyplot as plt

gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']

def get_ModifiedAverageSize(dataPath, modifier):
    # get images and label
    totalHeight = 0
    totalWidth = 0
    images = []
    for member in gfMembers_ENG:
        dirPath = dataPath + member +'/'
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
    return (int(dataHeight * modifier), int(dataWidth * modifier))

def getLabelClassIndex(classNames, numpyArr):
    i = 0
    for n in numpyArr:
        if n == 1.:
            return classNames[i]
        i += 1
    return 'ERROR'

def draw_Sample(dataset, width, height):
    for images, labels in dataset.take(1):
        for i in range(width * height):
            ax = plt.subplot(height, width, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"), cmap='gray', vmin = 0, vmax = 255)
            plt.title(getLabelClassIndex(dataset.class_names, labels[i].numpy()))
            plt.axis("off")
    plt.show()

def draw_HistoryResult(hist):
    plt.subplot(1, 2, 1)
    plt.plot(hist.history['accuracy'])
    plt.plot(hist.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(['Train', 'Val'], loc='upper left')

    plt.subplot(1, 2, 2)
    plt.plot(hist.history['loss'])
    plt.plot(hist.history['val_loss'])
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train', 'Val'], loc='upper left')
    plt.show()