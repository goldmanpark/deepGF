# ref : 
# https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
# https://beomi.github.io/gb-crawling/posts/2017-02-27-HowToMakeWebCrawler-With-Selenium.html
# https://yobbicorgi.tistory.com/29
# https://velog.io/@log327/Python-Selenium-Explicit-Waits-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

import os
import io
import time
import threading
import logging
import datetime
import urllib.request
from pathlib import Path
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from mtcnn import MTCNN
from PIL import Image
import cv2

# Initialize global vaiables
gfMembers_KOR = ['소원', '예린', '은하', '유주', '신비', '엄지']
gfMembers_ENG = ['SOWON', 'YERIN', 'EUNHA', 'YUJU', 'SINB', 'UMJI']
threadStart = [False, False, False, False, False, False]
chromeDriverLocation = os.getcwd() + '/chromedriver.exe'

# error Logger setting
Path(os.getcwd() + '/ERROR').mkdir(parents=True, exist_ok=True)
errLogName = 'ERROR/' + datetime.datetime.now().strftime('%Y_%m_%d') + '.log'
logging.basicConfig(filename=errLogName, filemode='w', encoding='utf-8', level=logging.ERROR)
loggerLock = threading.Lock()

def findOrCreateDirectory(idx):
    try:
        Path(os.getcwd() + '/' + gfMembers_ENG[idx]).mkdir(parents=True, exist_ok=True)
        Path(os.getcwd() + '/' + gfMembers_ENG[idx] + '/ORIGINAL').mkdir(parents=True, exist_ok=True)
        Path(os.getcwd() + '/' + gfMembers_ENG[idx] + '/FACE').mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)

def storeMemberImage_Google(idx, lock):
    option = webdriver.ChromeOptions()
    option.add_argument('log-level=3')  # to skip inevitable handshake err log
    chromeDriver = webdriver.Chrome(chromeDriverLocation, options=option)
    chromeDriver.implicitly_wait(3)
    #chromeWait = WebDriverWait(chromeDriver, 10, poll_frequency=1)
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
    while True:
        chromeDriver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = chromeDriver.execute_script('return document.body.scrollHeight')
        try:
            chromeDriver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height
    
    # 2. Count images and download all    
    currentBodyCount = len(chromeDriver.find_elements_by_css_selector('.rg_i.Q4LuWd'))
    for i in range(1, currentBodyCount):
        try:
            # click thumbnail to get larger image
            chromeDriver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]').click()
            # WebDriverWait cannot wait until image is fully loaded
            # chromeWait.until(EC.presence_of_element_located((By.XPATH, XPATH_IMG)))
            # chromeWait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))
            # chromeWait.until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
            time.sleep(1.5) # brute but perfect

            # store original image
            imgUrl = chromeDriver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img').get_attribute('src')
            imgDir = os.getcwd() + '/' + gfMembers_ENG[idx] + '/ORIGINAL/google_' + format(i, '05') + '.png'
            urllib.request.urlretrieve(imgUrl, imgDir)
            
            # face detection and crop, store
            rgbImg = cv2.cvtColor(cv2.imread(imgDir), cv2.COLOR_BGR2RGB) #numpy array type
            detector = MTCNN()
            for result in detector.detect_faces(rgbImg):
                x = result['box'][0]
                y = result['box'][1]
                w = result['box'][2]
                h = result['box'][3]
                cropImg = Image.fromarray(rgbImg[y : y + h, x : x + w]) #image
                cropImg.save(os.getcwd() + '/' + gfMembers_ENG[idx] + '/FACE/google_' + format(i, '05') + '.png')                

        except Exception as ex:
            with lock:
                print(gfMembers_ENG[idx] + '(' + format(i, '05') + ') :')
                print(ex)
                logging.error(gfMembers_ENG[idx] + '(' + format(i, '05') + ') :')
                logging.error(ex)
            pass

    chromeDriver.close()
    print(gfMembers_ENG[idx] + ' finished')

# Main
threadList = []
for idx in range(0, 6):
    findOrCreateDirectory(idx)
    th = threading.Thread(target=storeMemberImage_Google, args=[idx, loggerLock], name='thread_' + gfMembers_ENG[idx])
    th.start()

for thread in threadList:
    thread.join()

print('Finished!')