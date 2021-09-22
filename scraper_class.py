import time
import urllib.request
import io
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

class Scraper():
    def __init__(self, save_path, driver_path, kor_group, kor_name, eng_name):
        self.SAVE_PATH = save_path
        self.DRIVER_PATH = driver_path
        self.KOR_GROUP = kor_group
        self.KOR_NAME = kor_name
        self.ENG_NAME = eng_name

        # request option to prevent HTTP Error 403: Forbidden
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

    def print_exception(self, ex):
        print(ex)

    def init_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('log-level=3')  # to skip inevitable handshake err log
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-extensions")
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument("disable-infobars")
        options.add_argument("disable-gpu")
        self.CHROME_DRIVER = webdriver.Chrome(self.DRIVER_PATH, options=options)        
        self.CHROME_DRIVER.set_window_size(1920, 1080)
        self.CHROME_DRIVER.implicitly_wait(3)
        self.CHROME_WAIT = WebDriverWait(self.CHROME_DRIVER, 10, poll_frequency=1)

    def findOrCreateDirectory(self):
        try:
            Path(self.SAVE_PATH + self.ENG_NAME).mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            self.print_exception(ex)

    def select_color(self, colorIdx):
        INPUT = '//*[@id="sbtc"]/div/div[2]/input'
        SEARCH_BTN = '//*[@id="sbtc"]/button'
        TOOL_BTN = '//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div/div'
        COLOR_BTN = '//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[1]/div/div[2]/div/div[1]'
        COLOR_ITEM = '//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[3]/div/div/a[' + str(colorIdx) + ']'
        for _ in range(5):
            try:
                self.CHROME_DRIVER.get('https://www.google.co.kr/imghp?hl=ko')
                self.CHROME_DRIVER.find_element_by_xpath(INPUT).send_keys(self.KOR_GROUP + ' ' + self.KOR_NAME)
                self.CHROME_DRIVER.find_element_by_xpath(SEARCH_BTN).click()
                self.CHROME_DRIVER.implicitly_wait(2)
                self.CHROME_DRIVER.find_element_by_xpath(TOOL_BTN).click() # 도구
                self.CHROME_DRIVER.implicitly_wait(2)
                self.CHROME_DRIVER.find_element_by_xpath(COLOR_BTN).click() # 색상
                self.CHROME_DRIVER.implicitly_wait(2)
                self.CHROME_DRIVER.find_element_by_xpath(COLOR_ITEM).click() # 색상선택
                self.CHROME_DRIVER.implicitly_wait(3)
                break
            except Exception as ex:
                self.print_exception(ex)
                continue

    def get_image_list(self):
        try:
            # 1. Scrolling down until cannot scroll no more
            last_height = self.CHROME_DRIVER.execute_script('return document.body.scrollHeight')
            count = 0
            scroll_sec = 1.5
            while True:
                self.CHROME_DRIVER.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(scroll_sec)
                new_height = self.CHROME_DRIVER.execute_script('return document.body.scrollHeight')
                time.sleep(scroll_sec)
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
            images = self.CHROME_DRIVER.find_elements_by_css_selector('.rg_i.Q4LuWd')
            return images
        except Exception as ex:
            self.print_exception(ex)
            return None

    def store_member_images(self):
        for colorIdx in range(1, 13):   # 1 ~ 12 colors
            self.select_color(colorIdx=colorIdx)
            images = self.get_image_list()

            XPATH_IMG = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'
            maxTry = 5
            for i in range(0, len(images)):
                imgUrl = ''
                try:
                    images[i].click()
                    self.CHROME_WAIT.until(EC.presence_of_element_located((By.XPATH, XPATH_IMG)))
                    for tryCnt in range(maxTry):
                        try:
                            imgUrl = self.CHROME_DRIVER.find_element_by_xpath(XPATH_IMG).get_attribute('src')
                            if imgUrl.startswith('http') == False or imgUrl.startswith('https://encrypted-tbn0') or imgUrl == '':
                                if tryCnt == maxTry - 1:
                                    break
                                else:
                                    time.sleep(1)
                                    continue

                            imgData = Image.open(io.BytesIO(urllib.request.urlopen(imgUrl).read()))
                            if imgData.width <= 250 or imgData.height <= 250:
                                if tryCnt == maxTry - 1:
                                    break
                                else:
                                    time.sleep(1)
                                    continue

                            imgData.save(self.SAVE_PATH + self.ENG_NAME + '/google_' + format(colorIdx, '02') + format(i, '05') + '.png')
                            break
                        except Exception as ex:
                            if tryCnt == maxTry - 1:
                                self.print_exception(type(ex).__name__ + '-' + str(i) + ' : ' + imgUrl + '\n' + str(ex))
                            else:
                                time.sleep(2)
                except Exception as ex:
                    self.print_exception(type(ex).__name__ + '-' + str(i) + ' : ' + imgUrl + '\n' + str(ex))

        self.CHROME_DRIVER.close()