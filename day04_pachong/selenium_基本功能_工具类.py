from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time


class SeleniumTool:
    def __init__(self, driver_path: str, headless: bool = False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        self.service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)

    def open_url(self, url: str):
        self.driver.get(url)

    def click(self, by: By, value: str):
        element = self.driver.find_element(by, value)
        element.click()

    def input_text(self, by: By, value: str, text: str):
        element = self.driver.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_by(self, x: int, y: int):
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    def get_page_source(self) -> str:
        return self.driver.page_source

    def quit(self):
        self.driver.quit()


# 示例使用
if __name__ == "__main__":
    # 设置 chromedriver 的路径
    driver_path = r"E:\\py_workstation\\py_start\\New_Py_learn\\day04_pachong\\chromedriver.exe"

    # 创建 SeleniumTool 实例
    selenium_tool = SeleniumTool(driver_path, headless=False)

    # 打开 URL
    selenium_tool.open_url("http://www.baidu.com/")

    # 输入搜索关键词
    selenium_tool.input_text(By.NAME, "wd", "Selenium")

    # 模拟点击搜索按钮
    selenium_tool.click(By.ID, "su")

    time.sleep(2)  # 等待页面加载

    # 滚动到页面底部
    selenium_tool.scroll_to_bottom()

    time.sleep(2)  # 等待滚动

    # 滚动到页面顶部
    selenium_tool.scroll_to_top()

    time.sleep(2)  # 等待滚动

    # 获取网页源码
    page_source = selenium_tool.get_page_source()
    print(page_source[:500])  # 打印前500个字符

    # 后退
    selenium_tool.back()

    time.sleep(2)  # 等待页面加载

    # 前进
    selenium_tool.forward()

    time.sleep(2)  # 等待页面加载

    # 退出浏览器
    selenium_tool.quit()
