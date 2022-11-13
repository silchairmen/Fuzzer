from selenium import webdriver
from selenium.webdriver.common.by import By
from time import time
from src.func import *
from tqdm import tqdm

class build_option:
    def __init__(self,chrome, url, port, id, pw, job_name):
        self.chrome = chrome
        self.full_url = f"http:{url}:{port}/job/{job_name}/configure"
        self.id = id
        self.pw = pw

        #접근 후 로그인
        self.chrome.get(self.full_url)
        login(self.chrome,id,pw,"first_login")
        sleep(2)


    #빌드 옵션만 추가
    def add_build_step_all(self):
        #빌드 옵션 버튼을 가져와서 화면 중앙에 두고 클릭
        chrome = self.chrome
        add_option_btn = get_add_build_option_button(chrome)
        save_btn, apply_btn = get_submit_and_apply_button(chrome)

        #빌드 add 부분으로 이동 (처음 클릭해줘야 bd 태그를 가져올 수 있음)
        scroll_to_element(chrome, add_option_btn)
        sleep(3)
        add_option_btn.click()

        board = chrome.find_elements(By.CLASS_NAME, "bd")
        li_list = board[-1].find_elements(By.TAG_NAME, "li")

        for i in tqdm(range(0,len(li_list)),mininterval=2):
            chrome.execute_script("arguments[0].click();", li_list[i])
            li_name = li_list[i].find_element(By.TAG_NAME, "a").get_attribute("innerHTML")
            sleep(2)
            apply_btn.click()
            sleep(1.5)
            error_status = jenkins_error_alert(chrome)
            sleep(1.5)

            if error_status==True:
                #@todo li name에서 긁은거 div box가서 x버튼 클릭해줘야함
                error_divs = chrome.find_elements(By.TAG_NAME, "div")
                error_divs.reverse()
                for error_div in error_divs:
                    if error_div.get_attribute("innerText").startswith(li_name):
                        del_buttons = error_div.find_element(By.TAG_NAME, "button")
                        del_buttons.click()
                        sleep(2)
                        break

            elif error_status==False and (i<len(li_list)-2):
                scroll_to_element(chrome, add_option_btn)
                sleep(3)
                add_option_btn.click()



    #빌드 후 조치 추가
    def add_option_after_build(self):
        chrome = self.chrome
        add_after_build_btn = get_add_after_build_button(chrome)
        save_btn, apply_btn = get_submit_and_apply_button(chrome)

        #빌드 add 부분으로 이동 (처음 클릭해줘야 bd 태그를 가져올 수 있음)
        scroll_to_element(chrome, add_after_build_btn)
        sleep(2)
        add_after_build_btn.click()

        board = chrome.find_elements(By.CLASS_NAME, "bd")
        li_list = board[-1].find_elements(By.TAG_NAME, "li")

        for i in tqdm(range(0,len(li_list)),mininterval=2):
            chrome.execute_script("arguments[0].click();", li_list[i])
            li_name = li_list[i].find_element(By.TAG_NAME, "a").get_attribute("innerHTML")
            sleep(1)
            apply_btn.click()
            sleep(2)
            error_status = jenkins_error_alert(chrome)

            if error_status==True:
                #@todo li name에서 긁은거 div box가서 x버튼 클릭해줘야함
                error_divs = chrome.find_elements(By.TAG_NAME, "div")
                error_divs.reverse()
                for error_div in error_divs:
                    if error_div.get_attribute("innerText").startswith(li_name):
                        del_buttons = error_div.find_element(By.TAG_NAME, "button")
                        del_buttons.click()
                        sleep(1.5)
                        break

            elif error_status==False and (i<len(li_list)-2):
                scroll_to_element(chrome, add_after_build_btn)
                sleep(2.5)
                add_after_build_btn.click()
    #모든 옵션 삭제
    def delete_all_options(self):
        chrome = self.chrome
        delete_button = chrome.find_elements(By.TAG_NAME, "button")
        delete_button.reverse()
        for del_btn in tqdm(delete_button,mininterval=2):
            if del_btn.get_attribute("tooltip") == "삭제" and del_btn.get_attribute('title') == "삭제":
                scroll_to_element(chrome,del_btn)
                sleep(1.5)
                try:
                    del_btn.click()
                    sleep(1.5)
                except:
                    pass
        submit_btn, apply_btn = get_submit_and_apply_button(chrome)
        apply_btn.click()
        sleep(1)
        print("options are deleted")