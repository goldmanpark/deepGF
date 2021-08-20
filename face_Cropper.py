import os
import cv2
from mtcnn import MTCNN
from PIL import Image

# Initialize global vaiables
gfMembers_KOR = ['소원', '예린', '은하', '유주', '신비', '엄지']
gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']
threadStart = [False, False, False, False, False, False]

# directory path
chromeDriverPath = os.getcwd() + '/chromedriver.exe'
#ORIGINAL_PATH = os.getcwd() + '/ORIGINAL/'
ORIGINAL_PATH = 'D:\ORIGINAL/'
UNFIXED_PATH =  os.getcwd() + '/UNFIXED/'
DATA_PATH = os.getcwd() + '/DATA/'

def createCroppedImg(original, face):
    x = face['box'][0]
    y = face['box'][1]
    w = face['box'][2]
    h = face['box'][3]
    if w < 55 or h < 75:
        return None #too small
    return Image.fromarray(original[y : y + h, x : x + w]).convert('L')

def cropFace(idx, logger):
    memberName = gfMembers_ENG[idx]
    imgSet = os.listdir(ORIGINAL_PATH + memberName)
    cnt = 0
    logger.writeProcesslog('crop start', 'target image: ' + str(len(imgSet)))
    for img in imgSet:
        try:
            imgDir = ORIGINAL_PATH + memberName + '/' + img
            rgbImg = cv2.cvtColor(cv2.imread(imgDir), cv2.COLOR_BGR2RGB) # return numpy array type
            detector = MTCNN()
            results = detector.detect_faces(rgbImg)
            if len(results) == 0:
                logger.writeErrorlog('no faces detected', imgDir)
            elif len(results) == 1:
                cropImg = createCroppedImg(rgbImg, results[0])
                if cropImg:
                    cropImg.save(DATA_PATH + memberName + '/' + format(cnt, '05') + '.png')
                    cnt += 1
            else:
                cnts = []
                for res in results:
                    cropImg = createCroppedImg(rgbImg, res)
                    if cropImg:
                        cropImg.save(UNFIXED_PATH + memberName + '/' + memberName + '_' + format(cnt, '05') + '.png')                    
                        cnts.append(format(cnt, '05'))
                        cnt += 1
                if len(cnts) > 1:
                    logger.writeErrorlog('2 or more faces detected : ' + str(cnts), imgDir)
        except Exception as ex:
            logger.writeErrorlog(type(ex).__name__, imgDir + '/n' + str(ex))
    logger.writeProcesslog('crop end', 'face images: ' + str(len(os.listdir(DATA_PATH + memberName ))))
    logger.writeProcesslog('crop end', 'unfixed face images: ' + str(len(os.listdir(UNFIXED_PATH + memberName))))
