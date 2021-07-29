# ref : 
# https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
# https://beomi.github.io/gb-crawling/posts/2017-02-27-HowToMakeWebCrawler-With-Selenium.html
# https://yobbicorgi.tistory.com/29
# https://velog.io/@log327/Python-Selenium-Explicit-Waits-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

import os
import time
import threading
import urllib.request
import atexit
import cv2
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mtcnn import MTCNN
from PIL import Image
# custom class
from scrap_Logger import ScrapLogger

# Initialize global vaiables
gfMembers_KOR = ['소원', '예린', '은하', '유주', '신비', '엄지']
gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']
threadStart = [False, False, False, False, False, False]
chromeDriverLocation = os.getcwd() + '/chromedriver.exe'

# selenium option
chromeDriverOptions = webdriver.ChromeOptions()
chromeDriverOptions.add_argument('log-level=3')  # to skip inevitable handshake err log
chromeDriverOptions.add_argument("--disable-extensions")
chromeDriverOptions.add_argument("disable-infobars")
chromeDriverOptions.add_argument('window-size=1920x1080') 
chromeDriverOptions.add_argument("disable-gpu")
chromeDriverOptions.add_argument('headless')

# request option
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')] #to prevent HTTP Error 403: Forbidden
urllib.request.install_opener(opener)

def findOrCreateDirectory(idx):
    try:
        Path(os.getcwd() + '/' + gfMembers_ENG[idx]).mkdir(parents=True, exist_ok=True)
        Path(os.getcwd() + '/' + gfMembers_ENG[idx] + '/ORIGINAL').mkdir(parents=True, exist_ok=True)
        Path(os.getcwd() + '/' + gfMembers_ENG[idx] + '/FACE').mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)

def storeMemberImage_Google(idx, logger):
    memberName = gfMembers_ENG[idx]

    # chromeDriver setting    
    chromeDriver = webdriver.Chrome(chromeDriverLocation, options=chromeDriverOptions)
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
        if new_height == last_height and count == 5:
            break
        if new_height == last_height and count < 5: # new_height == last_height -> counting.
            count += 1
            scroll_sec += 0.5
        if new_height != last_height and count > 0:
            count = 0
            scroll_sec = 1.5
        last_height = new_height
    
    # 2. Count images and download all
    XPATH_IMG = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'
    images = chromeDriver.find_elements_by_css_selector('.rg_i.Q4LuWd')
    print(memberName + '_img_count = ' + str(len(images)))

    for i in range(0, len(images)):
        try:
            imgUrl = ''
            for cnt in range(5):
                try:
                    images[i].click()
                    chromeWait.until(EC.presence_of_element_located((By.XPATH, XPATH_IMG)))
                    imgUrl = chromeDriver.find_element_by_xpath(XPATH_IMG).get_attribute('src')
                    if imgUrl.startswith('http') == False and cnt < 4:
                        time.sleep(1.5)
                        continue
                    else:
                        break
                except Exception as ex:
                    if cnt < 4:
                        time.sleep(3)
                    else:
                         raise ex

            if imgUrl == '':
                logger.writeErrorlog('no url detected', imgUrl)
                continue
            if imgUrl.startswith('http') == False:
                logger.writeErrorlog('abnormal img src', imgUrl)
                continue

            imgDir = os.getcwd() + '/' + memberName + '/ORIGINAL/google_' + format(i, '05') + '.png'
            urllib.request.urlretrieve(imgUrl, imgDir)
        except Exception as ex:
            logger.writeErrorlog(type(ex).__name__, str(i) + ' : ' + imgUrl + '\n' + str(ex))
                
    chromeDriver.close()
    print(memberName + ' finished')

def cropFace(idx, logger):
    memberName = gfMembers_ENG[idx]
    imgSet = os.listdir(os.getcwd() + '/' + memberName + '/ORIGINAL')
    cnt = 0
    for img in imgSet:
        try:
            imgDir = os.getcwd() + '/' + memberName + '/ORIGINAL/' + img
            rgbImg = cv2.cvtColor(cv2.imread(imgDir), cv2.COLOR_BGR2RGB) # return numpy array type
            detector = MTCNN()
            results = detector.detect_faces(rgbImg)
            if len(results) == 1:
                res = results[0]
                x = res['box'][0]
                y = res['box'][1]
                w = res['box'][2]
                h = res['box'][3]
                cropImg = Image.fromarray(rgbImg[y : y + h, x : x + w])
                cropImg.save(os.getcwd() + '/' + memberName + '/FACE/google_' + format(cnt, '05') + '.png')
                cnt += 1
            elif len(results) == 0:
                logger.writeErrorlog('no faces detected', imgDir)
            else:   #len(results) > 1
                logger.writeErrorlog('2 or more faces detected', imgDir)
        except Exception as ex:
            logger.writeErrorlog(type(ex).__name__, imgDir + '/n' + str(ex))

def scrapWork(idx):
    logger = ScrapLogger(gfMembers_ENG[idx])
    storeMemberImage_Google(idx, logger)
    cropFace(idx, logger)
    print('Finished!')

# Main
threadList = []
for idx in range(0, 6):
    findOrCreateDirectory(idx)
    th = threading.Thread(target=scrapWork, args=(idx, ), name='thread_' + gfMembers_ENG[idx])
    th.start()

for thread in threadList:
    thread.join()