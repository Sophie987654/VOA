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


class UI_SelSit(object):
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
        
        UI_SelSit.selected_button_id = []
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # ==================== Header ====================
        self.headerFrame = QFrame()
        self.headerFrame.setMaximumSize(w, int(h*0.1))
        self.headerFrame.setSizePolicy(exExSP)
        self.headerFrame.setStyleSheet(
            "background-color: " + primary_color + ";")
        
        self.headerLabel = QLabel("승차권 예매")
        self.headerLabel.setSizePolicy(exExSP)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setStyleSheet(
            extraLargeFont +
            "color: " + primary_text_color + ";")
        
        # -------------------- 뒤로가기 버튼 --------------------
        self.backBtn = QPushButton()
        self.backBtn.setMaximumSize(int(h*0.15), int(h*0.1))
        self.backBtn.setSizePolicy(exExSP)
        self.backBtn.setText("뒤로\n가기")
        self.backBtn.setStyleSheet(
            largeFont +
            "color: " + secondary_text_color + ";"
            "background-color: " + secondary_color + ";")
        if gVar.mode == "touch":
            self.backBtn.clicked.connect(self.go_to_check)
        elif gVar.mode == "voice":
            self.backBtn.installEventFilter(self)

        # -------------------- 처음으로 버튼 --------------------
        self.homeBtn = QPushButton()
        self.homeBtn.setMaximumSize(int(h*0.15), int(h*0.1))
        self.homeBtn.setSizePolicy(exExSP)
        self.homeBtn.setText("처음\n으로")
        self.homeBtn.setStyleSheet(
            largeFont +
            "color: " + secondary_text_color + ";"
            "background-color: " + secondary_color + ";")
        if gVar.mode == "touch":
            self.homeBtn.clicked.connect(self.go_to_main)
        elif gVar.mode == "voice":
            self.homeBtn.installEventFilter(self)


        # ==================== 호차선택 ====================
        UI_SelSit.carNumBtns = []
        UI_SelSit.carBtnGroup = QButtonGroup()
        for i in range(8):
            self.carNumBtn = QPushButton(str(i+1) + '호차')
            self.carNumBtn.setCheckable(True)
            self.carNumBtn.setSizePolicy(exExSP)
            self.carNumBtn.setFixedSize(int(h*0.1), int(h*0.05))
            self.carNumBtn.setStyleSheet(
                largeFont +
                "font-weight: bold;" +
                "border: none;")
            UI_SelSit.carNumBtns.append(self.carNumBtn)
            UI_SelSit.carBtnGroup.addButton(self.carNumBtn, i)
            if gVar.mode == "touch":
                self.carNumBtn.clicked.connect(UI_SelSit.clicked_carNumBtn)
            elif gVar.mode == "voice":
                self.carNumBtn.installEventFilter(self)
                
        UI_SelSit.carNumBtns[0].setStyleSheet(
            largeFont +
            "font-weight: bold;" +
            "background-color: " + primary_color + ";" +
            "color: " + primary_text_color + ";")
        
        
        # ==================== 좌석선택 ====================
        self.leftSeatLayout = QHBoxLayout()
        self.leftSeatLabel_1 = QLabel("잔여 좌석 ")
        self.leftSeatLabel_1.setStyleSheet(
            largeFont +
            "font-weight: bold;")
        self.leftSeatLabel_1.setAlignment(Qt.AlignRight)

        UI_SelSit.leftSeatLabel_2 = QLabel(f"{gVar.leftSeat}")
        UI_SelSit.leftSeatLabel_2.setStyleSheet(
            largeFont +
            "font-weight: bold;" +
            "color: " + myColor.primary_color + ";")
        UI_SelSit.leftSeatLabel_2.setAlignment(Qt.AlignRight)

        self.leftSeatLabel_3 = QLabel(" /32")
        self.leftSeatLabel_3.setStyleSheet(
            largeFont +
            "font-weight: bold;")
        self.leftSeatLabel_3.setAlignment(Qt.AlignLeft)
        self.leftSeatLayout.addWidget(self.leftSeatLabel_1)
        self.leftSeatLayout.addWidget(UI_SelSit.leftSeatLabel_2)
        self.leftSeatLayout.addWidget(self.leftSeatLabel_3)
        
        self.seatLocLabel = []
        self.seatLocText = ["창측", "통로측", "통로측", "창측"]
        for i in range(4):
            self.seatLocLabel.append(QLabel(self.seatLocText[i]))
            if (self.seatLocLabel[i].text() == "창측"):
                self.seatLocLabel[i].setStyleSheet(
                    largeFont +
                    "color: " + primary_color + ";")
            else:
                self.seatLocLabel[i].setStyleSheet(
                    largeFont)
            self.seatLocLabel[i].setAlignment(Qt.AlignCenter)
        
        UI_SelSit.seatBtns = []
        seatLineText = ["A", "B", "C", "D"]
        aisle = []
        for i in range(4):
            for j in range(8):
                if j < 4: # 순방향
                    self.seatBtn = QPushButton(str(j+1) + seatLineText[i])
                    self.seatBtn.setStyleSheet(
                        largeFont)
                    UI_SelSit.seatBtns.append(self.seatBtn)
                else: # 역방향
                    self.seatBtn = QPushButton(str(j+1) + seatLineText[i-4])
                    self.seatBtn.setStyleSheet(
                        largeFont +
                        "border-style: dashed;")
                    UI_SelSit.seatBtns.append(self.seatBtn)

                self.seatBtn.setCheckable(True)
                self.seatBtn.setMaximumWidth(int(h*0.1))
                if gVar.mode == "touch":
                    self.seatBtn.clicked.connect(lambda _, id=j + 8*i: UI_SelSit.clicked_seatBtn(id))
                elif gVar.mode == "voice":
                    self.seatBtn.installEventFilter(self)

        for i in range(8):
            aisle.append(QLabel("▲"))
            aisle[i].setStyleSheet(
                largeFont +
                "color: " + lightGray + ";")
            aisle[i].setAlignment(Qt.AlignCenter)
            aisle[i].setFixedSize(int(h*0.05), int(h*0.05))

        # -------------------- 확인 버튼 --------------------
        self.buyBtn = QPushButton()
        self.buyBtn.setMinimumHeight(int(h*0.2))
        self.buyBtn.setMaximumHeight(int(h*0.3))
        self.buyBtn.setSizePolicy(exExSP)
        self.buyBtn.setText("예매하기")
        self.buyBtn.setStyleSheet(
            extraLargeFont +
            "background-color: " + primary_color + ";"
            "color: " + primary_text_color + ";"
            "margin:" + str(int(h*0.05)) + ";")
        if gVar.mode == "touch":
            self.buyBtn.clicked.connect(self.go_to_check)
        elif gVar.mode == "voice":
            self.buyBtn.installEventFilter(self)


        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.hearderLayout = QHBoxLayout(self.headerFrame)
        self.carNumLayout = QHBoxLayout()
        self.seatGridLayout = QGridLayout()
        
        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.hearderLayout.setContentsMargins(
            int(w*0.01), int(h*0.01), int(w*0.01), int(h*0.01))

        self.carNumLayout.setContentsMargins(
            int(w*0.05), int(h*0.05), int(w*0.05), int(h*0.05))
        
        self.seatGridLayout.setSpacing(0)
        self.seatGridLayout.setContentsMargins(
            int(w*0.05), int(h*0.05), int(w*0.05), int(h*0.05))
        
        # -------------------- Add Widgets & Layouts --------------------
        self.mainLayout.addWidget(self.headerFrame)

        self.hearderLayout.addWidget(self.backBtn)
        self.hearderLayout.addWidget(self.headerLabel)
        self.hearderLayout.addWidget(self.homeBtn)
        
        self.mainLayout.addLayout(self.carNumLayout)
        for btn in UI_SelSit.carNumBtns:
            self.carNumLayout.addWidget(btn)

        self.mainLayout.addLayout(self.leftSeatLayout)
        self.mainLayout.addLayout(self.seatGridLayout)

        self.seatGridLayout.addWidget(self.seatLocLabel[0], 0, 0)
        self.seatGridLayout.addWidget(self.seatLocLabel[1], 0, 1)
        self.seatGridLayout.addWidget(self.seatLocLabel[2], 0, 3)
        self.seatGridLayout.addWidget(self.seatLocLabel[3], 0, 4)
        
        for i in range(5):
            for j in range(8):
                if i == 2:
                    self.seatGridLayout.addWidget(aisle[j], j + 1, i)
                elif i < 2:
                    self.seatGridLayout.addWidget(UI_SelSit.seatBtns[j + 8*i], j + 1, i)
                elif i > 2:
                    self.seatGridLayout.addWidget(UI_SelSit.seatBtns[j + 8*(i-1)], j + 1, i)

        self.mainLayout.addWidget(self.buyBtn)
        
    def clicked_carNumBtn(self):
        for i, btn in enumerate(UI_SelSit.carNumBtns):
            if btn.isChecked():
                gVar.selCar = btn.text()
                btn.setStyleSheet(
                    largeFont +
                    "font-weight: bold;"
                    "background-color: " + myColor.primary_color + ";" +
                    "color: " + myColor.secondary_color + ";"
                    "border: none;"
                )
            else:
                btn.setStyleSheet(
                    largeFont +
                    "font-weight: bold;"
                    "background-color: " + transparent + ";" +
                    "color: " + myColor.secondary_text_color + ";"
                    "border: none;"
                )

    def clicked_seatBtn(id):
        gVar.seatNum = 0
        gVar.selSeats = []

        for i, btn in enumerate(UI_SelSit.seatBtns):
            if btn.isChecked():
                gVar.seatNum += 1
                gVar.selSeats.append(btn.text())

        if gVar.seatNum > gVar.totalPeople:
            UI_SelSit.seatBtns[id].setChecked(False)  # 선택한 버튼 선택 해제
            gVar.seatNum -= 1
            gVar.selSeats.pop()

        UI_SelSit.leftSeatLabel_2.setText(f"{gVar.leftSeat - gVar.seatNum}")
        
        