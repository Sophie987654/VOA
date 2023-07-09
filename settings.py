import pyautogui, pygame, pyttsx3
from gtts import gTTS
from datetime import *

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class gVar:
    mode = "touch"
    locateSelf = True
    currentP = "main"
    pause = 0
    menu = 1
    face_cnt = 0
    no_face_cnt = 0
    firstAsk = True
    darkMode = False
    clickAble = True
    
    depStat = "서울"
    arrStat = ""
    depDate = datetime.today().strftime("%Y%m%d")
    depTime = datetime.today().strftime("%H%M")
    knd = "KTX"
    notExist = False

    def gVarInit():
        gVar.mode = "touch"
        gVar.locateSelf = True
        gVar.currentP = "main"
        gVar.pause = 0
        gVar.menu = 1
        gVar.face_cnt = 0
        gVar.no_face_cnt = 0
        gVar.firstAsk = True
        gVar.darkMode = False
        gVar.clickAble = True

        gVar.depStat = "서울"
        gVar.arrStat = ""
        gVar.depDate = datetime.today().strftime("%Y%m%d")
        gVar.depTime = datetime.today().strftime("%H%M")
        gVar.knd = "KTX"
        gVar.notExist = False


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

def pyTTS(txt):
    engine = pyttsx3.init()
    engine.say(txt)
    engine.runAndWait()

def gglTTS(txt, fn):
    text = txt
    tts = gTTS(text=text, lang='ko')
    tts.save(fn + ".mp3")

    music_file = fn + ".mp3"   # mp3 or mid file

    freq = 16000    # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
    bitsize = -16   # signed 16 bit. support 8,-8,16,-16
    channels = 1    # 1 is mono, 2 is stereo
    buffer = 2048   # number of samples (experiment to get right sound)

    # default : pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(30)
    pygame.mixer.quit()