#Scanner for Fuzzer
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from tqdm import tqdm #빼도됨, 나중에 오래걸릴때 혹시몰라서 넣어둠
from user import login, check_path, check_dir, check_csv_file
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Scanner:
    #처음에 실행 되고, value 값 초기화
    def __init__(self):

        #해당 디렉터리에서 path.txt를 읽어와서 Path를 List 형태로 저장
        try:
            with open("./path.txt") as f:
                self.path = f.readlines()
        except:
            print("PATH file을 읽어올 수 없습니다 해당 경로에 path.txt 파일이 있는지 확인해 주세요")
            exit(-1)

        #url, port, id, pw를 입력받아서 전역변수에 저장
        while True:
            try:
                url, port = map(str, input("input url, port Like www.naver.com,8080\nInput = ").split(','))
                break
            except:
                print("형식에 맞춰서 넣어주세요 EX) Input=www.jenkins.com,8080")

        while True:
            try:
                id, pw = map(str, input("input id, pw Like root,toor\nInput = ").split(','))
                break
            except:
                print("형식에 맞춰서 넣어주세요 Ex) Input = root,toor")

        self.url = url
        self.port = port
        self.j_id = id
        self.j_pw = pw
        self.parameter = []
        self.result_Frame = [] #이중 배열로 만들어질 예정, [[url,port.....],[url,port.....]] 이런식으로 Frame에 요소로 배열을 전달해서 한줄씩 추가함
        self.result_ACL_PATH = []
        self.data_type = "text"
        #@todo 데이터 타입에 뭘 넣어서 테스트 해야할 수 있을지 생각해 봐야함(type이 text여도 url형식인게 있음)

    #Directory Path 별로 input 태그가 들어간 곳에 name을 가져옴
    def get_all_param(self):
        #초기 로그인
        Chrome = webdriver.Chrome()
        url = f"http://{self.url}:{self.port}"
        Chrome.get(url)
        login(Chrome, self.j_id, self.j_pw)

        #path.txt에서 path 하나 잡고 Payload 작성
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            print(payload)
            sleep(1)
            Chrome.get(payload)

            #PATH에 접근 가능한지 확인
            status_response = check_path(Chrome)
            ACL_PATH = [self.url, self.port, self.path[i], self.j_id, status_response]
            self.result_ACL_PATH.append(ACL_PATH)

            #가져올 태그를 선택하면 됨 Form, input 등등이긴한데, 입력 가능한 value 넣을라면 input이 좋을 것 같아서 input으로 짬
            input_tag = Chrome.find_elements(By.TAG_NAME, 'input')

            #input 태그 중에서 특성중에 class가 jenkins-input으로 시작하는 곳을 찾아서 name 값 가져오기
            for el in input_tag:
                #if el.get_attribute("class")[0:13]=='jenkins-input':
                row_data = [self.url, self.port, self.path[i], self.j_id, self.j_pw, el.get_attribute("name"), self.data_type]
                self.result_Frame.append(row_data)
                    #@todo 여기 필터링 어떤식으로 만들지 정해야함

        Chrome.close()

    # 이중배열에 원소로 배열을 넣어줬으니 만들어진 배열을 DataFrame 형식으로 만들어서 csv로 출력함 출력할 원소 수정하려면 70번째줄이랑 같이 수정해야함
    def result_to_csv(self):
        #컬럼(세로 값)
        Param_col = ['URL','Port','Path','Jenkins_id','jenkins.pw','Parameter','Data_type']
        DataFrame = pd.DataFrame(self.result_Frame, columns=Param_col)

        ACL_PATH_col = ['URL','Port','Path','Jenkins_id','Response']
        DataFrame2 = pd.DataFrame(self.result_ACL_PATH, columns=ACL_PATH_col)

        #파일이 있는지 확인하고, 있으면 덮어씌움, 참고로 파일은 Scanning_result_유저이름.csv임
        check_dir("csv", "./")

        result_file = f"Scanning_result_{self.j_id}.csv"
        result_file2 = f"Check_Path_{self.j_id}.csv"

        file_list = os.listdir("./csv/")

        check_csv_file(DataFrame, result_file,file_list)
        check_csv_file(DataFrame2, result_file2, file_list)

#클래스 선언하고 함수 실행시킴, 이것마저도 안에 넣고싶으면 넣으면 되긴하는데 개인적으로 이건 빼두는게 낫지 않을까 싶어요 ㅎㅎ;
Scanner = Scanner()
Scanner.get_all_param()
Scanner.result_to_csv()