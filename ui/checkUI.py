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


class UI_Check(object):
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
        self.backBtn.setFixedSize(int(h*0.15), int(h*0.08))
        self.backBtn.setSizePolicy(exExSP)
        self.backBtn.setText("뒤로\n가기")
        self.backBtn.setStyleSheet(
            largeFont +
            "color: " + secondary_text_color + ";"
            "background-color: " + secondary_color + ";")
        if gVar.mode == "touch":
            self.backBtn.clicked.connect(self.go_to_selSit)
        elif gVar.mode == "voice":
            self.backBtn.installEventFilter(self)

        # -------------------- 처음으로 버튼 --------------------
        self.homeBtn = QPushButton()
        self.homeBtn.setFixedSize(int(h*0.15), int(h*0.08))
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
        
        #-----------------------예매확인-------------------------
        departure = gVar.depStat
        arrival = gVar.arrStat
        departure_time = gVar.depTime
        arrival_time = gVar.arrTime
        train_info = gVar.trainInfo
        price = 0
        
        self.depNameLabel = QLabel("출발")
        self.depNameLabel.setAlignment(Qt.AlignLeft)
        self.depNameLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")
        self.depLabel = QLabel(f"{departure}({departure_time})")
        self.depLabel.setAlignment(Qt.AlignLeft)
        self.depLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")
        
        self.arrNameLabel = QLabel("도착")
        self.arrNameLabel.setAlignment(Qt.AlignLeft)
        self.arrNameLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")
        self.arrLabel = QLabel(f"{arrival}({arrival_time})")
        self.arrLabel.setAlignment(Qt.AlignLeft)
        self.arrLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")
        
        self.trainNameLabel = QLabel("열차")
        self.trainNameLabel.setAlignment(Qt.AlignLeft)
        self.trainNameLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")
        self.trainLabel = QLabel(f"{train_info}")
        self.trainLabel.setAlignment(Qt.AlignLeft)
        self.trainLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")
        
        self.priceNameLabel = QLabel("가격")
        self.priceNameLabel.setAlignment(Qt.AlignLeft)
        self.priceNameLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")
        self.priceLabel = QLabel(f"{gVar.totalPrice}원")
        self.priceLabel.setAlignment(Qt.AlignLeft)
        self.priceLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")

        # -----------------------인원수정하기-------------------------
        self.childPrice = int(round(int(gVar.adultPrice) * 0.5, -2))
        self.oldPrice = int(round(int(gVar.adultPrice) * 0.7, -2))
        self.disabledPrice = int(round(int(gVar.adultPrice) * 0.5, -2))
        self.personnel = {
            f"성인({gVar.adultPrice}원)": gVar.adultNum,
            f"어린이({self.childPrice}원)": gVar.childNum,
            f"경로({self.oldPrice}원)": gVar.oldNum,
            f"중증장애인({self.disabledPrice}원)": gVar.disabledNum,
        }
        
        self.price = {
            f"성인({gVar.adultPrice}원)": int(gVar.adultPrice),
            f"어린이({self.childPrice}원)": self.childPrice,
            f"경로({self.oldPrice}원)": self.oldPrice,
            f"중증장애인({self.disabledPrice}원)": self.disabledPrice
        }

        self.personnel_buttons = []
        self.btnObjs = []

        for p_type in self.personnel.keys():
            p_label = QLabel(f"{p_type}")
            p_label.setAlignment(Qt.AlignLeft)
            p_label.setStyleSheet(
                largeFont +
                "font-weight: bold;"
                "color: " + secondary_text_color + ";")
            
            if "성인" in p_type:
                p_count_label = QLabel(f"{gVar.adultNum}")
            elif "어린이" in p_type:
                p_count_label = QLabel(f"{gVar.childNum}")
            elif "경로" in p_type:
                p_count_label = QLabel(f"{gVar.oldNum}")
            elif "장애인" in p_type:
                p_count_label = QLabel(f"{gVar.disabledNum}")
            p_count_label.setAlignment(Qt.AlignLeft)
            p_count_label.setStyleSheet(
                largeFont +
                "font-weight: bold;"
                "color: " + secondary_text_color + ";")
            
            self.personnel_buttons.append((p_type, p_count_label))
            self.btnObjs.append((p_label, p_count_label))

        self.selSeatLabel = QLabel(f"선택한 좌석({gVar.selCar})")
        self.selSeatLabel.setAlignment(Qt.AlignLeft)
        self.selSeatLabel.setStyleSheet(
            largeFont +
            "font-weight: bold;"
            "color: " + secondary_text_color + ";")

        self.selSeats = []
        for n in gVar.selSeats:
            self.selSeats.append(QLabel(f"{n}"))
            self.selSeats[-1].setAlignment(Qt.AlignCenter)
            self.selSeats[-1].setStyleSheet(
                largeFont +
                "font-weight: bold;"
                "color: " + primary_text_color + ";"
                "background-color: " + primary_color + ";")


        # -------------------- 확인 버튼 --------------------
        self.checkBtn = QPushButton()
        self.checkBtn.setMinimumHeight(int(h*0.1))
        self.checkBtn.setMaximumHeight(int(h*0.2))
        self.checkBtn.setSizePolicy(exExSP)
        self.checkBtn.setText("결제하기")
        self.checkBtn.setStyleSheet(
            extraLargeFont +
            "background-color: " + primary_color + ";"
            "color: " + primary_text_color + ";"
            "margin:" + str(int(h*0.05)) + ";")
        if gVar.mode == "touch":
            self.checkBtn.clicked.connect(self.dlg_sms)
        elif gVar.mode == "voice":
            self.checkBtn.installEventFilter(self)
            
        self.Hspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)


        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.hearderLayout = QHBoxLayout(self.headerFrame)
        self.gridLayout = QGridLayout()
        self.selSeatsLayout = QHBoxLayout()
        
        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.hearderLayout.setContentsMargins(
            int(w*0.01), int(h*0.01), int(w*0.01), int(h*0.01))
        
        self.gridLayout.setAlignment(Qt.AlignLeft)
        self.gridLayout.setVerticalSpacing(int(h*0.01))
        self.gridLayout.setHorizontalSpacing(int(h*0.02))
        self.gridLayout.setContentsMargins(
            int(h*0.05), int(h*0.05), int(h*0.05), int(h*0.05))

        self.selSeatsLayout.setAlignment(Qt.AlignLeft)
        self.selSeatsLayout.setSpacing(10)

        # -------------------- Add Widgets & Layouts --------------------
        self.mainLayout.addWidget(self.headerFrame)
        
        self.hearderLayout.addWidget(self.backBtn)
        self.hearderLayout.addWidget(self.headerLabel)
        self.hearderLayout.addWidget(self.homeBtn)
        
        self.mainLayout.addLayout(self.gridLayout)
        self.gridLayout.addWidget(self.depNameLabel, 0, 0)
        self.gridLayout.addWidget(self.depLabel, 0, 1)
        self.gridLayout.addWidget(self.arrNameLabel, 1, 0)
        self.gridLayout.addWidget(self.arrLabel, 1, 1)
        self.gridLayout.addWidget(self.trainNameLabel, 2, 0)
        self.gridLayout.addWidget(self.trainLabel, 2, 1)
        self.gridLayout.addWidget(self.priceNameLabel, 3, 0)
        self.gridLayout.addWidget(self.priceLabel, 3, 1)
        for i, (p_label, p_count_label) in enumerate(self.btnObjs):
            self.gridLayout.addWidget(p_label, i+4, 0)
            self.gridLayout.addWidget(p_count_label, i+4, 1)
        self.gridLayout.addWidget(self.selSeatLabel, 8, 0)

        for btn in self.selSeats:
            self.selSeatsLayout.addWidget(btn)
        self.gridLayout.addLayout(self.selSeatsLayout, 8, 1)

        self.mainLayout.addWidget(self.checkBtn)