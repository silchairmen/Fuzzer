#Scanner for Fuzzer
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from tqdm import tqdm #빼도됨, 나중에 오래걸릴때 혹시몰라서 넣어둠
from src.func import login, check_dir, check_csv_file,check_driver
import src.Scan_filter as filter

class Scanner:
    def __init__(self):

        #해당 디렉터리에서 path.txt를 읽어와서 Path를 List 형태로 저장
        try:
            path_file = []
            file_list = os.listdir()
            for file in file_list:
                if '.txt' in file:
                    path_file.append(file)

            print("Text file list : "+str(path_file))

            path_txt = input("읽어들일 path파일을 입력해 주세요\nPath : ")
            with open(path_txt,"r") as f:
                #self.path = []
                self.path = f.readlines()
        except Exception as e:
            print(f"PATH file을 읽어올 수 없습니다 해당 경로에 path.txt 파일이 있는지 확인해 주세요\nError : {e}")
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
        self.post_data = []
        self.data_type = "text"
        self.vm_num = vm_num

        #Chrome 실행
        #먼저 chrome driver이 폴더에 있으면 그거 사용
        if "chromedriver.exe" in os.listdir():
            try:
                self.chrome = webdriver.Chrome()
            except:
                print("Chrome driver error, Check version or file is ok")

        #chrome 실행
        #추후에 없으면 다운로드해서 사용
        try:
            self.chrome = webdriver.Chrome(check_driver())
            print("chrome driver이 설치되었습니다")
        except:
            print("chrome 드라이버가 설치되지 않았습니다. 인터넷을 확인해 주세요")

        #ID/PW 확인 후 테스팅 시작
        self.chrome.get(f"http://{url}:{port}")
        sleep(2)
        try:
            login(self.chrome,id,pw,"first_login")
            print("Log in success")
        except:
            print("Log in fail")
            exit(-1)

    #파라미터를 전부 가져옴 (form 태그를 통하여 전송되는 데이터)
    def get_all_param(self):
        print("############################################Get ALL parameter scan##############################################")
        #path.txt에서 path 설정 후 수집 시작
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            print(payload+"\n")
            sleep(1)
            try:
                self.chrome.get(payload)
                login(self.chrome,self.j_id,self.j_pw)
            except:
                print("Connection fail, time out error")

            try:
                #input 태그로 모든 파라미터 긁어옴
                row_data = filter.get_all_param(self.chrome, self.url, self.port, self.path[i], self.j_id, self.j_pw, self.data_type)
                self.result_Frame += row_data

            except:
                print("too long runtime")

    #PATH 경로를 전부다 들어가서 response code를 가져옴
    def get_response(self):
        print("############################################Get Response##############################################")
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            print(payload+"\n")
            try:
                #뭔진 모르겠는데 갑자기 세션이 끊겨서 로그인 창으로 이동할 떄가 있음, 그래서 재로그인 해줘야함
                self.chrome.get(payload)
                sleep(1)
                login(self.chrome,self.j_id,self.j_pw)
            except:
                print("Connection fail, time out error")

            #PATH에 id로 접근 후, javascript를 통한 respones 값 받아옴, wired_selenium으로도 가능하긴 한데 그럼 소스코드 전체를 수정해야해서 좀 그럼
            try:
                status_response = filter.check_path(self.chrome)
                ACL_PATH = [self.url, self.port, self.path[i], self.j_id, status_response]
                self.result_ACL_PATH.append(ACL_PATH)
            except:
                print("too long runtime")

    def get_post_param(self):
        print("############################################Get Post form parameter scan##############################################")
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            print(payload+"\n")
            try:
            #뭔진 모르겠는데 갑자기 세션이 끊겨서 로그인 창으로 이동할 떄가 있음, 그래서 재로그인 해줘야함
                self.chrome.get(payload)
                sleep(1)
                login(self.chrome,self.j_id,self.j_pw)
            except:
                print("로그인이 유지되는중")

            try:
                row_data = filter.get_post_input(self.chrome, self.url, self.port, self.path[i],self.j_id, self.j_pw)
                self.post_data += row_data
            except:
                print("too long runtime or Directory dosen't exist")


    def result_all_param_to_csv(self):
        # 컬럼(세로 값)
        Param_col = ['URL', 'Port', 'Path', 'Jenkins_id', 'jenkins.pw', 'Parameter', 'Data_type', 'Class name']
        DataFrame = pd.DataFrame(self.result_Frame, columns=Param_col)

        # 파일이 있는지 확인하고, 있으면 덮어씌움, 참고로 파일은 Scanning_result_유저이름.csv임
        check_dir("csv")

        result_file = f"Scanning_result_vm{self.vm_num}_{self.j_id}.csv"
        file_list = os.listdir("./csv/")

        check_csv_file(DataFrame, result_file, file_list)


    def result_get_response_to_csv(self):
        # 컬럼(세로 값)
        ACL_PATH_col = ['URL', 'Port', 'Path', 'Jenkins_id', 'Response']
        DataFrame = pd.DataFrame(self.result_ACL_PATH, columns=ACL_PATH_col)

        # 파일이 있는지 확인하고, 있으면 덮어씌움, 참고로 파일은 Scanning_result_유저이름.csv임
        check_dir("csv")
        result_file = f"Check_Path_vm{self.vm_num}_{self.j_id}.csv"
        file_list = os.listdir("./csv/")

        check_csv_file(DataFrame, result_file, file_list)


    def result_get_post_param_to_csv(self):
        # 컬럼(세로 값)
        post_data_col = ['URL', 'Port', 'Jenkins_id', 'Jenkins_pw', 'Path', 'Action', 'Value', 'Value_type']
        DataFrame = pd.DataFrame(self.post_data, columns=post_data_col)
        # 파일이 있는지 확인하고, 있으면 덮어씌움, 참고로 파일은 Scanning_result_유저이름.csv임
        check_dir("csv")

        result_file = f"post_value_check_vm{self.vm_num}_{self.j_id}.csv"
        file_list = os.listdir("./csv/")

        check_csv_file(DataFrame, result_file, file_list)

    def close_Chrome(self):
        print("Chrome을 종료합니다.")
        self.chrome.close()