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


class UI_SMS(object):
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

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.installEventFilter(self)  # eventFilter를 central_widget에 설치


        self.phoneLabel_1 = QLabel("휴대폰 번호를 입력해주세요.")
        self.phoneLabel_1.setSizePolicy(exExSP)
        self.phoneLabel_1.setMaximumHeight(int(h*0.1))
        self.phoneLabel_1.setAlignment(QtCore.Qt.AlignCenter)
        self.phoneLabel_1.setStyleSheet(
            extraLargeFont +
            "color: " + secondary_text_color + ";")
        
        UI_SMS.phoneLabel_2 = QLabel("")
        UI_SMS.phoneLabel_2.setSizePolicy(exExSP)
        UI_SMS.phoneLabel_2.setMaximumHeight(int(h*0.1))
        UI_SMS.phoneLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        UI_SMS.phoneLabel_2.setStyleSheet(
            extraLargeFont +
            "color: " + secondary_text_color + ";")

        UI_SMS.phoneBtns = []
        for i in range(10):
            if i == 9:
                self.btn = QPushButton("0")
            else:
                self.btn = QPushButton(str(i + 1))
            self.btn.setFixedSize(int(h*0.08), int(h*0.08))
            self.btn.setStyleSheet(
                largeFont +
                "color: " + primary_text_color + ";"
                "background-color: " + primary_color + ";")
            if gVar.mode == "touch":
                self.btn.clicked.connect(lambda state, x=i: UI_SMS.clicked_phoneBtn(x))
            elif gVar.mode == "voice":
                self.btn.installEventFilter(self)
            UI_SMS.phoneBtns.append(self.btn)
        
        self.delBtn = QPushButton("지우기")
        self.delBtn.setFixedSize(int(h*0.08), int(h*0.08))
        self.delBtn.setStyleSheet(
            largeFont +
            "color: " + primary_text_color + ";"
            "background-color: " + primary_color + ";")
        if gVar.mode == "touch":
            self.delBtn.clicked.connect(UI_SMS.clicked_delBtn)
        elif gVar.mode == "voice":
            self.delBtn.installEventFilter(self)

        self.cleatBtn = QPushButton("전부\n지우기")
        self.cleatBtn.setFixedSize(int(h*0.08), int(h*0.08))
        self.cleatBtn.setStyleSheet(
            largeFont +
            "color: " + primary_text_color + ";"
            "background-color: " + primary_color + ";")
        if gVar.mode == "touch":
            self.cleatBtn.clicked.connect(UI_SMS.clicked_clearBtn)
        elif gVar.mode == "voice":
            self.cleatBtn.installEventFilter(self)

        self.okBtn = QPushButton("확인")
        self.okBtn.setFixedHeight(int(h*0.08))
        self.okBtn.setSizePolicy(exExSP)
        self.okBtn.setStyleSheet(
            largeFont +
            "color: " + primary_text_color + ";"
            "background-color: " + primary_color + ";")
        if gVar.mode == "touch":
            self.okBtn.clicked.connect(self.finish_sms)
        elif gVar.mode == "voice":
            self.okBtn.installEventFilter(self)

            
        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.phoneLayout = QGridLayout()

        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        
        self.phoneLayout.setAlignment(Qt.AlignCenter)
        self.phoneLayout.setSpacing(int(h*0.01))
        self.phoneLayout.setContentsMargins(
            int(h*0.05), int(h*0.05), int(h*0.05), int(h*0.05))
        
        self.mainLayout.addWidget(self.phoneLabel_1)
        self.mainLayout.addWidget(UI_SMS.phoneLabel_2)
        self.mainLayout.addLayout(self.phoneLayout)

        for i in range(10):
            self.phoneLayout.addWidget(UI_SMS.phoneBtns[i], i//3, i%3)
        self.phoneLayout.addWidget(UI_SMS.phoneBtns[9], 3, 1)
        self.phoneLayout.addWidget(self.delBtn, 3, 0)
        self.phoneLayout.addWidget(self.cleatBtn, 3, 2)

        self.phoneLayout.addWidget(self.okBtn, 4, 0, 1, 3)

    def clicked_phoneBtn(x):
        if len(UI_SMS.phoneLabel_2.text()) < 13:
            UI_SMS.phoneLabel_2.setText(UI_SMS.phoneLabel_2.text() + UI_SMS.phoneBtns[x].text())
            if len(UI_SMS.phoneLabel_2.text()) == 3 or len(UI_SMS.phoneLabel_2.text()) == 8:
                UI_SMS.phoneLabel_2.setText(UI_SMS.phoneLabel_2.text() + "-")

        numbers = [int(char) for char in UI_SMS.phoneLabel_2.text() if char.isdigit()]
        gVar.phoneNum = ''.join(map(str, numbers))

    def clicked_delBtn(self):
        if len(UI_SMS.phoneLabel_2.text()) == 5 or len(UI_SMS.phoneLabel_2.text()) == 10:
            UI_SMS.phoneLabel_2.setText(UI_SMS.phoneLabel_2.text()[:-2])
        else:
            UI_SMS.phoneLabel_2.setText(UI_SMS.phoneLabel_2.text()[:-1])

    def clicked_clearBtn(self):
        UI_SMS.phoneLabel_2.setText("")