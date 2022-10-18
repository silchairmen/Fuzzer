from src.func import *
from pprint import pprint
import pandas as pd


class query:
    def __init__(self):
        csv_list = os.listdir('./csv/')
        # 파일에 있는 기존 csv데이터를 가지고 옴
        try:
            id ,pw = 'root','toor' #default
            id, pw = map(str, input("Input ID,PW  ex)root,toor\nInput = ").split(','))
            self.vm_num = int(input("input the vm number(only number!!!! ex) 1 )\ninput = "))
            self.j_id = id
            self.j_pw = pw
            self.file_name = f"Scanning_result_vm{self.vm_num}_{self.j_id}.csv"

            csv_data = pd.read_csv(self.file_name)
        except:
            if id not in csv_list:
                print("해당 유저로 생성된 파일이 없음")
                exit(0)
            else:
                print("파일 열기에 실패했습니다.")
                exit(-1)

        # 여기서 부터 본격 적인 가용 데이터 제작
        # path에 따른 파라미터 나눠야함 정확히는 payload?
        get_url = csv_data['URL'].to_list()
        self.url = get_url[0]
        get_port = csv_data['Port'].to_list()
        self.port = get_port[0]

        get_Path_list = csv_data['Path'].to_list()
        self.path_list = []
        self.parameter_list = {}
        for i in range(len(get_Path_list)):
            self.path_list.append(get_Path_list[i])

        #path list = ['/manage','/help',.....]

        self.path_list = list(set(self.path_list))
        print("self.path_list")
        for i in range(len(self.path_list)):
            self.parameter_list[self.path_list[i]] = csv_data[csv_data['Path'] == self.path_list[i]]['Parameter'].to_list()
        #parameter_list = {'path':[], 'path2':[]}

    #만약 자신이 테스트할 path와 path에서 보낼 수 있는 파라미터를 확인해보고 싶다면 사용
    def print_check_list(self):
        print("===============================PATH=======================================")
        pprint(self.path_list)
        print("============================PATH : Param==================================")
        pprint(self.parameter_list)

    #여기서 부터 퍼져 만들기, 정확히는 테스트 스크립트
    def check_param(self):
        Chrome = webdriver.Chrome()
        Chrome.get(f"http://{self.url}:{self.port}")
        login(Chrome, self.j_id, self.j_pw)

