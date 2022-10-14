from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
from tqdm import tqdm
#빼도됨, 나중에 오래걸릴때 혹시몰라서 넣어둠
from pprint import pprint
import user



class Resource_test:
    def __init__(self):
        csv_list = os.listdir('./csv/')
        # 파일에 있는 기존 csv데이터를 가지고 옴
        try:
            id, pw = map(str, input("Input ID,PW  ex)root,toor\nInput = ").split(','))
            self.j_id = id
            self.j_pw = pw
            self.file_name = f"./csv/Scanning_result_{self.j_id}.csv"

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
        #pprint(self.parameter_list)
        #parameter list = {'path':[], 'path2':[]}

    def check_path_trav():
        Chrome = webdriver.Chrome()
        url = f"http://{self.url}:{self.port}"
        Chrome.get(url)
        user.login(Chrome, self.j_id, self.j_pw)
        sleep(2)


        for path in self.path_list:
            url = f"http://{self.url}:{self.port}{path}"
            print(f"URL = {url}")
            Chrome.get(url)
            print("success")
            log = Chrome.get_issue_message()
            print(log)

    def check_param(self):
        Chrome = webdriver.Chrome()
        user.login(Chrome, self.j_id, self.j_pw)

R = Resource_test()
R.check_path_trav()
