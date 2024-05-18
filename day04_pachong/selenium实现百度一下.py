from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

"""
通过selenium实现百度一下的点击
"""
driver ="chromedriver.exe"
# 加载chrome浏览器的驱动
service=Service(executable_path=driver)
url="https://www.baidu.com/"
# 传入参数，调用浏览器的使用
content=webdriver.Chrome(service=service)
page=content.get(url)
# print(content.page_source)
# 根据id找到对象
button=content.find_element(by=By.ID,value="su")
button_2=content.find_element(by=By.NAME,value="wd")
button_3=content.find_element(by=By.XPATH,value="//input[@id='su']")
button_4=content.find_element(by=By.PARTIAL_LINK_TEXT,value="视")
button_5=content.find_element(by=By.LINK_TEXT,value="视频")
print(button)
print(button_2)
print(button_3)
print(button_4)
print(button_5==button_4)