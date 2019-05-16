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


def getIndexPage(indexUrl):
    # print("用于google浏览器动态访问首页返回数据，这一步会稍微慢点")
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')  # 使用google浏览器的静默模式
    # browser = webdriver.Chrome(chrome_options=option)
    # browser.get(indexUrl)
    # response = browser.page_source

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 使用google浏览器的静默模式
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(indexUrl)
    response = browser.page_source
    print(response)
    # response = BeautifulSoup(response, 'lxml')
    # print("response" + str(response))
    # pageSoup = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageNumS})
    # pageSRs = re.findall(r'<a href="index_(.?).shtml" target="_self">尾页</a>', str(pageSoup))
    # pageS1 = pageSRs[0]
    # pageS1 = int(pageS1)
    # # 每条数据
    # pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
    # RSList = re.findall(re.compile(self.compilePageTable), str(pageSoup1))
    # print(RSList)
    # print("这一页一共有：" + str(len(RSList)) + "条数据")
    #
    # return pageS1, RSList

# getIndexPage("http://www.xinyongxy.com/index.php?m=content&c=index&a=lists&catid=253&page=1")