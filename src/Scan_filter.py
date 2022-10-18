from selenium import webdriver
from selenium.webdriver.common.by import By



#Scanner.py에서 사용될 필터 제작

#데이터 타입에 상관 없이, 일단 input 태그 안에 존재하는 name과 type을 가져옴, iframe 안에 있는 것도 가져올 수 있게 수정했음
def get_all_param(Chrome, url, port, path,id, pw,type):

#        main_panel = Chrome.find_element(By.ID, 'main-panel')
#        input_tag = main_panel.find_elements(By.TAG_NAME, 'input')

    input_tag = Chrome.find_elements(By.TAG_NAME, 'input')

    row_result = []
    for el in input_tag:
        #데이터 포멧
        row_data = [url, port, path, id, pw, el.get_attribute("name"), el.get_attribute('type')]
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

