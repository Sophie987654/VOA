import pyautogui

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from settings import *
from src.module.TAGO import *
from src.module.TAGO_data import *


class UI_SelStation(object):
    def setupUI(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # ==================== Header ====================
        self.headerFrame = QFrame()
        self.headerFrame.setMaximumSize(w, int(h*0.1))
        self.headerFrame.setSizePolicy(exExSP)
        self.headerFrame.setStyleSheet(
            "background-color: " + blue + ";")

        self.headerLabel = QLabel("승차권 예매")
        self.headerLabel.setSizePolicy(exExSP)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setStyleSheet(
            extraLargeFont +
            "color: " + white + ";"
        )
        
        
        # -------------------- 뒤로가기 버튼 --------------------
        self.backBtn = QPushButton()
        self.backBtn.setMaximumSize(int(w/30), int(w/30))
        self.backBtn.setText("뒤로\n가기")
        self.backBtn.setStyleSheet(
            medianFont +
            "color: " + black + ";" +
            "background-color: " + white + ";")
        self.backBtn.clicked.connect(self.go_to_main)
        # -------------------- 처음으로 버튼 --------------------
        self.homeBtn = QPushButton()
        self.homeBtn.setMaximumSize(int(w/30), int(w/30))
        self.homeBtn.setText("처음\n으로")
        self.homeBtn.setStyleSheet(
            medianFont +
            "color: " + black + ";" +
            "background-color: " + white + ";")
        self.homeBtn.clicked.connect(self.go_to_main)
        
        # ==================== 출발 도착 ====================
        # -------------------- 출발 --------------------
        self.depFrame = QFrame()
        self.depFrame.setMaximumSize(w, int(h*0.1))
        self.depFrame.setSizePolicy(exExSP)
        self.depFrame.setStyleSheet(
            "background-color: " + white + ";"
            "border-radius: " + str(int(h*0.01)) + ";")
        
        self.depTitleLabel = QLabel("출발")
        self.depTitleLabel.setSizePolicy(exExSP)
        self.depTitleLabel.setMaximumSize(int(w/2), int(w/2))
        self.depTitleLabel.setAlignment(Qt.AlignCenter)
        self.depTitleLabel.setStyleSheet(
            smallFont +
            "color: " + lightGray + ";")
        
        self.depContLabel = QLabel("서울")
        self.depContLabel.setSizePolicy(exExSP)
        self.depContLabel.setMaximumSize(int(w/2), int(w/2))
        self.depContLabel.setAlignment(Qt.AlignCenter)
        self.depContLabel.setStyleSheet(
            largeFont)
        
        # -------------------- 도착 --------------------
        self.arrFrame = QFrame()
        self.arrFrame.setMaximumSize(w, int(h*0.1))
        self.arrFrame.setSizePolicy(exExSP)
        self.arrFrame.setStyleSheet(
            "background-color: " + blue + ";"
            "border-radius: " + str(int(h*0.01)) + ";")
        
        self.arrTitleLabel = QLabel("도착")
        self.arrTitleLabel.setSizePolicy(exExSP)
        self.arrTitleLabel.setMaximumSize(int(w/2), int(w/2))
        self.arrTitleLabel.setAlignment(Qt.AlignCenter)
        self.arrTitleLabel.setStyleSheet(
            smallFont +
            "color: " + lightGray + ";")
        
        self.arrContLabel = QLabel("부산")
        self.arrContLabel.setSizePolicy(exExSP)
        self.arrContLabel.setMaximumSize(int(w/2), int(w/2))
        self.arrContLabel.setAlignment(Qt.AlignCenter)
        self.arrContLabel.setStyleSheet(
            largeFont +
            "color: " + white + ";")
        

        # ==================== 역 선택 ====================
        self.selStat_1 = QtWidgets.QPushButton()
        self.selStat_2 = QtWidgets.QPushButton()
        self.selStat_3 = QtWidgets.QPushButton()
        self.selStat_4 = QtWidgets.QPushButton()
        self.selStat_5 = QtWidgets.QPushButton()
        self.selStat_6 = QtWidgets.QPushButton()
        self.selStat_7 = QtWidgets.QPushButton()
        self.selStat_8 = QtWidgets.QPushButton()
        self.selStat_9 = QtWidgets.QPushButton()
        self.selStat_10 = QtWidgets.QPushButton()
        self.selStat_11 = QtWidgets.QPushButton()
        self.selStat_12 = QtWidgets.QPushButton()
        self.selStat_13 = QtWidgets.QPushButton()
        self.selStat_14 = QtWidgets.QPushButton()
        self.selStat_15 = QtWidgets.QPushButton()

        global selStat
        selStat = [
            [self.selStat_1, self.selStat_2, self.selStat_3],
            [self.selStat_4, self.selStat_5, self.selStat_6],
            [self.selStat_7, self.selStat_8, self.selStat_9],
            [self.selStat_10 , self.selStat_11, self.selStat_12],
            [self.selStat_13, self.selStat_14, self.selStat_15]]

        for i in range(0, 5):
            for j in range(0, 3):
                selStat[i][j].setText(impStat[i][j])
                selStat[i][j].setSizePolicy(exExSP)
                selStat[i][j].setMaximumSize(
                    int(w*0.8), int(h*0.8))
                selStat[i][j].setStyleSheet(
                largeFont)

        # ==================== Footer ====================
        # -------------------- 이전 페이지 --------------------
        icon = QIcon(img_path + "offPreBtn.png")
        self.preBtn = QPushButton()
        self.preBtn.setSizePolicy(exExSP)
        self.preBtn.setMaximumSize(int(w*0.5), int(h*0.07))
        self.preBtn.setStyleSheet(
            "background-color: " + transparent + ";" +
            "border-color: " + transparent)
        self.preBtn.setIcon(icon)
        self.preBtn.setIconSize(
            QSize(self.preBtn.sizeHint().height(),
                  self.preBtn.sizeHint().height()))
        self.preBtn.clicked.connect(UI_SelStation.clicked_preBtn)
        
        # -------------------- 다음 페이지 --------------------
        icon = QIcon(img_path + "nextBtn.png")
        self.nextBtn = QPushButton()
        self.nextBtn.setSizePolicy(exExSP)
        self.nextBtn.setMaximumSize(int(w*0.5), int(h*0.07))
        self.nextBtn.setStyleSheet(
            "background-color: " + transparent + ";" +
            "border-color: " + transparent)
        self.nextBtn.setIcon(icon)
        self.nextBtn.setIconSize(
            QSize(self.nextBtn.sizeHint().height(),
                  self.nextBtn.sizeHint().height()))
        self.nextBtn.clicked.connect(UI_SelStation.clicked_nextBtn)

        global GpreBtn, GnextBtn
        GpreBtn = self.preBtn
        GnextBtn = self.nextBtn
        
        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.hearderLayout = QHBoxLayout(self.headerFrame)
        self.deparrLayout = QHBoxLayout()
        self.depLayout = QVBoxLayout(self.depFrame)
        self.arrLayout = QVBoxLayout(self.arrFrame)
        self.gridLayout = QtWidgets.QGridLayout()
        self.footerLayout = QHBoxLayout()

        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.hearderLayout.setContentsMargins(
            int(w*0.01), int(h*0.01), int(w*0.01), int(h*0.01))
        
        self.deparrLayout.setAlignment(Qt.AlignCenter)
        self.deparrLayout.setContentsMargins(
            int(w*0.05), int(h*0.05), int(w*0.05), int(h*0.05))
        
        self.gridLayout.setContentsMargins(
            int(w*0.02), int(h*0.02), int(w*0.02), int(h*0.02))
        self.gridLayout.setSpacing(int(w*0.01))

        self.footerLayout.setContentsMargins(
            int(w*0.01), int(h*0.01), int(w*0.01), int(h*0.01)
        )
        self.footerLayout.setSpacing(int(w*0.01))

        # -------------------- Add Widgets & Layouts --------------------
        self.mainLayout.addWidget(self.headerFrame)

        self.hearderLayout.addWidget(self.backBtn)
        self.hearderLayout.addWidget(self.headerLabel)
        self.hearderLayout.addWidget(self.homeBtn)
        
        self.mainLayout.addLayout(self.deparrLayout)
        self.deparrLayout.addWidget(self.depFrame)
        self.depLayout.addWidget(self.depTitleLabel)
        self.depLayout.addWidget(self.depContLabel)
        self.deparrLayout.addWidget(self.arrFrame)     
        self.arrLayout.addWidget(self.arrTitleLabel)
        self.arrLayout.addWidget(self.arrContLabel)

        self.mainLayout.addLayout(self.gridLayout)
        for i in range(0, 5):
            for j in range(0, 3):
                self.gridLayout.addWidget(
                    selStat[i][j], i, j)
                
        self.mainLayout.addLayout(self.footerLayout)
        self.footerLayout.addWidget(self.preBtn)
        self.footerLayout.addWidget(self.nextBtn)
    

    global page
    page = 1

    def clicked_preBtn(self):
        global GpreBtn, GnextBtn, page

        if page == 2:
            icon = QIcon(img_path + "offPreBtn.png")
            GpreBtn.setIcon(icon)

            for i in range(0, 5):
                for j in range(0, 3):
                    selStat[i][j].setText(impStat[i][j])
            
            page = 1
        elif page == 3:
            icon = QIcon(img_path + "nextBtn.png")
            GnextBtn.setIcon(icon)

            for i in range(0, 5):
                for j in range(0, 3):
                    selStat[i][j].setText(impStat[i+5][j])
            
            page = 2

    def clicked_nextBtn(self):
        global GpreBtn, GnextBtn
        global selStat, page
        
        if page == 1:
            icon = QIcon(img_path + "PreBtn.png")
            GpreBtn.setIcon(icon)

            for i in range(0, 5):
                for j in range(0, 3):
                    selStat[i][j].setText(impStat[i+5][j])
            
            page = 2
        elif page == 2:
            for i in range(0, 5):
                for j in range(0, 3):
                    if (impStat[i+10][j] == ""):
                        selStat[i][j].setText("")
                    else:
                        selStat[i][j].setText(impStat[i+10][j])
            
            icon = QIcon(img_path + "offNextBtn.png")
            GnextBtn.setIcon(icon)

            page = 3