import pandas as pd
import os
from src.query_test import query
from src.Scanner import Scanner as scan
from src.func import check_driver

if __name__ == "__main__":
    #q = query()
    #q.print_check_list()
#    q.check_param()
    s = scan()
    s.get_all_param()
    s.result_to_csv()
