# ref : 
# https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
# https://beomi.github.io/gb-crawling/posts/2017-02-27-HowToMakeWebCrawler-With-Selenium.html
# https://yobbicorgi.tistory.com/29
# https://velog.io/@log327/Python-Selenium-Explicit-Waits-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

import os
import time
import threading
import urllib.request
import io
import datetime
import cv2
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from fake_useragent import UserAgent
from mtcnn import MTCNN
from PIL import Image
from scrap_Logger import ScrapLogger

# Initialize global vaiables
gfMembers_KOR = ['소원', '예린', '은하', '유주', '신비', '엄지']
gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']
threadStart = [False, False, False, False, False, False]

# directory path
chromeDriverPath = os.getcwd() + '/chromedriver.exe'
ORIGINAL_PATH = os.getcwd() + '/ORIGINAL/'
UNFIXED_PATH =  os.getcwd() + '/UNFIXED/'
DATA_PATH = os.getcwd() + '/DATA/'

# selenium option
chromeDriverOptions = webdriver.ChromeOptions()
chromeDriverOptions.add_argument('log-level=3')  # to skip inevitable handshake err log
chromeDriverOptions.add_argument("--ignore-certificate-error")
chromeDriverOptions.add_argument("--ignore-ssl-errors")
chromeDriverOptions.add_argument("--disable-extensions")
chromeDriverOptions.add_argument('headless')
chromeDriverOptions.add_argument('--no-sandbox')
#chromeDriverOptions.add_argument(f'user-agent={UserAgent().random}')
chromeDriverOptions.add_argument("disable-infobars")
chromeDriverOptions.add_argument("disable-gpu")

# request option
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')] #to prevent HTTP Error 403: Forbidden
urllib.request.install_opener(opener)

def findOrCreateDirectory(idx):
    try:
        Path(ORIGINAL_PATH + gfMembers_ENG[idx]).mkdir(parents=True, exist_ok=True)
        Path(UNFIXED_PATH + gfMembers_ENG[idx]).mkdir(parents=True, exist_ok=True)
        Path(DATA_PATH + gfMembers_ENG[idx]).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)

def storeMemberImage_Google(idx, logger):
    memberName = gfMembers_ENG[idx]

    # chromeDriver setting    
    chromeDriver = webdriver.Chrome(chromeDriverPath, options=chromeDriverOptions)
    chromeDriver.set_window_size(1920, 1080)
    chromeDriver.implicitly_wait(3)
    chromeWait = WebDriverWait(chromeDriver, 10, poll_frequency=1)
    chromeDriver.get('https://www.google.co.kr/imghp?hl=ko')
    chromeDriver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input').send_keys('여자친구 ' + gfMembers_KOR[idx])
    chromeDriver.find_element_by_xpath('//*[@id="sbtc"]/button').click()
    chromeDriver.implicitly_wait(2)
    
    # wait until browsers in other threads can start
    threadStart[idx] = True    
    while not all(threadStart):
        pass

    # 1. Scrolling down until cannot scroll no more
    last_height = chromeDriver.execute_script('return document.body.scrollHeight')
    count = 0
    scroll_sec = 1.5
    while True:
        chromeDriver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(scroll_sec)
        new_height = chromeDriver.execute_script('return document.body.scrollHeight')
        if new_height == last_height and count == 3:
            break
        if new_height == last_height and count < 3: # new_height == last_height -> counting.
            count += 1
            scroll_sec += 0.5
        if new_height != last_height and count > 0:
            count = 0
            scroll_sec = 1.5
        last_height = new_height
    
    # 2. Count images and download all
    XPATH_IMG = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'
    images = chromeDriver.find_elements_by_css_selector('.rg_i.Q4LuWd')
    logger.writeProcesslog('scrap start', memberName + '_img_count = ' + str(len(images)))

    maxTry = 5
    for i in range(0, len(images)):
        startDttm = datetime.datetime.now()
        compFlag = True
        imgUrl = ''
        try:
            images[i].click()
            chromeWait.until(EC.presence_of_element_located((By.XPATH, XPATH_IMG)))
            for tryCnt in range(maxTry):        
                try:
                    imgUrl = chromeDriver.find_element_by_xpath(XPATH_IMG).get_attribute('src')
                    if imgUrl.startswith('http') == False or imgUrl.startswith('https://encrypted-tbn0') or imgUrl == '':
                        if tryCnt == maxTry - 1:
                            logger.writeErrorlog('abnormal img src url', imgUrl)
                            compFlag = False
                            break
                        else:
                            time.sleep(1.5)
                            continue

                    imgData = Image.open(io.BytesIO(urllib.request.urlopen(imgUrl).read()))
                    if imgData.width <= 250 or imgData.height <= 250:
                        if tryCnt == maxTry - 1:
                            logger.writeErrorlog('too small image', imgUrl)
                            compFlag = False
                            break
                        else:
                            time.sleep(1.5)
                            continue

                    imgData.save(ORIGINAL_PATH + memberName + '/google_' + format(i, '05') + '.png')
                    compFlag = True
                    break
                except Exception as ex:
                    if tryCnt == maxTry - 1:
                        logger.writeErrorlog(type(ex).__name__, str(i) + ' : ' + imgUrl + '\n' + str(ex))
                        compFlag = False
                    else:
                        time.sleep(2)
        except Exception as ex:
            logger.writeErrorlog(type(ex).__name__, str(i) + ' : ' + imgUrl + '\n' + str(ex))
        
        endDttm = datetime.datetime.now()
        if compFlag == True:
            logger.writeProcesslog(str(i), str(endDttm - startDttm))
        else:
            logger.writeProcesslog(str(i) + ' : ERROR', str(endDttm - startDttm))

    chromeDriver.close()
    logger.writeProcesslog('scrap end', 'image scrapped: ' + str(len(os.listdir(ORIGINAL_PATH + memberName))))

def createCroppedImg(original, face):
    x = face['box'][0]
    y = face['box'][1]
    w = face['box'][2]
    h = face['box'][3]
    if w <= 35 or h <= 35:
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

def scrapWork(idx):
    logger = ScrapLogger(gfMembers_ENG[idx])
    findOrCreateDirectory(idx)
    storeMemberImage_Google(idx, logger)
    cropFace(idx, logger)
    print(gfMembers_ENG[idx] + ' finished')

# Main
threadList = []
for idx in range(0, 6):
    th = threading.Thread(target=scrapWork, args=(idx, ), name='thread_' + gfMembers_ENG[idx])
    th.start()

for thread in threadList:
    thread.join()