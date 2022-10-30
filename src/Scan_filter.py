from selenium import webdriver
from selenium.webdriver.common.by import By


#Scanner.py에서 사용될 필터 제작
#데이터 타입에 상관 없이, 일단 input 태그 안에 존재하는 name과 type을 가져옴, iframe 안에 있는 것도 가져올 수 있게 수정했음
def get_all_param(Chrome, url, port, path,id, pw,type):
    input_tag = Chrome.find_elements(By.TAG_NAME, 'input')
    row_result = []

    for el in input_tag:
        #데이터 포멧
        row_data = [url, port, path, id, pw, el.get_attribute("name"), el.get_attribute('type'), el.get_attribute('class')]
        row_result.append(row_data)

    #iframe이 존재할경우 frame을 옮겨서 조사해 주어야함
    iframe = Chrome.find_elements(By.TAG_NAME, 'iframe')

    for frame in iframe:
        Chrome.switch_to.frame(frame)
        input_tag = Chrome.find_elements(By.TAG_NAME, 'input')

        for el in input_tag:
            row_data = [url, port, path, id, pw, el.get_attribute("name"), "iframe_"+el.get_attribute('type')]
            #iframe에서 긁어온 데이터는 type에 iframe임을 명시함, iframe의 경우 파라미터 전달이 불가, iframe 내에서 수행해야함
            print("iframe 값이 존재합니다.===================================\n,",row_data)
            row_result.append(row_data)

        Chrome.switch_to.default_content()

    return row_result

def check_path(chrome):
    #페이지 상태 추출
    js = """
        var xhr = new XMLHttpRequest();
        xhr.open('GET', window.location.href, false);xhr.send(null);
        return xhr.status
    """
    response = chrome.execute_script(js)
    return response


def get_user_input_param(Chrome, url, port, path,id, pw):
    input_tag = Chrome.find_elements(By.TAG_NAME, 'input')

    row_result = []
    for el in input_tag:
        c_name = el.get_attribute('class')

#        if c_name in jenkins_input:
#        # 데이터 포멧
#         row_data = [url, port, path, id, pw, el.get_attribute("name"), el.get_attribute('type')]
#         row_result.append(row_data)

    # iframe이 존재할경우 frame을 옮겨서 조사해 주어야함
    iframe = Chrome.find_elements(By.TAG_NAME, 'iframe')

    for frame in iframe:
        Chrome.switch_to.frame(frame)
        input_tag = Chrome.find_elements(By.TAG_NAME, 'input')

        for el in input_tag:
            row_data = [url, port, path, id, pw, el.get_attribute("name"), "iframe_" + el.get_attribute('type')]
            # iframe에서 긁어온 데이터는 type에 iframe임을 명시함, iframe의 경우 파라미터 전달이 불가, iframe 내에서 수행해야함
            print("iframe 값이 존재합니다.===================================\n,", row_data)
            row_result.append(row_data)

        Chrome.switch_to.default_content()

    return row_result

def get_post_input(Chrome, url, port, path,id, pw):
    row_result = []
    all_form = Chrome.find_elements(By.TAG_NAME, 'form')
    for form in all_form:
        if form.get_attribute("method")=="post":
            action = form.get_attribute("action")
            all_button = form.find_elements(By.TAG_NAME, 'button')
            all_input = form.find_elements(By.TAG_NAME, 'input')

            for button in all_button:
                if button!="":
                    button_type = button.get_attribute("type")
                    #[url, port, id, pw, path, action, value, value_type or name]
                    #[                                 button, submit           ]
                    row_data = [url, port, id, pw, path, action, "button", button_type]
                    row_result.append(row_data)

            for input in all_input:
                #class ? name ?
                if input!="":
                    input_name = input.get_attribute("name")

                    if input_name=="":
                        input_class = input.get_attribute("class")
                        row_data = [url, port, id, pw, path, action, "input", "class :" + input_class]
                        row_result.append(row_data)
                        print(row_data)
                    #[url, port, id, pw, path, action, value, value_type or name]
                    #[                                 class, jenkins_input           ]
                    else:
                        row_data = [url, port, id, pw, path, action, "input", "name : " + input_name]
                        row_result.append(row_data)

    # iframe이 존재할경우 frame을 옮겨서 조사해 주어야함
    iframe = Chrome.find_elements(By.TAG_NAME, 'iframe')

    for frame in iframe:
        Chrome.switch_to.frame(frame)

        all_form = Chrome.find_elements(By.TAG_NAME, 'form')
        for form in all_form:
            if form.get_attribute("method") == "post":
                action = form.get_attribute("action")
                all_button = form.find_elements(By.TAG_NAME, 'button')
                all_input = form.find_elements(By.TAG_NAME, 'input')

                for button in all_button:
                    if button!="":
                        button_type = button.get_attribute("type")
                        # [url, port, id, pw, path, action, value, value_type or name]
                        # [                                 button, submit           ]
                        row_data = [url, port, id, pw, path+"_iframe", action, "button", button_type]
                        row_result.append(row_data)

                for input in all_input:
                    # class ? name ?
                    if input!="":
                        input_name = input.get_attribute("class")
                        row_data = [url, port, id, pw, path+"_iframe", action, "class", input_name]
                        row_result.append(row_data)

        #원래의 frame으로 돌아옴
        Chrome.switch_to.default_content()
        return row_result
