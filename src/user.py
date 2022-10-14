from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from time import sleep

def login(Chrome, id,pw):
    try:
        Chrome.find_element(By.NAME, 'j_username').send_keys(id)
        Chrome.find_element(By.NAME, 'j_password').send_keys(pw)
        sleep(1)
        Chrome.find_element(By.NAME, 'Submit').click()
        print(f"유저 : {id} 비밀번호 : {pw} 로그인 성공")
    except:
        print(f"유저 : {id} 비밀번호 : {pw} 로그인 실패")