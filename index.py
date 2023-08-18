#python 3.10.12
import csv
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def openurl(url):
    driver = Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    return driver
def roomidinput(driver,str1:str):
    try:
        ele=driver.find_element(By.XPATH,'//*[@id="roomCode"]')
        ele.send_keys(str1)
        button=driver.find_element(By.XPATH,'//*[@id="container"]/div/div[2]/div/div/i')
        button.click()
        sleep(0.15)
        alert = driver.switch_to.alert
        alert.accept()
        sleep(0.05)
        ele.clear()
        sleep(0.05)
        alertflag=True
        return alertflag
    except:
        sleep(0.05)
        alertflag=False
        ele.clear()
        sleep(0.05)
        return alertflag
def getmes(driver):
    roomid=driver.find_element(By.XPATH,'//*[@id="roomId"]')
    roomname=driver.find_element(By.XPATH,'//*[@id="roomName"]')
    sydl=driver.find_element(By.XPATH,'//*[@id="sydl"]')
    syje=driver.find_element(By.XPATH,'//*[@id="syje"]')

    dic={
        'roomid':roomid.text,
        'roomname':roomname.text,
        'sydl':sydl.text,
        'syje':syje.text,
    }

    print(dic)
    with open ('message.csv','a',newline='') as file:
        fieldnames=['roomid','roomname','sydl','syje']
        writer=csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(dic)
def roomlist(strtmp):
    roomlist=[]
    for num1 in range(1,7):
        for num2 in range(0,4):
            for num3 in range(0,10):
                strroom=strtmp+str(num1)+str(num2)+str(num3)
                roomlist.append(strroom)
    return roomlist

def initcsv():
    with open('message.csv','w',newline='') as file:
        names = ['系统房间编号', '房间名', '剩余电量', '剩余金额']
        writer=csv.writer(file)
        writer.writerow(names)

if __name__ == '__main__':
    print('统计全楼各寝室电费情况（楼号规则：ABB，A代表用户类型（1=本科，2=硕士，3=博士），BB代表栋数。）')
    num3=input('请输入前三位:')
    roomlist=roomlist(str(num3))
    initcsv()

    url = 'https://wx.uestc.edu.cn/oneCartoon/index.html'
    driver=openurl(url)

    for i in roomlist:
        try:
            print(i)
            alertflag=roomidinput(driver,i)
        except:
            print('error,pass '+i+' room')
            continue
        if alertflag==False:
            try:
                getmes(driver)
            except:
                print('error getmessage')
    # input('Selenium running done.')
    driver.quit()