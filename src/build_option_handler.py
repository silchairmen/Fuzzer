from src.func import *
from tqdm import tqdm
import requests as req
import json

class build_option:
    def __init__(self,chrome, url, port, id, pw, job_name,vm_num):
        self.chrome = chrome
        self.url = url
        self.job_name = job_name
        self.full_url = f"http:{url}:{port}/job/{job_name}/configure"
        self.id = id
        self.pw = pw
        self.vm_num = vm_num

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


    #담당자 : 이소연
    def add_option_all(self):
        url = f'http://{self.url}/login?from=%2F'
        login_url = f'http://{self.url}/j_spring_security_check'
        crumbI_url = f'http://{self.url}/crumbIssuer/api/json'
        job_config_url = f"http://{self.url}/job/{self.job_name}/configSubmit"

        session = req.session()

        set_data = {}
        with open(f"../jen/jen{self.vm_num}_all.json", "r") as f:
            set_data = json.load(f)

        # 로그인
        def login():
            session.get(url)
            login_data = {
                "j_username": "admin",
                "j_password": "admin",
                "from": "/",
                "Submit": ""
            }
            res = session.post(login_url, data=login_data)
            res.raise_for_status()

        # job_config
        def job_config(crumb):
            res = session.post(job_config_url, data={"Jenkins-Crumb": crumb, "json": json.dumps(set_data)})
            res.raise_for_status()

        def main():
            login()
            Jenkins_crumb_json = session.get(crumbI_url, cookies=(session.cookies.get_dict()))
            Jenkins_crumb_json = json.loads(Jenkins_crumb_json.text)

            crumb = Jenkins_crumb_json['crumb']
            set_data["Jenkins-Crumb"] = Jenkins_crumb_json['crumb']

            job_config(crumb)

        main()