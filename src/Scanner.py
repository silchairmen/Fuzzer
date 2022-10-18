#Scanner for Fuzzer
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from tqdm import tqdm #빼도됨, 나중에 오래걸릴때 혹시몰라서 넣어둠
from src.func import login, check_path, check_dir, check_csv_file,check_driver
from src.Scan_filter import *

class Scanner:
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
        #환경구성을 vm에 분할하여서 vm번호로 csv 파일에 생성예장
        while True:
            vm_num = int(input("VM 번호를 입력해 주세요 숫자만!\nInput = "))
            if type(vm_num)!=int:
                print("숫자만 입력해주세요.")
            else:
                break

        self.url = url
        self.port = port
        self.j_id = id
        self.j_pw = pw
        self.parameter = []
        self.result_Frame=[] #이중 배열로 만들어질 예정, [[url,port.....],[url,port.....]] 이런식으로 Frame에 요소로 배열을 전달해서 한줄씩 추가함
        self.result_ACL_PATH = []
        self.data_type = "text"
        self.vm_num = vm_num
        #@todo 데이터 타입에 뭘 넣어서 테스트 해야할 수 있을지 생각해 봐야함(type이 text여도 url형식인게 있음)


    #파라미터를 전부 가져옴 (form 태그를 통하여 전송되는 데이터)
    def get_all_param(self):
        #초기 로그인
        try:
            Chrome = webdriver.Chrome()

        except:
            check_driver()

        #접근할 url 설정
        try:
            url = f"http://{self.url}:{self.port}"
            Chrome.get(url)
        except:
            print("login fail")

        #path.txt에서 path 설정 후 수집 시작
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            print(payload)
            sleep(1)
            try:
                Chrome.get(payload)
                login(Chrome,self.j_id,self.j_pw)
            except:
                print("Connection fail, time out error")

            #PATH에 id로 접근 후, javascript를 통한 respones 값 받아옴, wired_selenium으로도 가능하지만 현재 코드 수정할 시간이 없어서 일단락
            try:
                status_response = check_path(Chrome)
                ACL_PATH = [self.url, self.port, self.path[i], self.j_id, status_response]
                self.result_ACL_PATH.append(ACL_PATH)
                row_data = get_all_param(Chrome, self.url, self.port, self.path[i], self.j_id, self.j_pw, self.data_type)
                self.result_Frame += row_data

            except:
                print("too long runtime")
            #input tag가 존재하는 곳에서의 모든 name을 가져옴으로 서 기본 입력 파라미터 조사 가


    def result_to_csv(self):
        #컬럼(세로 값)
        Param_col = ['URL','Port','Path','Jenkins_id','jenkins.pw','Parameter','Data_type']
        DataFrame = pd.DataFrame(self.result_Frame, columns=Param_col)

        ACL_PATH_col = ['URL','Port','Path','Jenkins_id','Response']
        DataFrame2 = pd.DataFrame(self.result_ACL_PATH, columns=ACL_PATH_col)

        #파일이 있는지 확인하고, 있으면 덮어씌움, 참고로 파일은 Scanning_result_유저이름.csv임
        check_dir("csv")

        result_file = f"Scanning_result_vm{self.vm_num}_{self.j_id}.csv"
        result_file2 = f"Check_Path_vm{self.vm_num}_{self.j_id}.csv"

        file_list = os.listdir("./csv/")

        check_csv_file(DataFrame, result_file,file_list)
        check_csv_file(DataFrame2, result_file2, file_list)
