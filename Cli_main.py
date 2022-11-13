from src.Scanner import Scanner as scan
from src.exploit import make_query_exploit as exploit
from pprint import pprint
from src.build_option_handler import build_option
from selenium import webdriver
from src.func import *
from selenium.webdriver.chrome.options import Options
from pprint import pprint

kitri = """
 **   ** **   **          **   ******            ******  
/**  ** //   /**         //   /*////**          /*////** 
/** **   ** ****** ****** **  /*   /**   ****** /*   /** 
/****   /**///**/ //**//*/**  /******   **////**/******  
/**/**  /**  /**   /** / /**  /*//// **/**   /**/*//// **
/**//** /**  /**   /**   /**  /*    /**/**   /**/*    /**
/** //**/**  //** /***   /**  /******* //****** /******* 
//   // //    //  ///    //   ///////   //////  ///////  


  **////**  **////**  /*////**                      /**                    
 **    //  **    //   /*   /**   ******  ********** /**       *****  ******
/**       /**         /******   **////**//**//**//**/******  **///**//**//*
/**       /**         /*//// **/**   /** /** /** /**/**///**/******* /** / 
//**    **//**    **  /*    /**/**   /** /** /** /**/**  /**/**////  /**   
 //******  //******   /******* //******  *** /** /**/****** //******/***   
  //////    //////    ///////   //////  ///  //  // /////    ////// ///    
"""


if __name__ == "__main__":
    print(kitri+"\n")
    check_method = input("Get information by\n"
                         "1. Get info from file (info.txt가 있어야함)\n"
                         "2. User info input\n"
                         "Input Number : ")

    #기본 정보 설정하기
    if check_method =="1":
        check_file = check_file_exist("info.txt")
        if check_file == False:
            print("File doesn't exsist!!")
            exit(-1)

        with open("./info.txt", "r") as info:
            info_data = info.readlines()
            for i in range(len(info_data)):
                info_data[i] = info_data[i].strip()

            url, port, vm_num, id, pw, job_name = info_data
            pprint(info_data)

    elif check_method == "2":

        while True:
            try:
                url, port = map(str, input("input url, port Like 192.168.139.128,8080\nInput = ").split(','))
                break
            except:
                print("형식에 맞춰서 넣어주세요 EX) Input=192.168.139.128,8080")

        while True:
            try:
                id, pw = map(str, input("input id, pw Like root,toor\nInput = ").split(','))
                break
            except:
                print("형식에 맞춰서 넣어주세요 Ex) Input = root,toor")
        # 환경구성을 vm에 분할하여서 vm번호로 csv 파일에 생성예장
        while True:
            try:
                vm_num,job_name = map(str, input("VM 번호, Job name을 입력해 주세요 ex)3-1,test1 \nInput = ").split(','))
                break
            except:
                print("형식에 맞춰서 넣어주세요 Ex) Input = 3-1,test1")

    else:
        exit(0)

    agent = get_user_agent_info()

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('window-size=1920x1080')
    options.add_argument(f"user-agent={agent}")

    try:
        print("Get Chrome browser.....")
        chrome = webdriver.Chrome(check_driver(),options=options)
        print("Chrome browser is ready")
    except Exception as e:
        print(f"!Error : {e}")

    #유저가 원하는 동작 시작
    while True:
        tool_option = int(input("1. Scanner\n"
                                "2. Exploit\n"
                                "3. add_build_options\n"
                                "4. exit\n"
                                "Number = "))

        if tool_option ==1:
            s = scan(chrome,url, port,id,pw,vm_num)
            S_options = int(input("1.Get all parameter\n"
                                  "2.Get response\n"
                                  "3.Get post_parameter\n"
                                  "Number = "))

            if S_options==1:
                s.get_all_param()
            elif S_options==2:
                s.get_response()
            elif S_options==3:
                s.get_post_param()
            else:
                print("Closing......")
                break

        elif tool_option == 2:
            e = exploit(chrome,url,port,vm_num,id,pw,job_name)
            E_options = int(input("1. CSRF protection check\n"
                                  "2. Reflected xss check\n"
                                  "3. Stored xss check\n"
                                  "4. XXE Check\n"
                                  "Number = "))

            if E_options==1:
                e.csrf_protection_check()
            elif E_options==2:
                e.reflected_xss_check()
            elif E_options==3:
                print("준비중")
            elif E_options==4:
                e.xxe_vlun_check()
            else:
                print("Closing......")
                break

        elif tool_option == 3:
            b_options = build_option(chrome,url,port,id,pw,job_name)
            B_options = int(input("1. Add build options\n"
                                  "2. Add after build\n"
                                  "3. delete all options\n"
                                  "Number = "))

            if B_options==1:
                b_options.add_build_step_all()
            elif B_options==2:
                b_options.add_option_after_build()
            elif B_options==3:
                b_options.delete_all_options()


        elif tool_option == 4:
            exit(0)





