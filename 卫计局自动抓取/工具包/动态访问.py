from selenium import webdriver
from bs4 import BeautifulSoup


def get_index_page(url):
    print("用于google浏览器动态访问首页返回数据，使用静默模式，这一步会稍微慢点")
    # 创建Chrome WebDriver实例，此路径为驱动程序的路径
    driver = webdriver("D:\基本软件\Google\Chrome\Application\chromedriver.exe")
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
    # 创建Chrome WebDriver实例，此路径为驱动程序的路径
    driver = webdriver("D:\基本软件\Google\Chrome\Application\chromedriver.exe")
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


def getIndexPage(indexUrl):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 使用google浏览器的静默模式
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(indexUrl)
    response = browser.page_source
    print(response)


get_index_page_1("https://www.baidu.com")