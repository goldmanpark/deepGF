# ref : 
# https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
# https://beomi.github.io/gb-crawling/posts/2017-02-27-HowToMakeWebCrawler-With-Selenium.html
# https://yobbicorgi.tistory.com/29
# https://velog.io/@log327/Python-Selenium-Explicit-Waits-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

import os
import time
import threading
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# Initialize..
gfMembers = ['소원', '예린', '은하', '유주', '신비', '엄지']
threadStart = [False, False, False, False, False, False]
XPATH_IMG = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'
chromeDriverLocation = os.getcwd() + '/chromedriver.exe'

def findOrCreateDirectory(name):
    try:
        Path(os.getcwd() + '/' + name).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)

def storeMemberImage(idx):
    name = gfMembers[idx]
    chromeDriver = webdriver.Chrome(chromeDriverLocation)
    chromeDriver.implicitly_wait(3)
    #chromeWait = WebDriverWait(chromeDriver, 10, poll_frequency=1)
    chromeDriver.get('https://www.google.co.kr/imghp?hl=ko')
    chromeDriver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input').send_keys('여자친구 ' + name)
    chromeDriver.find_element_by_xpath('//*[@id="sbtc"]/button').click()
    
    # wait until browsers in other threads can start
    threadStart[idx] = True    
    while not all(threadStart):
        pass

    for i in range(1,20):
        try:
            chromeDriver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]').click()
            # WebDriverWait cannot wait until image is fully loaded
            # chromeWait.until(EC.presence_of_element_located((By.XPATH, XPATH_IMG)))
            # chromeWait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n3VNCb')))
            # chromeWait.until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
            time.sleep(2) # brute but perfect
            src = chromeDriver.find_element_by_xpath(XPATH_IMG).get_attribute('src')
            urllib.request.urlretrieve(src, os.getcwd() + '/' + name + '/google_' + format(i, '05') + '.png')
        except Exception as e:
            print(e)
            pass

    chromeDriver.close()

threadList = []
for idx in range(0, 6):
    findOrCreateDirectory(gfMembers[idx])
    th = threading.Thread(target=storeMemberImage, args=(idx,))
    th.start()

for thread in threadList:
    thread.join()

print('Finished!')