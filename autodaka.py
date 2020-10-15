#encoding:utf-8
from selenium import webdriver
import time
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
    driver.set_page_load_timeout(10)
    return driver

def operate_dk(name,pw,zy,nj,gy,qs,msurl):
    driver = openChrome()
    url = "https://ehall.jlu.edu.cn"
    driver.get(url)
    elem = driver.find_element_by_id("username")
    elem.send_keys(name)
    elem = driver.find_element_by_id("password")
    elem.send_keys(pw)
    try:
        driver.find_element_by_id("login-submit").click()

    except Exception as e:
        print("")

    url = "https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start"
    driver.get(url)
    time.sleep(5)
    try:
        elem = driver.find_element_by_id("V1_CTRL40")
        elem.clear()
        elem.send_keys(zy)  #专业
        elem = driver.find_element_by_id("V1_CTRL41")
        elem.send_keys(nj) #年级
        elem = driver.find_element_by_id("V1_CTRL42")
        elem.send_keys(u"中心校区") #校区
        elem = driver.find_element_by_id("V1_CTRL7")
        elem.send_keys(gy) #公寓
        elem = driver.find_element_by_id("V1_CTRL8")
        elem.clear()
        elem.send_keys(qs) #寝室
        driver.find_element_by_id("V1_CTRL44").click() #硕士
        driver.find_element_by_id("V1_CTRL28").click() #早打卡
    except Exception as e:
        wxpost("于错误的时间，打卡失败！", msurl)
        driver.close()
        return
    try:
        driver.find_element_by_id("V1_CTRL19").click() #午打卡
        driver.find_element_by_id("V1_CTRL23").click() #晚打卡
    except Exception as e:
        pass
    try:
        driver.find_element_by_class_name('command_button_content').click()
        time.sleep(5)
        driver.find_element_by_css_selector('.dialog_button.default.fr').click()
        time.sleep(5)
        wxpost("打卡成功！",msurl)
    except Exception as e:
        wxpost("打卡失败！", msurl)
    driver.close()
    time.sleep(5)
    return

#微信Server酱
def wxpost(content,msurl):
    if(msurl=="null"):
        return
    driver = openChrome()
    time = datetime.datetime.now().strftime('%H')+"时"+datetime.datetime.now().strftime('%M')+"分"+datetime.datetime.now().strftime('%S')+"秒"
    driver.get(msurl+content+time)


if __name__ == '__main__':
    print("自动打卡")
    operate_dk("zhangdx20", "zdx19981006",u"电子信息","2020",u"文苑六公寓","417",
               "https://sc.ftqq.com/SCU117990T162e5b67dea4ea8e857cb0c459aff7015f853653461bc.send?text=")
    operate_dk("yangmq19", "520yangmingqi", u"计算机技术", "2020", u"南苑7公寓", "352",
               "https://sc.ftqq.com/SCU117990T162e5b67dea4ea8e857cb0c459aff7015f853653461bc.send?text=")
    operate_dk("chenxd19", "cx295440", u"软件工程", "2019", u"南苑8公寓", "649",
               "https://sc.ftqq.com/SCU118277T8c8cee25dbd9587e9f720ce0bf22b8695f87a5e2b3573.send?text=")
    operate_dk("tyzhang19", "zty146112", u"计算机技术", "2019", u"南苑8公寓", "535-1",
               "https://sc.ftqq.com/SCU118278T0292bd80e057a7f3b58bb67f2b259f905f87a8192c510.send?text=")
    operate_dk("wangtao20", "243613492wt", u"电子信息", "2020", u"文苑六公寓", "417",
               "https://sc.ftqq.com/SCU118073T820da58ecb224bd24232663e608e7d995f85b1b9ce517.send?text=")
    operate_dk("sunxh20", "302614aaaa", u"电子信息", "2020", u"文苑六公寓", "417",
               "https://sc.ftqq.com/SCU118081Tca2319e134c4b8bdbad9cafd534678d55f85b8d718d78.send?text=")
    operate_dk("lengzq20", "lengzhaoqi0409", u"电子信息", "2020", u"文苑六公寓", "417",
               "https://sc.ftqq.com/SCU118073T820da58ecb224bd24232663e608e7d995f85b1b9ce517.send?text=")
    operate_dk("hqli20", "di88254123", u"软件工程", "2020", u"文苑六公寓", "316", "null")
    print("打卡成功")