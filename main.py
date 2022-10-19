from src.Scanner import Scanner as scan
from src.func import check_driver

if __name__ == "__main__":
    #q = query()
    #q.print_check_list()
#    q.check_param()

    #path.txt 안에 있는 path를 전부 들어가 response를 받고 path에 존재하는 파라미터 가지고옴
    s = scan()
    s.get_all_param()
    s.result_to_csv()