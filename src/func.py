from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

def check_driver():
    print("Chrome이 업데이트 되었거나, Chrome 웹 드라이버가 존재하지 않습니다. 다운을 시작합니다.")
    ChromeDriverManager().install()
    print(" 다운이 완료되었습니다. 경로 : c:/{사용자}/.wdm/drivers/chromedriver/win32")


def login(Chrome, id,pw):
    try:
        Chrome.find_element(By.NAME, 'j_username').send_keys(id)
        Chrome.find_element(By.NAME, 'j_password').send_keys(pw)
        sleep(1)
        Chrome.find_element(By.NAME, 'Submit').click()
        print(f"유저 : {id} 비밀번호 : {pw} 로그인 성공")
        Chrome.find_element(By.ID, 'remember_me').click()
    except:
        print(f"유저 : {id} 비밀번호 : {pw} 로그인 실패")


def check_path(chrome):
    #페이지 상태 추출
    js = """
        var xhr = new XMLHttpRequest();
        xhr.open('GET', window.location.href, false);xhr.send(null);
        return xhr.status
    """
    response = chrome.execute_script(js)
    return response


def check_dir(dir_name):
    path = os.listdir("./")
    if dir_name not in path:
        try:
            os.system(f"mkdir ./{dir_name}")
        except:
            print("Your os is linux")
            os.system(f"mkdir ./{dir_name}")


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
            print("success")
            break
