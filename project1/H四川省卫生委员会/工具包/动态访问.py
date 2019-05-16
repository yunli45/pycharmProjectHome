from selenium import webdriver
from bs4 import BeautifulSoup


def get_index_page(url):
    print("用于google浏览器动态访问首页返回数据，这一步会稍微慢点")
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 使用google浏览器的静默模式
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(url)
    response = browser.page_source
    # response = BeautifulSoup(response, 'lxml')
    # print("response" + str(response))
    return response



def get_index_page_1(url):
    print("用于google浏览器动态访问首页返回数据，这一步会稍微慢点")
    browser = webdriver.Chrome()
    browser.get(url)
    response = browser.page_source
    # response = BeautifulSoup(response, 'lxml')
    print("response" + str(response))
    return response


def get_index_page_2(url, page_no):
    print("用于google浏览器动态访问首页返回数据，这一步会稍微慢点")
    browser = webdriver.Chrome()
    if page_no==1:

        browser.get(url)
        response = browser.page_source
        # response = BeautifulSoup(response, 'lxml')
        print("response" + str(response))
    else:

        browser.get(url)
        browser.find_element_by_name('page-next').click()
        response = browser.page_source

        # response = BeautifulSoup(response, 'lxml')
    print("response" + str(response))
    return response


# get_index_page_1("http://shenyang.pbc.gov.cn/shenyfh/108074/108127/108208/3657761/2018110517581658194.xls")