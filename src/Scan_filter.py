from selenium import webdriver
from selenium.webdriver.common.by import By


def get_all_param(Chrome, url, port, path,id, pw):
    input_tag = Chrome.find_elements(By.TAG_NAME, 'input')
    for el in input_tag:
        # if el.get_attribute("class")[0:13]=='jenkins-input':
        row_data = [url, port, path, id, pw, el.get_attribute("name"), el.get_attribute("type")]

        return row_data