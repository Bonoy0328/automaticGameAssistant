import cv2
import subprocess
import time
import pytesseract
from PIL import Image
import numpy as np
import math

buildTime = 0
buildTime2 = 0
trainTime = [0,0,0,0]
studyTime = 0
seekingTime = 0
miningTime = 0
treasureTime = 0
fightTime = 0
managing = 0
pytesseract.pytesseract.tesseract_cmd = "C://Program Files/Tesseract-OCR/tesseract.exe"
#判断是否打开了进度管理页面
def isOpenWindows():
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png",0)
    subImage = image[478:523,344:512]
    for i in range(subImage.shape[0]):
        for j in range(subImage.shape[1]):
            if(subImage[i,j]<150):
                subImage[i,j] = 0
            else:
                subImage[i,j] = 255
    processOfImage = cv2.imread("process.png",0)
    imageBuf = processOfImage-subImage
    print(imageBuf.sum())
    if imageBuf.sum()<10000:
        return True
    else:
        return False
#打开或者关闭进度管理界面
def openOrClose(flag):
    whatPage = []
    index = 4
    worldPage = cv2.imread("world.png",0)
    mainPage = cv2.imread("main.png",0)
    backPage = cv2.imread("back.png",0)
    mainPage2 = cv2.imread("main2.png",0)
    while not((index==1)or(index==3)):
        while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
            True
        image = cv2.imread("buf.png",0)
        subImage = image[40:110,20:110]
        for i in range(subImage.shape[0]):
            for j in range(subImage.shape[1]):
                if(subImage[i,j]<100):
                    subImage[i,j] = 0
                else:
                    subImage[i,j] = 255
        whatPage = [(worldPage-subImage).sum(),(mainPage-subImage).sum(),(backPage-subImage).sum(),(mainPage2-subImage).sum()]
        index = whatPage.index(min(whatPage))
        if(index==0):
            subprocess.call("adb shell input tap 150 2015",shell=True) 
            time.sleep(4)
        elif(index==2):
            subprocess.call("adb shell input tap 60 75",shell=True) 
            time.sleep(2)
    if(flag=="open"):                 
        while not(isOpenWindows()):
            subprocess.call("adb shell input tap 40 1045",shell=True) 
            time.sleep(1)
    else:                     
        while (isOpenWindows()):
            subprocess.call("adb shell input tap 890 1045",shell=True) 
            time.sleep(1)
#获取图标的像素位置
def getIconIndex(icon):
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png",0)
    ret,binImage = cv2.threshold(image,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)
    iconImage = cv2.imread(icon+".png",0)
    #图标都在533:1603 30：90之间
    e = 99999999
    for i in range(533,1603-60):
        d = (iconImage - binImage[i:i+60,30:90]).sum()
        if e>d:
            e = d
            index = i
    return index
#获取图标的开启状态
def getIconState(icon):
    off = cv2.imread("off.png",0)
    on = cv2.imread("on.png",0)
    index = getIconIndex(icon)
    image = cv2.imread("buf.png",0)
    ret,binImage = cv2.threshold(image,0,255,cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)   
    if(on - binImage[index:index+60,771:821]).sum() < (off - binImage[index:index+60,771:821]).sum():
        return True
    else:
        return False
#打开或者关闭子菜单
def openOrCloseIcon(icon,flag):
    if(flag=="open"):
        while not(getIconState(icon)):
            subprocess.call("adb shell input tap 500 "+str(getIconIndex(icon)+30),shell=True) 
    else:
        while getIconState(icon):
            subprocess.call("adb shell input tap 500 "+str(getIconIndex(icon)+30),shell=True)
#获取剩余时间的函数
def getTime(image,x1,x2):
    sec = 0
    subImage = image[x1:x2,360:640]
    c = 0
    err = [0,0,-5,-10,-15,-20,-25,-30,10,20,30,40,20,60,70]
    while True:
        while not(cv2.imwrite("time.png",subImage)):
            True
        text = pytesseract.image_to_string(Image.open("time.png"),lang="eng")
        if len(text)==8 and text[2]==":" and text[5]==":":
            print(text)
            sec = (int(text[0])*10 + int(text[1]))*3600 + (int(text[3])*10 + int(text[4]))*60 + (int(text[6])*10 + int(text[7]))
            break
        else:
            print(text)
            for i in range(subImage.shape[0]):
                for j in range(subImage.shape[1]):
                    if(subImage[i,j]<100+err[c]):
                        subImage[i,j] = 0
        if c>13:
            sec = 600
            break
        else:
            c+=1
    return sec

#建筑管理的函数
def buildManager():
    global buildTime,buildTime2
    openOrClose("open")
    openOrCloseIcon("icon1","open")
    #780:800 630:650判断颜色
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png")
    image3 = cv2.imread("buf.png",0)
    subImage = image[630:650,780:800]
    subImage2 = image[720:740,780:800]
    if (subImage.sum())<140000:
        subprocess.call("adb shell input tap 800 650",shell=True)
        time.sleep(2)
        #880:900 1990:2010
        while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
            True
        image = cv2.imread("buf.png")
        subImage = image[1990:2010,880:900]
        if (subImage.sum())<140000:
            subprocess.call("adb shell input tap 900 2010",shell=True)
    if (subImage2.sum())<140000:
        subprocess.call("adb shell input tap 800 740",shell=True)
        time.sleep(2)
        #880:900 1990:2010
        while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
            True
        image = cv2.imread("buf.png")
        subImage2 = image[1990:2010,880:900]
        if (subImage2.sum())<140000:
            subprocess.call("adb shell input tap 900 2010",shell=True)
    # else:
    #     buildTime = getTime(image3,610,700)
    #     openOrCloseIcon("icon1","close")
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    buildTime = getTime(image3,610,700)
    buildTime2 = getTime(image3,690,800)
    openOrCloseIcon("icon1","close")

def trainManager():
    #四个兵种，分别对应于780   800 890 970 1060
    global trainTime
    index = [800,890,970,1060]
    d = 0
    index2 = [770,850,940,1020]
    openOrClose("open")
    openOrCloseIcon("icon2","open")
    for i in index:
        while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
            True
        image = cv2.imread("buf.png")
        image3 = cv2.imread("buf.png",0)
        subImage = image[i:i+20,780:800]   
        if(subImage.sum())<140000:
            subprocess.call("adb shell input tap 800 "+str(i+20),shell=True)
            time.sleep(2)
            #880:900 1990:2010
            while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
                True
            image = cv2.imread("buf.png")
            subImage = image[1990:2010,880:900]
            if (subImage.sum())<140000:
                subprocess.call("adb shell input tap 900 2010",shell=True)
                time.sleep(2)
                subprocess.call("adb shell input tap 55 80",shell=True)
            openOrClose("open")
            time.sleep(2)
            while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
                True
            image3 = cv2.imread("buf.png",0)
            trainTime[d] = getTime(image3,index2[d],index2[d]+100)
        else:
            print(subImage.sum())
            trainTime[d] = getTime(image3,index2[d],index2[d]+100)
        d+=1
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    openOrCloseIcon("icon2","close")

def studyManager():
    # index = 900
    global studyTime
    openOrClose("open")
    openOrCloseIcon("icon3","open")
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png")
    image3 = cv2.imread("buf.png",0)
    subImage = image[900:920,780:800]
    if (subImage.sum())<140000:
        subprocess.call("adb shell input tap 800 920",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 325 2080",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 870 1441",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 900 455",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 770 1700",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 855 1400",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 55 80",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 55 80",shell=True)
    # else:
    #     studyTime = getTime(image3,875,975)
    #     openOrCloseIcon("icon3","close")
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    studyTime = getTime(image3,875,975)
    openOrCloseIcon("icon3","close")

def seekRolesManager():
    # index = 1030
    global seekingTime
    openOrClose("open")
    openOrCloseIcon("icon4","open")
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png")
    image3 = cv2.imread("buf.png",0)
    subImage = image[1030:1050,780:800]
    if (subImage.sum())<140000:
        subprocess.call("adb shell input tap 800 1050",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 924 1465",shell=True) #登庸
        time.sleep(1)
        subprocess.call("adb shell input tap 810 1725",shell=True) #登庸
        time.sleep(1)
        subprocess.call("adb shell input tap 55 80",shell=True)
        time.sleep(1)
    # else:
    #     seekingTime = getTime(image3,1000,1120)
    #     openOrCloseIcon("icon4","close")
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    seekingTime = getTime(image3,1000,1120)
    openOrCloseIcon("icon4","close")

def miningManager():
    global miningTime
    openOrClose("open")
    openOrCloseIcon("icon5","open")    
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png")
    subImage = image[1260:1370,40:240]
    image3 = cv2.imread("buf.png",0)
    # subImage = image[1250:1370,630:840]
    while not(cv2.imwrite("forward.png",subImage)):
        True
    text = pytesseract.image_to_string(Image.open("forward.png"),lang="chi_sim")
    if(text=="空 闲 中"):
        subprocess.call("adb shell input tap 765 1302",shell=True)
        time.sleep(3)
        subprocess.call("adb shell input tap 550 1807",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 350 1090",shell=True)
        time.sleep(3)
        subprocess.call("adb shell input text 1196",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 750 1090",shell=True)
        time.sleep(3)
        subprocess.call("adb shell input text 936",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 510 1270",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 720 1360",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 996 660",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 810 1253",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 800 2035",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 160 2000",shell=True)
        time.sleep(6)
    # else:
    #     miningTime = getTime(image3,1250,1370)
    #     print("正在挖矿，无需配置")
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    miningTime = getTime(image3,1250,1370)
    openOrCloseIcon("icon5","close")


def treasureManager():
    global treasureTime
    openOrClose("open")
    openOrCloseIcon("icon6","open")    
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png")
    subImage = image[1150:1170,780:800]
    image3 = cv2.imread("buf.png",0)
    if (subImage.sum())<140000:
        subprocess.call("adb shell input tap 800 1170",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 815 1680",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 815 1680",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 815 1680",shell=True)
        time.sleep(1)
        subprocess.call("adb shell input tap 55 80",shell=True)
        time.sleep(1)
    # else:
    #     treasureTime = getTime(image3,1130,1240)
    #     openOrCloseIcon("icon6","close")
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    treasureTime = getTime(image3,1130,1240)
    openOrCloseIcon("icon6","close")

def updateTime(dt,name):
    global buildTime,trainTime,studyTime,seekingTime,miningTime,treasureTime,buildTime2
    if name == "buildTime":
        # buildTime -= dt
        for i in range(4):
            trainTime[i]-=dt
        studyTime -= dt
        seekingTime -= dt
        miningTime -= dt
        treasureTime -= dt
    elif name == "trainTime":
        buildTime -= dt
        buildTime2 -= dt
        # trainTime -= dt
        studyTime -= dt
        seekingTime -= dt
        miningTime -= dt
        treasureTime -= dt
    elif name == "studyTime":
        buildTime -= dt
        buildTime2 -= dt
        for i in range(4):
            trainTime[i]-=dt
        # studyTime -= dt
        seekingTime -= dt
        miningTime -= dt
        treasureTime -= dt
    elif name == "seekingTime":
        buildTime -= dt
        buildTime2 -= dt
        for i in range(4):
            trainTime[i]-=dt
        studyTime -= dt
        # seekingTime -= dt
        miningTime -= dt
        treasureTime -= dt
    elif name == "miningTime":
        buildTime -= dt
        buildTime2 -= dt
        for i in range(4):
            trainTime[i]-=dt
        studyTime -= dt
        seekingTime -= dt
        # miningTime -= dt
        treasureTime -= dt
    elif name == "treasureTime":
        buildTime -= dt
        buildTime2 -= dt
        for i in range(4):
            trainTime[i]-=dt
        studyTime -= dt
        seekingTime -= dt
        miningTime -= dt
        # treasureTime -= dt

def fightWithHJ():
    global fightTime
    subprocess.call("adb shell input tap 78 1602",shell=True)
    time.sleep(1)
    subprocess.call("adb shell input tap 667 1483",shell=True)
    time.sleep(1)
    subprocess.call("adb shell input tap 780 2031",shell=True)
    time.sleep(3)
    subprocess.call("adb shell input tap 518 1537",shell=True)
    time.sleep(1)
    subprocess.call("adb shell input tap 1000 653",shell=True)
    time.sleep(1)
    subprocess.call("adb shell input tap 800 1245",shell=True)
    time.sleep(1)
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png",0)
    sec = 0
    subImage = image[1847:1939,624:820]
    c = 0
    err = [0,0,-5,-10,-15,-20,-25,-30,10,20,30,40,20,60,70]
    while True:
        while not(cv2.imwrite("time.png",subImage)):
            True
        text = pytesseract.image_to_string(Image.open("time.png"),lang="eng")
        if len(text)==8 and text[2]==":" and text[5]==":":
            print(text)
            sec = (int(text[0])*10 + int(text[1]))*3600 + (int(text[3])*10 + int(text[4]))*60 + (int(text[6])*10 + int(text[7]))
            break
        else:
            print(text)
            for i in range(subImage.shape[0]):
                for j in range(subImage.shape[1]):
                    if(subImage[i,j]<100+err[c]):
                        subImage[i,j] = 0
        if c>13:
            sec = 600
            break
        else:
            c+=1
    fightTime = 2*sec
    subprocess.call("adb shell input tap 760 2031",shell=True)
    time.sleep(2)

def manager():
    # buildTime = 0,trainTime = [],studyTime = 0,seekingTime = 0,miningTime = 0,treasureRime = 0
    global buildTime,trainTime,studyTime,seekingTime,miningTime,treasureTime,fightTime,buildTime2
    buildManager()
    time1 = time.time()
    # trainManager()
    time2 = time.time()
    studyManager()
    time3 = time.time()
    seekRolesManager()
    time4 = time.time()
    miningManager()
    time5 = time.time()
    treasureManager()
    time6 = time.time()
    buildTime -= int(time6 - time1)
    buildTime2 -= int(time6 - time1)
    for i in range(4):
        trainTime[i] -= int(time6 - time2)
    studyTime -= int(time6 - time3)
    seekingTime -= int(time6 - time4)
    miningTime -= int(time6 - time5)
    while True:
        timeS = time.time()
        buildTime-=1
        buildTime2-=1
        for i in range(4):
            trainTime[i]-=1
        studyTime-=1
        seekingTime-=1
        miningTime-=1
        treasureTime-=1
        if(buildTime<=-5)or(buildTime2<=-5):
            timeStart = time.time()
            buildManager()
            timeEnd = time.time()
            dt = int(timeEnd - timeStart)
            updateTime(dt,"buildTime")
        # if(min(trainTime)<=-5):
        #     timeStart = time.time()
        #     trainManager()
        #     timeEnd = time.time()
        #     dt = int(timeEnd - timeStart)
        #     updateTime(dt,"trainTime")
        if(studyTime<=-5):
            timeStart = time.time()
            studyManager()
            timeEnd = time.time()
            dt = int(timeEnd - timeStart)
            updateTime(dt,"studyTime")
        if(seekingTime<=-5):
            timeStart = time.time()
            seekRolesManager()
            timeEnd = time.time()
            dt = int(timeEnd - timeStart)
            updateTime(dt,"seekingTime")
        if(miningTime<=-120):
            timeStart = time.time()
            miningManager()
            timeEnd = time.time()
            dt = int(timeEnd - timeStart)
            updateTime(dt,"miningTime")
        if(treasureTime<=-5):
            timeStart = time.time()
            treasureManager()
            timeEnd = time.time()
            dt = int(timeEnd - timeStart)
            updateTime(dt,"treasureTime")
        
        subprocess.call("cls",shell=True)
        print("buildTime:" + str(buildTime))
        print("buildTime2:" + str(buildTime2))
        # print("trainTime:" + str(min(trainTime)))
        print("studyTime:"+str(studyTime))
        print("seekingTime:"+str(seekingTime))
        print("miningTime:" + str(miningTime))
        print("treasureTime:" + str(treasureTime))
        timeE = time.time()
        ddt = timeE - timeS
        if(ddt<=1):
            time.sleep(1-ddt)
        else:
            pass
manager()
# treasureManager()
# isOpenWindows()
# trainManager()
# fightWithHJ()
# while True:
#     if(fightTime<0):
#         # cute()
#         fightWithHJ()
#     fightTime-=1
#     time.sleep(1)
#     subprocess.call("cls",shell=True)
#     print("fightTime:" + str(fightTime))
# trainManager()
# studyManager()
# seekRolesManager()
# miningManager()
# image = cv2.imread("buf.png",0)
# # getTime(image)
# subImage = image[40:110,20:110]
# for i in range(subImage.shape[0]):
#     for j in range(subImage.shape[1]):
#         if(subImage[i,j]<100):
#             subImage[i,j] = 0
#         else:
#             subImage[i,j] = 255
# cv2.imshow("figure",subImage)
# cv2.imwrite("main2.png",subImage)
# while not(cv2.imwrite("time.png",subImage)):
#     True
# text = pytesseract.image_to_string(Image.open("time.png"),lang="eng")
# print(text)