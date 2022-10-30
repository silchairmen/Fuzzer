from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import requests as req
from bs4 import BeautifulSoup


#request 헤더 구성을 위하여 에이전트 정보를 가져옵니다
def get_agent_info(chrome):
    try:
        print("에이전트정보를 가져옵니다. href = www.whatismybrowser.com")
        chrome.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
        agent = chrome.find_element(By.ID, 'detected_value')
        agent_info = agent.text
        return agent_info

    except:
        agent_info = input("에이전트 정보를 불러올 수 없습니다. 브라우저 에이전트 정보를 직접 입력해 주세요\nAgent = ")
        return agent_info


#드라이버가 있는지 없는지 파악하고, 있다면 경로를 반환합니다. 없으면 다운로드하고 경로를 반환합니다.
def check_driver():
    print("Chrome 정보를 확인합니다..")
    chrome_driver = ChromeDriverManager().install()
    print(f" Chrome 정보. 경로 : {chrome_driver}")
    return chrome_driver


#기본적으로 젠킨스 사이트에 로그인하는 함수, selenium을 사용하여 직접적으로 접근함
def login(Chrome, id, pw, option):
    if option=='first_login':
        try:
            Chrome.find_element(By.NAME, 'j_username').send_keys(id)
            Chrome.find_element(By.NAME, 'j_password').send_keys(pw)
            Chrome.find_element(By.NAME, 'Submit').click()
            print(f"유저 : {id} 비밀번호 : {pw} 로그인 성공")
            #Chrome.find_element(By.ID, 'remember_me').click()
        except Exception as e:
            print(f"유저 : {id} 비밀번호 : {pw} 로그인 실패" + str(e))
    else:
        Chrome.find_element(By.NAME, 'j_username').send_keys(id)
        Chrome.find_element(By.NAME, 'j_password').send_keys(pw)
        sleep(0.5)
        Chrome.find_element(By.NAME, 'Submit').click()

#셀레니움에서 js로 접근해서


def check_dir(dir_name):
    path = os.listdir("./")
    if dir_name not in path:
        try:
            print(f"{dir_name}이 존재하지 않습니다... 생성합니다.....\n")
            os.system(f"mkdir {dir_name}")
            print("생성되었습니다.\n")
        except:
            print("permission error")


def check_csv_file(Frame_name, file_name, file_list):
    while True:
        if file_name in file_list:
            choice = input(f"{file_name} 이 존재합니다. 덮어 씌울까요? y/n\ny/n = ")
            if choice == 'y':
                try:
                    Frame_name.to_csv(f"./csv/{file_name}")
                    break
                    print("success")
                except:
                    print("유저 이름에 파일 이름으로 생성할 수 없는 문자가 들어가 있습니다 !")

            elif choice == 'n':
                break
                print("파일을 저장하지 않고 종료합니다")
            else:
                print("wrong! chose y or n")
        else:
            Frame_name.to_csv(f"./csv/{file_name}")
            print(f"<{file_name}> is created")
            break

def get_session(Chrome, user_agent):
    session = req.session()
    headers = {
        "User-Agent" : user_agent
    }
    session.headers.update(headers)

    for cookie in Chrome.get_cookies():
        c = {cookie['name']:cookie['value']}
        session.cookies.update(c)

    return session