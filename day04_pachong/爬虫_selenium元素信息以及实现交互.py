import selenium.webdriver.chrome.service
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
通过selenium的基本使用，实现对响应页面实现交互
"""
driver="chromedriver.exe"
url="https://www.baidu.com"
service=selenium.webdriver.chrome.service.Service(driver)
content=webdriver.Chrome(service=service)
content.get(url)
print(content.title)
input_button=content.find_element(by=By.ID,value='su')
class_value=input_button.get_attribute("class")
tag_name=input_button.tag_name
# 访问元素信息
# 获取元素属性
# -- .get_attribute('class')
# 获取元素文本
# --.text
# 获取标签名
# -- .tag_name
print(class_value)
print(tag_name)
a=content.find_element(by=By.LINK_TEXT,value='新闻')
print(a.text)