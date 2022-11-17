#Scanner for Fuzzer
from time import sleep
import os
from tqdm import tqdm #빼도됨, 나중에 오래걸릴때 혹시몰라서 넣어둠
from src.func import login, make_csv_file,check_dir
import src.Scan_filter as filter

class Scanner:
    def __init__(self,chrome, url, port, id, pw, vm_num):
        #해당 디렉터리에서 path.txt를 읽어와서 Path를 List 형태로 저장
        try:
            check_dir('path')
            path_txt = f"./path/path_vm{vm_num}.txt"

            with open(path_txt,"r") as f:
                self.path = f.readlines()
            print(f"Path file = {path_txt}")
        except Exception as e:
            print(f"PATH file을 읽어올 수 없습니다 해당 경로에 path.txt 파일이 있는지 확인해 주세요\nError : {e}")
            exit(-1)

        self.chrome = chrome
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
        #path.txt에서 path 설정 후 수집 시작
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            sleep(1)
            try:
                self.chrome.get(payload)
            except:
                login(self.chrome, self.j_id, self.j_pw)
                print("Connection fail, time out error")

            try:
                print(f"Get all parameter *PATH : {self.path[i]}....")
                #input 태그로 모든 파라미터 긁어옴
                row_data = filter.get_all_param(self.chrome, self.url, self.port, self.path[i], self.j_id, self.j_pw)
                self.result_Frame += row_data

            except:
                print("too long runtime")

        Param_col = ['URL', 'Port', 'Jenkins_id', 'jenkins.pw', 'Method', 'Path','Action', 'Parameter', 'Data_type',
                     'Class name', "Value"]

        # 파일이 있는지 확인하고, 있으면 덮어씌움, 참고로 파일은 Scanning_result_유저이름.csv임

        result_file_name = f"Scanning_all_param_result_vm{self.vm_num}_{self.j_id}.csv"
        make_csv_file(Param_col, self.result_Frame, result_file_name, 'Action')

    #PATH 경로를 전부다 들어가서 response code를 가져옴
    def get_response(self):
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            print(payload+"\n")
            try:
                print(f"Get response *PATH : {self.path[i]}....")
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

        ACL_PATH_col = ['URL', 'Port', 'Path', 'Jenkins_id', 'Response']
        # 파일이 있는지 확인하고, 있으면 덮어씌움, 참고로 파일은 Scanning_result_유저이름.csv임
        result_file = f"get_response_path_vm{self.vm_num}_{self.j_id}.csv"
        make_csv_file(ACL_PATH_col, self.result_ACL_PATH, result_file)

    def get_post_param(self):
        for i in tqdm(range(len(self.path)), mininterval=0.1):
            payload = f"http://{self.url}:{self.port}{self.path[i]}"
            print(payload+"\n")
            try:
                print(f"Get post param *PATH : {self.path[i]}....")
                #뭔진 모르겠는데 갑자기 세션이 끊겨서 로그인 창으로 이동할 떄가 있음, 그래서 재로그인 해줘야함
                self.chrome.get(payload)
                sleep(1)
                login(self.chrome,self.j_id,self.j_pw)
            except:
                print(f"!Path : {self.path[i]} connection fail")

            try:
                row_data = filter.get_post_input(self.chrome, self.url, self.port, self.path[i],self.j_id, self.j_pw)
                self.post_data += row_data
            except:
                print("too long runtime or Directory dosen't exist")


        post_data_col = ['URL', 'Port', 'Jenkins_id', 'Jenkins_pw', 'Path', 'Action', 'Value', 'Value_type']
        result_file = f"post_value_check_vm{self.vm_num}_{self.j_id}.csv"
        make_csv_file(post_data_col, self.post_data, result_file)


    def close_Chrome(self):
        print("Chrome을 종료합니다.")
        self.chrome.close()