import os
import cv2
import threading
from pathlib import Path
from mtcnn import MTCNN
from PIL import Image

# Initialize global vaiables
gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']

# directory path
chromeDriverPath = os.getcwd() + '/chromedriver.exe'
#ORIGINAL_PATH = os.getcwd() + '/ORIGINAL/'
ORIGINAL_PATH = 'D:\ORIGINAL/'
UNFIXED_PATH =  os.getcwd() + '/UNFIXED/'
DATA_PATH = os.getcwd() + '/DATA/'

def findOrCreateDirectory(idx):
    try:
        Path(UNFIXED_PATH + gfMembers_ENG[idx]).mkdir(parents=True, exist_ok=True)
        Path(DATA_PATH + gfMembers_ENG[idx]).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)

def createCroppedImg(original, face):
    x = face['box'][0]
    y = face['box'][1]
    w = face['box'][2]
    h = face['box'][3]
    if w < 55 or h < 75:
        return None #too small
    return Image.fromarray(original[y : y + h, x : x + w]).convert('L')

def cropFace(idx):
    memberName = gfMembers_ENG[idx]
    imgSet = os.listdir(ORIGINAL_PATH + memberName)
    fixedCnt = 1
    unFixedCnt = 1
    detector = MTCNN()

    for img in imgSet:
        try:
            imgDir = ORIGINAL_PATH + memberName + '/' + img
            rgbImg = cv2.cvtColor(cv2.imread(imgDir), cv2.COLOR_BGR2RGB) # return numpy array type            
            results = detector.detect_faces(rgbImg)

            if len(results) == 0:
                continue
            elif len(results) == 1:
                cropImg = createCroppedImg(rgbImg, results[0])
                if cropImg:
                    cropImg.save(DATA_PATH + memberName + '/' + format(fixedCnt, '05') + '.png')
                    fixedCnt += 1
            else:
                for res in results:
                    cropImg = createCroppedImg(rgbImg, res)
                    if cropImg:
                        cropImg.save(UNFIXED_PATH + memberName + '/' + memberName + '_' + format(unFixedCnt, '05') + '.png')
                        unFixedCnt += 1
                
        except Exception as ex:
            print(ex)

def cropWork(idx):
    findOrCreateDirectory(idx)
    cropFace(idx)

# Main
threadList = []
for idx in range(0, 6):
    th = threading.Thread(target=cropWork, args=(idx, ), name='thread_' + gfMembers_ENG[idx])
    threadList.append(th)
    th.start()

for thread in threadList:
    thread.join()