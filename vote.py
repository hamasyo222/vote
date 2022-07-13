# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome import service as fs
import traceback
import sys



options = Options()
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions');
options.add_argument('--proxy-server="direct://"');
options.add_argument('--proxy-bypass-list=*');
options.add_argument('--start-maximized');
#options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

#
# Chromeドライバーの起動
#
DRIVER_PATH = '/app/.chromedriver/bin/chromedriver' #heroku
#DRIVER_PATH = '/Users/hamasyo/Selenium/chromedriver' #ローカル
chrome_sevice = fs.Service(DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_sevice, options=options)
driver.implicitly_wait(20)

urls = ["https://liff.line.me/1656040756-GwmBkdPY/vote/mrgakushuin2022/M/3", "https://liff.line.me/1656040756-GwmBkdPY/vote/kokugakuin2022/N/1"]

#ライン認証
def line(driver):
  #ライン認証
  #ID
  driver.find_element(By.CSS_SELECTOR,'#app > div > div > div > div.MdBox01 > div > form > fieldset > div:nth-child(2) > input[type=text]').send_keys("hamasyo222@docomo.ne.jp")#

  #パスワード
  driver.find_element(By.CSS_SELECTOR,'#app > div > div > div > div.MdBox01 > div > form > fieldset > div:nth-child(3) > input[type=password]').send_keys("hamaguti222")#

  #ログイン
  driver.find_element(By.CSS_SELECTOR,'#app > div > div > div > div.MdBox01 > div > form > fieldset > div.mdFormGroup01Btn > button').click()


#投票
def vote(driver, urls, i):
  #〇〇に投票
  driver.get(urls[i])

  #はじめのみライン認証
  if i == 0:
    line(driver)

  #投票
  driver.find_element(By.CSS_SELECTOR,'#root > div > div:nth-child(1) > div > form:nth-child(2) > div > div > div > button').click()

  #時間停止
  time.sleep(3)

  w = driver.execute_script("return document.body.scrollWidth;")
  h = driver.execute_script("return document.body.scrollHeight;")

  # set window size
  driver.set_window_size(w,h)

  # Get Screen Shot
  driver.save_screenshot(f"image{i}.jpeg")

  #ライン送信
  main_gazo(i)

#ライン送信
def main_gazo(i):
    url = "https://notify-api.line.me/api/notify"
    token = "1M36qrYaziRpapUJXjlPZT0sGL0NX9fnjSlYZqVBph2"
    headers = {"Authorization" : "Bearer "+ token}

    message = i
    payload = {"message" :  message}
    #imagesフォルダの中のgazo.jpg
    files = {"imageFile":open(f'image{i}.jpeg','rb')}
    #rbはバイナリファイルを読み込む
    post = requests.post(url ,headers = headers ,params=payload,files=files)

for i in range(len(urls)):
  vote(driver, urls, i)