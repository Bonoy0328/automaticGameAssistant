import cv2
import subprocess
import time
import pytesseract
from PIL import Image
import numpy as np
import math
buildTime = 0
trainTime = [0,0,0,0]
studyTime = 0
seekingTime = 0
miningTime = 0
treasureTime = 0
pytesseract.pytesseract.tesseract_cmd = "C://Program Files/Tesseract-OCR/tesseract.exe"
#判断是否打开了进度管理页面
def isOpenWindows():
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png",0)
    subImage = image[478:523,344:512]
    processOfImage = cv2.imread("process.png",0)
    imageBuf = processOfImage-subImage
    print(imageBuf.sum())
    if imageBuf.sum()<600000:
        return True
    else:
        return False
#打开或者关闭进度管理界面
def openOrClose(flag):
    if(flag=="open"):                 
        while not(isOpenWindows()):
            subprocess.call("adb shell input tap 40 1045",shell=True) 
            time.sleep(0.3)
    else:                     
        while (isOpenWindows()):
            subprocess.call("adb shell input tap 890 1045",shell=True) 
            time.sleep(0.3)
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
            sec = 1800
            break
        else:
            c+=1
    return sec

#建筑管理的函数
def buildManager():
    global buildTime
    openOrClose("open")
    openOrCloseIcon("icon1","open")
    #780:800 630:650判断颜色
    while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
        True
    image = cv2.imread("buf.png")
    image3 = cv2.imread("buf.png",0)
    subImage = image[630:650,780:800]
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
    # else:
    #     buildTime = getTime(image3,610,700)
    #     openOrCloseIcon("icon1","close")
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    buildTime = getTime(image3,610,700)
    openOrCloseIcon("icon1","close")

def trainManager():
    #四个兵种，分别对应于780   800 890 970 1060
    global trainTime
    index = [800,890,970,1060]
    d = 0
    index2 = [770,850,940,1020]
    for i in index:
        openOrClose("open")
        openOrCloseIcon("icon2","open")
        while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
            True
        image = cv2.imread("buf.png")
        image3 = cv2.imread("buf.png",0)
        subImage = image[i:i+20,780:800]   
        if(subImage.sum())<140000:
            if(d>=1):
                trainTime[d-1] = getTime(image3,index2[d-1],index2[d-1]+100)
            subprocess.call("adb shell input tap 800 "+str(i+20),shell=True)
            time.sleep(0.5)
            #880:900 1990:2010
            while subprocess.call("adb exec-out screencap -p > buf.png",shell=True):
                True
            image = cv2.imread("buf.png")
            subImage = image[1990:2010,880:900]
            if (subImage.sum())<140000:
                subprocess.call("adb shell input tap 900 2010",shell=True)
                time.sleep(0.3)
                subprocess.call("adb shell input tap 55 80",shell=True)
        else:
            print(subImage.sum())
            trainTime[d] = getTime(image3,index2[d],index2[d]+100)
        d+=1
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    trainTime[d-1] = getTime(image3,index2[d-1],index2[d-1]+100)
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
        time.sleep(0.5)
        subprocess.call("adb shell input tap 870 2080",shell=True)
        time.sleep(0.5)
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
        subprocess.call("adb shell input tap 830 1720",shell=True)
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
        time.sleep(0.5)
        subprocess.call("adb shell input text 1193",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 750 1090",shell=True)
        time.sleep(0.5)
        subprocess.call("adb shell input text 935",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 510 1270",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 720 1360",shell=True)
        time.sleep(2)
        subprocess.call("adb shell input tap 305 2040",shell=True)
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
        subprocess.call("adb shell input tap 55 80",shell=True)
        time.sleep(1)
    # else:
    #     treasureTime = getTime(image3,1130,1240)
    #     openOrCloseIcon("icon6","close")
    openOrClose("open")
    image3 = cv2.imread("buf.png",0)
    treasureTime = getTime(image3,1130,1240)
    openOrCloseIcon("icon6","close")

def manager():
    # buildTime = 0,trainTime = [],studyTime = 0,seekingTime = 0,miningTime = 0,treasureRime = 0
    buildManager()
    trainManager()
    studyManager()
    seekRolesManager()
    miningManager()
    treasureManager()
    global buildTime,trainTime,studyTime,seekingTime,miningTime,treasureTime
    while True:
        buildTime-=1
        for i in range(4):
            trainTime[i]-=1
        studyTime-=1
        seekingTime-=1
        miningTime-=1
        treasureTime-=1
        time.sleep(1)
        if(buildTime<=0):
            buildManager()
        if(min(trainTime)<=0):
            trainManager()
        if(studyTime<=0):
            studyManager()
        if(seekingTime<=0):
            seekRolesManager()
        if(miningTime<=0):
            miningManager()
        if(treasureTime<=0):
            treasureManager()
        print("buildTime:" + str(buildTime))
        print("trainTime:" + str(min(trainTime)))
        print("studyTime:"+str(studyTime))
        print("seekingTime:"+str(seekingTime))
        print("miningTime:" + str(miningTime))
        print("treasureTime:" + str(treasureTime))
manager()
# trainManager()
# studyManager()
# seekRolesManager()
# miningManager()
# image = cv2.imread("buf.png",0)
# # getTime(image)
# subImage = image[875:975,360:640]
# for i in range(subImage.shape[0]):
#     for j in range(subImage.shape[1]):
#         if(subImage[i,j]<100):
#             subImage[i,j] = 0
# while not(cv2.imwrite("time.png",subImage)):
#     True
# text = pytesseract.image_to_string(Image.open("time.png"),lang="eng")
# print(text)