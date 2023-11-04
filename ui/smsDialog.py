import time as t
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_material import *
import pandas as pd
from pandas import json_normalize
from settings import *
from src.module.TAGO import *
from src.module.TAGO_data import *
from src.module.sms import *


class SMS_Dialog(QDialog):
    def __init__(self):
        super(SMS_Dialog, self).__init__()
        self.setupUI()
        self.show()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def setupUI(self):
        if gVar.darkMode:
            primary_color = teal
            secondary_color = darkGray
            primary_text_color = darkGray
            secondary_text_color = teal
        else:
            primary_color = "rgb(41, 121, 255)" # blue
            secondary_color = "rgb(255, 255, 255)" # white
            primary_text_color = "rgb(255, 255, 255)" # white
            secondary_text_color = "rgb(0, 0, 0)" # black
            

        self.askLabel = QLabel("문자로 예매 내역을 보내시겠습니까?")
        self.askLabel.setSizePolicy(exExSP)
        self.askLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.askLabel.setStyleSheet(
            extraLargeFont +
            "margin: " + str(int(h*0.05)) + "px;" +
            "color: " + secondary_text_color + ";")
        
        self.yesBtn = QPushButton()
        self.yesBtn.setFixedSize(int(h*0.15), int(h*0.08))
        self.yesBtn.setSizePolicy(exExSP)
        self.yesBtn.setText("네")
        self.yesBtn.setStyleSheet(
            largeFont +
            "color: " + primary_text_color + ";"
            "background-color: " + primary_color + ";")
        if gVar.mode == "touch":
            self.yesBtn.clicked.connect(self.clicked_yesBtn)
        elif gVar.mode == "voice":
            self.yesBtn.installEventFilter(self)

        self.noBtn = QPushButton()
        self.noBtn.setFixedSize(int(h*0.15), int(h*0.08))
        self.noBtn.setSizePolicy(exExSP)
        self.noBtn.setText("아니오")
        self.noBtn.setStyleSheet(
            largeFont +
            "color: " + primary_color + ";"
            "background-color: " + primary_text_color + ";")
        if gVar.mode == "touch":
            self.noBtn.clicked.connect(self.clicked_noBtn)
        elif gVar.mode == "voice":
            self.noBtn.installEventFilter(self)

        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self)
        self.yesnoLayout = QHBoxLayout()
        
        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(
            int(w*0.05), int(h*0.05), int(w*0.05), int(h*0.05))
        self.mainLayout.setSpacing(0)

        self.yesnoLayout.setAlignment(Qt.AlignCenter)
        self.yesnoLayout.setSpacing(int(h*0.05))

        # -------------------- Add Widgets & Layouts --------------------
        self.mainLayout.addWidget(self.askLabel)
        
        self.yesnoLayout.addWidget(self.yesBtn)
        self.yesnoLayout.addWidget(self.noBtn)
        self.mainLayout.addLayout(self.yesnoLayout)

        if gVar.mode == "voice":
            SMS_Dialog.clicked_yesBtn(self)

    def clicked_yesBtn(self):
        self.close()

    def clicked_noBtn(self):
        self.close()
        self.charge()

    def charge(self):
        pyTTS("IC칩을 위로 향하게 하여 카드 투입구에 꽂아주세요.")
        # 5초 멈춤
        t.sleep(5)
        pyTTS("결제가 완료되었습니다. 감사합니다.")