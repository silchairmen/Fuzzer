from src.Scanner import Scanner as scan
from src.exploit import make_query_exploit as exploit
from pprint import pprint
from src.build_option_handler import build_option
from selenium import webdriver
from src.func import *

if __name__ == "__main__":

    kitri = """
 __  ___  __  .___________..______       __  
|  |/  / |  | |           ||   _  \     |  | 
|  '  /  |  | `---|  |----`|  |_)  |    |  | 
|    <   |  |     |  |     |      /     |  | 
|  .  \  |  |     |  |     |  |\  \----.|  | 
|__|\__\ |__|     |__|     | _| `._____||__| 
    """

    bomber = """                    
  **////**  **////**  /*////**                      /**                    
 **    //  **    //   /*   /**   ******  ********** /**       *****  ******
/**       /**         /******   **////**//**//**//**/******  **///**//**//*
/**       /**         /*//// **/**   /** /** /** /**/**///**/******* /** / 
//**    **//**    **  /*    /**/**   /** /** /** /**/**  /**/**////  /**   
 //******  //******   /******* //******  *** /** /**/****** //******/***   
  //////    //////    ///////   //////  ///  //  // ///살려    줘//// ///    
    """
    print(kitri+'\n'+bomber)
    while True:
        print("Fuzzer start Choose number\n"
              "!notice = you have to scan first before you start Fuzzing!")
        print("Number 1 = Scanner\n"
              "Number 2 = Fuzzing and extract data to csv\n"
              "Number 3 = Add all option on build")


        num = int(input("Number : "))

        if num==1:
            print("Default value input")
            s = scan()
            print("====================================================Scanner List====================================================\n")
            function_list = ["1. get_all_param", "2. get_response", "3. get_post_param" "\nIf you want finish, Input finish"]
            pprint(function_list)

            check = input("Number? : ")

            if check =='1':
                s.get_all_param()
                s.result_get_post_param_to_csv()
            elif check =='2':
                s.get_response()
                s.result_get_response_to_csv()
            elif check =='3':
                s.get_post_param()
                s.result_get_post_param_to_csv()
            elif check == "finish":
                break
            else:
                print("wrong input")

        elif num==2:
            print("====================================================Fuzzer List====================================================\n")
            function_list = ["1. XXE TEST", "2. CSRF TEST", "\nif you want finish input finish"]
            pprint(function_list)

            check = input("Number? : ")
            if check =='1':
                e = exploit()
                print("NONE")
                exit(0)
            elif check =='2':
                e = exploit()
                e.csrf_protection_check()
                e.csrf_protection_check_to_csv()
                exit(0)
            elif check == "finish":
                break
            else:
                print("wrong input")

        elif num==3:
            chrome = webdriver.Chrome(check_driver())
            url = "192.168.139.128"
            port = "8080"
            id,pw = "admin", "admin"
            jobname = "test1"
            build_option = build_option(chrome,url,port,id,pw,jobname)
            build_option.delete_all_options()
            break

        else:
            print("only number")

