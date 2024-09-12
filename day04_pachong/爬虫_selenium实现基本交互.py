from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
"""
通过selenium实现基本的操作
# 一些常用的交互函数
# (1)点击:click()
# (2)输入：:send_keys()
# (3)后退操作:browser.back()
# (4)前进操作:browser.forward()
# (5)模拟js滚动:js="document.documentElement.scrollTop="100000""
#              browser.execute_script(js) 执行js代码
# (7)获取网页代码:page_source
# (8)退出:browser.quit()
"""
driver="chromedriver.exe"
service = Service(driver)
wb_page=webdriver.Chrome(service=service)
url="https://www.baidu.com"
wb_page.get(url)
wb_page.maximize_window()
time.sleep(10)
kw_elemment=wb_page.find_element(by=By.ID,value="kw")
kw_elemment.send_keys("朱梦珂")
print(kw_elemment)
time.sleep(5)
button=wb_page.find_element(by=By.ID,value="su")
button.click()
# 滑到底部
# 滑到页面底部是一个固定写法
# document.documentElement.scrollTop=100000
js_button='document.documentElement.scrollTop=100000'
wb_page.execute_script(js_button)
time.sleep(2)
# 获取下一页的按钮
next=wb_page.find_element(by=By.XPATH,value="//a[@class='n']")
print(next)
next.click()
time.sleep(5)
# 回到上一页
wb_page.back()
# 前进一页
wb_page.forward()
time.sleep(5)




