# ref : 
# https://levelup.gitconnected.com/how-to-download-google-images-using-python-2021-82e69c637d59
# https://beomi.github.io/gb-crawling/posts/2017-02-27-HowToMakeWebCrawler-With-Selenium.html
# https://yobbicorgi.tistory.com/29
# https://velog.io/@log327/Python-Selenium-Explicit-Waits-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0

import os
import threading
import urllib.request
import sys
import json
from selenium import webdriver
from scraper_class import Scraper

def scrap_work(worker, workerIdx, threadStart):
    print(worker.ENG_NAME + ' scrap started')
    worker.findOrCreateDirectory()
    worker.init_browser()

    # wait until browsers in other threads can start
    threadStart[workerIdx] = True    
    while not all(threadStart):
        pass
    
    worker.store_member_images()
    print(worker.ENG_NAME + 'scrap finished')

def main():
    try:
        if len(sys.argv) == 1:
            print("argv error")
            sys.exit(0)

        selected_group = {}
        with open(os.getcwd() + '/idol_list.json', encoding='UTF8') as f:
            json_data = json.loads(f.read())
            selected_group = json_data[sys.argv[1]]

        # directory path
        DRIVER_PATH = os.getcwd() + '/chromedriver.exe'
        SAVE_PATH = 'D:\DeepLearning_DATA/' + selected_group['group_eng'] + '/ORIGINAL/'
        
        threadList = []
        threadStart = [False for _ in range(len(selected_group['members']))]

        for idx, member in enumerate(selected_group['members']):
            worker = Scraper(save_path=SAVE_PATH, driver_path=DRIVER_PATH, kor_group=selected_group['group_kor'], 
                            kor_name=member['kor'], eng_name=member['eng'])
            th = threading.Thread(target=scrap_work, args=(worker, idx, threadStart), name='thread_' + member['eng'])
            threadList.append(th)
            th.start()

        for thread in threadList:
            thread.join()

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()