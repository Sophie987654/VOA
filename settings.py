import pyautogui
from datetime import *

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class gVar:
    retry = 0
    mode = "touch"
    locateSelf = True
    currentP = "main"
    pause = 0
    menu = 0
    face_first = True
    no_face_first = True
    firstAsk = True
    darkMode = False
    
    depStat = "서울"
    arrStat = ""
    depDate = datetime.today().strftime("%Y%m%d")
    depTime = datetime.today().strftime("%H%M")
    arrTime = ""
    trainInfo = ""
    adultPrice = 0
    knd = ""
    
    adultNum = 0
    childNum = 0
    oldNum = 0
    disabledNum = 0
    totalPrice = 0
    totalPeople = 0
    
    seatNum = 0
    preSeatNum = 0
    leftSeat = 32
    selSeats = []
    selCar = "1호차"

    phoneNum = ""

    ampm = ""
    day = ""
    hour = ""
    minute = ""
    
    def gVarInit():
        gVar.retry = 0
        gVar.mode = "touch"
        gVar.locateSelf = True
        gVar.currentP = "main"
        gVar.pause = 0
        gVar.menu = 0
        gVar.face_first = True
        gVar.no_face_first = True
        gVar.firstAsk = True
        gVar.darkMode = False

        gVar.depStat = "서울"
        gVar.arrStat = ""
        gVar.depDate = datetime.today().strftime("%Y%m%d")
        gVar.depTime = datetime.today().strftime("%H%M")
        gVar.arrTime = ""
        gVar.knd = ""
        gVar.trainInfo = ""

        gVar.adultNum = 0
        gVar.childNum = 0
        gVar.oldNum = 0
        gVar.disabledNum = 0
        gVar.adultPrice = 0
        gVar.totalPrice = 0
        gVar.totalPeople = 0
        
        gVar.seatNum = 0
        gVar.preSeatNum = 0
        gVar.leftSeat = 32
        gVar.selSeats = []
        gVar.selCar = "1호차"

        gVar.phoneNum = ""

        gVar.ampm = ""
        gVar.day = ""
        gVar.hour = ""
        gVar.minute = ""

    def discount(originPrice, pType):
        if pType == 1:
            int(round(int(originPrice) * 0.5, -2))
        elif pType == 2:
            int(round(int(originPrice) * 0.7, -2))


# 현재 화면의 크기
w, h = pyautogui.size()

# 이미지 경로
img_path = "src/img/"

# SizePolicy
# 너비 확장 높이 확장
exExSP = QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

# small font
smallfontSize = str(int(h*0.012))
smallFont = "font-size: " + smallfontSize + "px;"
# basic font
basicfontSize = str(int(h*0.013))
basicFont = "font-size: " + basicfontSize + "px;"
# median font
medianfontSize = str(int(h*0.015))
medianFont = "font-size: " + medianfontSize + "px;"
# large font
largefontSize = str(int(h*0.02))
largeFont = "font-size: " + largefontSize + "px;"
# Extralarge font
extraLargefontSize = str(int(h*0.03))
extraLargeFont = "font-size: " + extraLargefontSize + "px;"

# color palette
blue = "rgb(41, 121, 255)"
white = "rgb(255, 255, 255)"
black = "rgb(0, 0, 0)"
lightGray = "rgb(195, 195, 195)"
transparent = "rgba(255, 255, 255, 0)"
teal = "rgb(29, 233, 182)"
darkGray = "rgb(35, 38, 41)"
red = "rgb(255, 0, 0)"
lightBlue = "rgb(0, 176, 255)"

class myColor:
    primary_color = blue
    secondary_color = white
    primary_text_color = white
    secondary_text_color = black