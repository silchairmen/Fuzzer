from selenium import webdriver
from src.func import *

class build_option:
    def __init__(self):
        self.url = input("URL ex) 192.168.139.128:8080\nURL : ")
        self.id,self.pw = input("Login info id,pw ex) admin,admin\nID,PW : ").split(",")
        self.job_name = input("job name ex) test1\nJob name : ")
        self.error_stack = 0

    def build_option_add(self):
        url = f"http://{self.url}/job/{self.job_name}/configure"
        id, pw = self.id, self.pw

        script = """
                window.scrollTo(0,document.body.scrollHeight)
            """

        # 브라우저 실행 안하고 그냥 백그라운드로 돌리는 요소
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        chrome = webdriver.Chrome(check_driver(),options=chrome_options)

        # 로그인 후 url 접근
        chrome.get(url)
        sleep(1)
        login(chrome, id, pw, "first_login")

        button = chrome.find_elements(By.TAG_NAME, "button")
        # divs = chrome.find_elements(By.TAG_NAME, "div")

        # 저장, apply 버튼 설정
        for btn in button:
            if btn.get_attribute("innerHTML") == 'Apply':
                apply_btn = btn
            elif btn.get_attribute("innerHTML") == ('저장' or "save"):
                save_btn = btn

        # 빌드 버튼 전부 클릭
        for btn in button:
            if btn.get_attribute("class") == "hetero-list-add" and btn.get_attribute("suffix") == "builder":
                chrome.execute_script(script)
                sleep(1)
                btn.click()
                board = chrome.find_elements(By.CLASS_NAME, "bd")
                li_list = board[-1].find_elements(By.TAG_NAME, "li")

                for i in range(len(li_list)):
                    li_list[i].click()
                    sleep(1)
                    chrome.execute_script(script)
                    sleep(2)
                    apply_btn.click()
                    sleep(1)

                    # 빌드 버튼을 클릭하고 팝업창으로 에러가 드면 error=true 설정
                    try:
                        check_error = chrome.find_element(By.CLASS_NAME, "shadow").get_attribute("style")[:19]
                        if check_error == 'visibility: visible':
                            print("error")
                            self.error_stack +=1
                            error_status = True
                        else:
                            error_status = False
                    except:
                        print("no error")

                    # saved가 뜨는지 확인하기
                    notify = chrome.find_element(By.ID, "notification-bar")
                    notify_text = notify.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")

                    # 팝업창 에러 컨트롤 에러 => 에러 닫기 => 에러가 발생한 플러그인 없애기
                    if error_status != False:
                        chrome.find_element(By.CLASS_NAME, "container-close").click()
                        sleep(3)
                        delete_button = chrome.find_elements(By.TAG_NAME, "button")
                        delete_button.reverse()
                        for del_btn in delete_button:
                            if del_btn.get_attribute("tooltip") == "삭제" and del_btn.get_attribute('title') == "삭제":
                                del_btn.click()
                                sleep(3)
                                break

                    # @todo 만들긴 했는데 테스트를 못해봄, apply했을때 에러 핸들링
                    elif notify_text != "Saved":
                        delete_button = chrome.find_elements(By.TAG_NAME, "button")
                        delete_button.reverse()
                        for del_btn in delete_button:
                            if del_btn.get_attribute("tooltip") == "삭제" and del_btn.get_attribute('title') == "삭제":
                                del_btn.click()
                                break

                    sleep(1)
                    if i < len(li_list) - 1:
                        btn.click()

        #빌드 후 조치 클릭
        for btn in button:
            if btn.get_attribute("class") == "hetero-list-add" and btn.get_attribute("suffix") == "publisher":
                chrome.execute_script(script)
                sleep(1.5)
                btn.click()
                board = chrome.find_elements(By.CLASS_NAME, "bd")
                li_list = board[-1].find_elements(By.TAG_NAME, "li")

                #delete repo는 뺴고 추가해줌
                for i in range(len(li_list)-1):
                    li_list[i].click()
                    sleep(1)
                    chrome.execute_script(script)
                    sleep(2)
                    apply_btn.click()
                    sleep(1)

                    # 빌드 버튼을 클릭하고 팝업창으로 에러가 드면 error=true 설정
                    try:
                        check_error = chrome.find_element(By.CLASS_NAME, "shadow").get_attribute("style")[:19]
                        if check_error == 'visibility: visible':
                            print("error")
                            self.error_stack +=1
                            error_status = True
                        else:
                            error_status = False
                    except:
                        print("no error")

                    # saved가 뜨는지 확인하기
                    notify = chrome.find_element(By.ID, "notification-bar")
                    notify_text = notify.find_element(By.TAG_NAME, "span").get_attribute("innerHTML")

                    # 팝업창 에러 컨트롤 에러 => 에러 닫기 => 에러가 발생한 플러그인 없애기
                    if error_status != False:
                        chrome.find_element(By.CLASS_NAME, "container-close").click()
                        sleep(3)
                        delete_button = chrome.find_elements(By.TAG_NAME, "button")
                        delete_button.reverse()
                        for del_btn in delete_button:
                            if del_btn.get_attribute("tooltip") == "삭제" and del_btn.get_attribute('title') == "삭제":
                                del_btn.click()
                                sleep(3)
                                break

                    # @todo 만들긴 했는데 테스트를 못해봄, apply했을때 에러 핸들링
                    elif notify_text != "Saved":
                        delete_button = chrome.find_elements(By.TAG_NAME, "button")
                        delete_button.reverse()
                        for del_btn in delete_button:
                            if del_btn.get_attribute("tooltip") == "삭제" and del_btn.get_attribute('title') == "삭제":
                                del_btn.click()
                                break

                    sleep(1)
                    if i < len(li_list) - 2:
                        btn.click()

        chrome.execute_script(script)
        sleep(2)
        save_btn.click()
        print("빌드 옵션 설정 완료")
