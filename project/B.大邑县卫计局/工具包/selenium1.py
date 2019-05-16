from selenium import webdriver
import os
from bs4 import BeautifulSoup
"""
打开的两种方式：
1、直接在程序员种指定驱动的位置，注意用“/”不是“\\"
      chromedriver = "E:/基本软件/Google/Chrome/Application/chromedriver"
      os.environ["webdriver.chrome.driver"] = chromedriver
      driver = webdriver.Chrome(chromedriver) #模拟打开浏览器
      browser.get(url) #打开网址
2、在系统环境-path-中加入驱动的位置
        path---》E:\基本软件\Google\Chrome\Application
    browser = webdriver.Chrome() #模拟打开浏览器
    browser.get(url) #打开网址
    
完整的演示:
    browser = webdriver.Chrome() #模拟打开浏览器
    browser.get("http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml") #打开网址
    txt = browser.page_source  # 获取浏览器访问的数据，直接返回的是一个文本值，使用BeautifulSoup和正则来提取所需的数据
    soup = BeautifulSoup(txt,'lxml')
    soup = soup.find_all('div',attrs={'class':'footer_con_t'})
    print(soup)
    browser.maximize_window() #窗口最大化（无关紧要哈）
    browser.quit()

    
    
"""
"""
获取和删除cookies
    browser = webdriver.Chrome()
    browser.get('http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml')
    print(browser.get_cookies())
    #browser.delete_all_cookies() # 删除
    # browser.add_cookie({'name': '', 'domain': '', 'value': ''}) # 添加cookies，这三个值是必须的，如果在获取cookie后发现其他的值，按照上面的格式添加就好了，多跑几次，有时候出现问题
    #print(browser.get_cookies()) #获取删除后的cookies，是一个空的数组
    browser.quit()

"""
"""
在python程序中手动添加cookies
1、先使用selenium测试出期网址的cookie格式和值
   
    browser = webdriver.Chrome()
    browser.get('http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml')
    print(browser.get_cookies())
    browser.quit()
    
    # [{'domain': 'www.nhfpc.gov.cn', 'expiry': 1539256354.639384, 'httpOnly': False, 'name': 'banggoo.nuva.cookie', 'path': '/', 'secure': False, 'value': '1|W7601|W7601'}]
    # 
from fake_useragent import UserAgent 
    header = {"User-Agent": UserAgent().random}
    cookies = requests.cookies.RequestsCookieJar()
    # 不加cookie会返回202状态吗，
    cookies.set(name='banggoo.nuva.cookie', value='1|W71xc|W71xb', path='/', domain='www.nhfpc.gov.cn')

"""

"""
静默模式（在后台打开浏览器）
    1、 使用phantomjs，参考文章：http://www.cnblogs.com/nbkhic/p/4217714.html
from selenium import webdriver
    browser = webdriver.PhantomJS('phantomjs')
    browser.get('http://www.nhfpc.gov.cn/bgt/zcwj2/new_zcwj.shtml')
    txt = browser.page_source
    # print(txt)
    soup = BeautifulSoup(txt,'lxml')
    soup = soup.find_all('div',attrs={'class':'footer_con_t'})
    print(soup)
    browser.maximize_window() #窗口最大化（无关紧要哈）
    browser.quit()

    2、Chrome浏览器也是可以实现静默模式（其他的没试过）
from selenium import webdriver

    option = webdriver.ChromeOptions()
    option.add_argument('headless')  # 静默模式
    # 打开chrome浏览器
    browser = webdriver.Chrome( chrome_options=option)
    browser.get("http://www.nhfpc.gov.cn/bgt/zcwj2/new_zcwj.shtml")
    txt = browser.page_source
    # print(txt)
    soup = BeautifulSoup(txt,'lxml')
    soup = soup.find_all('div',attrs={'class':'footer_con_t'})
    print(soup)
"""




from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument('headless')  # 静默模式
# 打开chrome浏览器
browser = webdriver.Chrome( chrome_options=option)
browser.get("http://www.nhfpc.gov.cn/caiwusi/zcwj2/new_zcwj.shtml")
txt = browser.page_source
print(txt)
soup = BeautifulSoup(txt,'lxml')
soup = soup.find_all('div',attrs={'class':'pagination_index_last'})
print(soup)

