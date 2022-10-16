from selenium import webdriver
from selenium.webdriver.common.by import By


def get_all_param(Chrome, url, port, path,id, pw,type):

#        main_panel = Chrome.find_element(By.ID, 'main-panel')
#        input_tag = main_panel.find_elements(By.TAG_NAME, 'input')

    input_tag = Chrome.find_elements(By.TAG_NAME, 'input')

    row_result = []
    for el in input_tag:
        # if el.get_attribute("class")[0:13]=='jenkins-input':
        row_data = [url, port, path, id, pw, el.get_attribute("name"), el.get_attribute('type')]
        row_result.append(row_data)



    #iframe이 존재할경우 frame을 옮겨서 조사해 주어야함
    iframe = Chrome.find_elements(By.TAG_NAME, 'iframe')

    for frame in iframe:
        Chrome.switch_to.frame(frame)
        input_tag = Chrome.find_elements(By.TAG_NAME, 'input')

        for el in input_tag:
            # if el.get_attribute("class")[0:13]=='jenkins-input':
            row_data = [url, port, path, id, pw, el.get_attribute("name"), "iframe_"+el.get_attribute('type')]
            print("iframe 값이 존재합니다.===================================\n,",row_data)
            row_result.append(row_data)

        Chrome.switch_to.default_content()

    return row_result

