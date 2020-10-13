#encoding:utf-8 
from selenium import webdriver
import time
import json



def openChrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1600x900') # 指定浏览器分辨率
    options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
    #options.add_argument('--headless') # 浏览器不提供可视化页面.linux下如果系统不支持可视化不加这条会启动失败
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=options,executable_path='./chromedriver')
    driver.set_page_load_timeout(10)
    return driver
    
def operate_dk(driver):
    url = "https://ehall.jlu.edu.cn"
    driver.get(url)
    elem = driver.find_element_by_id("username")
    elem.send_keys("zhangdx20")
    elem = driver.find_element_by_id("password")
    elem.send_keys("zdx19981006")
    try:
        driver.find_element_by_id("login-submit").click()
    except Exception,e:
        
    
    url = "https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start"
    driver.get(url)
    
    return
   

def wxpost(content):
    driver.get("https://sc.ftqq.com/SCU117990T162e5b67dea4ea8e857cb0c459aff7015f853653461bc.send?text="+content)
    print("微信打卡成功")
    
if __name__ == '__main__':
    print("这是一个自动健康打卡的程序。")
    driver = openChrome()
    operate_dk(driver)
