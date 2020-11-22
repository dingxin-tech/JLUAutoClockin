#encoding:utf-8
from selenium import webdriver
import time
import pandas as pd
import datetime

def openChrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1600x900') # 指定浏览器分辨率
    options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
    options.add_argument('--headless') # 浏览器不提供可视化页面.linux下如果系统不支持可视化不加这条会启动失败
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=options,executable_path='/chromedriver')
    driver.set_page_load_timeout(15)
    driver.implicitly_wait(20)
    return driver

def Clock_in(name,pw,zy,nj,gy,qs,SC_KEY):
    try:
        driver = openChrome()
        url = "https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start"
        driver.get(url)
        elem = driver.find_element_by_id("username")
        elem.send_keys(name)
        elem = driver.find_element_by_id("password")
        elem.send_keys(pw)
        driver.find_element_by_id("login-submit").click()
        elem = driver.find_element_by_id("V1_CTRL40")
        elem.clear()
        elem.send_keys(zy.decode("utf-8"))  #专业
        elem = driver.find_element_by_id("V1_CTRL41")
        elem.send_keys(nj) #年级
        elem = driver.find_element_by_id("V1_CTRL42")
        elem.send_keys(u"中心校区") #校区
        elem = driver.find_element_by_id("V1_CTRL7")
        elem.send_keys(gy.decode("utf-8")) #公寓
        elem = driver.find_element_by_id("V1_CTRL8")
        elem.clear()
        elem.send_keys(qs) #寝室
        driver.find_element_by_id("V1_CTRL44").click() #硕士
        driver.find_element_by_id("V1_CTRL28").click() #打卡
        time.sleep(3)
        driver.find_element_by_class_name('command_button_content').click()  #提交
        driver.find_element_by_css_selector('.dialog_button.default.fr').click()  #是
        time.sleep(5)
        driver.find_element_by_xpath("// * / div[2] / button").click()  #是
        time.sleep(5)
        message=driver.find_element_by_xpath("// *[ @ id = \"title_content\"] / nobr").text
        if(message=='研究生每日打卡:申请填写(已完成)'.decode("utf-8") or message=="研究生每日打卡:申请填写(Completed)".decode("utf-8")):
            driver.close()
            return True
        else:
            driver.close()
            return False
    except Exception as e:
        print(e)
        driver.close()
        return False

#微信Server酱
def wxpost(content,SC_KEY):
    if(SC_KEY=="nothing"):
        return
    driver = openChrome()
    time = "@"+datetime.datetime.now().strftime('%H')+"点"+datetime.datetime.now().strftime('%M')+"分"+datetime.datetime.now().strftime('%S')+"秒"
    print("https://sc.ftqq.com/" + SC_KEY + ".send?text=" + content + time)
    driver.get("https://sc.ftqq.com/"+SC_KEY+".send?text="+content+time)
    driver.close()


if __name__ == '__main__':
    data = pd.read_csv("/document.csv")  #从.csv文件中读取信息
    print("自动打卡")
    for index, row in data.iterrows():
        name, secret = row['name'], row['secret']
        subject, years = row['subject'],row['years']
        document, doc_number = row['document'],row['doc_number']
        SC_KEY = row['SC_KEY']
        count=0
        while(not Clock_in(name,secret,subject,years,document,doc_number,SC_KEY)):
            count=count+1
            print("打卡失败")
            time.sleep(30)
            if(count==20):
                wxpost("打卡失败",SC_KEY)
                break
        if(count!=20):
            wxpost("打卡成功",SC_KEY)
    print("打卡成功")
