# ref : 
# https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
# https://beomi.github.io/gb-crawling/posts/2017-02-27-HowToMakeWebCrawler-With-Selenium.html
# https://yobbicorgi.tistory.com/29

import os
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver

# Initialize..
gfMembers = ['소원', '예린', '은하', '유주', '신비', '엄지']
chromeDriverLocation = os.getcwd() + '/chromedriver.exe'
chromeDriver = webdriver.Chrome(chromeDriverLocation)
chromeDriver.implicitly_wait(3)

def getMemberThumbnail(name):
    chromeDriver.get('https://www.google.co.kr/imghp?hl=ko')
    chromeDriver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input').send_keys('여자친구 ' + name)
    chromeDriver.find_element_by_xpath('//*[@id="sbtc"]/button').click()

    for i in range(1,100):
        try:
            chromeDriver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(os.getcwd() + '/' + name + '/' + str(i) + '.png')
        except Exception as e:
            print(e)
            pass

for name in gfMembers:
    Path(os.getcwd() + '/' + name).mkdir(parents=True, exist_ok=True)
    getMemberThumbnail(name)
