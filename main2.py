from src.Scanner import Scanner as scan
from src.exploit import make_query_exploit as exploit
from pprint import pprint
from src.build_option_handler import build_option
from selenium import webdriver
from src.func import *
from tkinter import *

cc_bomber = """
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
# url, port, id, pw를 입력받아서 전역변수에 저장
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
# 환경구성을 vm에 분할하여서 vm번호로 csv 파일에 생성예장
while True:
    vm_num = int(input("VM 번호를 입력해 주세요 숫자만! ex)3-1 \nInput = "))
    if len(vm_num)>4:
        print("숫자만 입력해주세요.")
    else:
        break


if __name__ == "__main__":
    screen = Tk()
    screen.title("Jenkins Fuzzer")
    screen.geometry("1530x860")
    screen.mainloop()


