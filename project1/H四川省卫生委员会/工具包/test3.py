# python3.4+selenium3.5+chrome版本 63.0.3239.132+chrome驱动chromedriver.exe
# 实现自动登录百度
from selenium import webdriver
from time import sleep

# 新建webdriver对象
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://passport.baidu.com/v2/?login')
sleep(2)
driver.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
driver.find_element_by_name("userName").clear()
driver.find_element_by_name("userName").send_keys('YUNLI44')
driver.find_element_by_name("password").clear()
driver.find_element_by_name("password").send_keys('WLWAN520WS...')
driver.find_element_by_id("TANGRAM__PSP_3__submit").click()