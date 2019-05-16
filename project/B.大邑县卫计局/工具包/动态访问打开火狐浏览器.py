from selenium import webdriver

browser =webdriver.Firefox()

browser.get("http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml")
print(browser.page_source)
browser.close()

str1 ="http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml"
print(str1[:str1.rfind(".shtml")])

