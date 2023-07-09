from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_material import *
from datetime import *
import calendar

from settings import *
from src.module.TAGO import *
from src.module.TAGO_data import *


class UI_SelDepDate(object):
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
        
        self.centralwidget = QWidget(self)
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
        self.backBtn.clicked.connect(self.go_to_selStation)

        # -------------------- 처음으로 버튼 --------------------
        self.homeBtn = QPushButton()
        self.homeBtn.setMaximumSize(int(h*0.15), int(h*0.1))
        self.homeBtn.setSizePolicy(exExSP)
        self.homeBtn.setText("처음\n으로")
        self.homeBtn.setStyleSheet(
            largeFont +
            "color: " + secondary_text_color + ";"
            "background-color: " + secondary_color + ";")
        self.homeBtn.clicked.connect(self.go_to_main)
        

        # ==================== 출발 도착 ====================
        # -------------------- 출발 --------------------
        self.depFrame = QFrame()
        self.depFrame.setMaximumSize(w, int(h*0.1))
        self.depFrame.setSizePolicy(exExSP)
        self.depFrame.setStyleSheet(
            "background-color: " + secondary_color + ";"
            "border-radius: " + str(int(h*0.01)) + ";")
        
        self.depTitleLabel = QLabel("출발")
        self.depTitleLabel.setSizePolicy(exExSP)
        self.depTitleLabel.setMaximumSize(int(w/2), int(w/2))
        self.depTitleLabel.setAlignment(Qt.AlignCenter)
        self.depTitleLabel.setStyleSheet(
            medianFont +
            "color: " + secondary_text_color + ";")
        
        self.depContLabel = QLabel(gVar.depStat)
        self.depContLabel.setSizePolicy(exExSP)
        self.depContLabel.setMaximumSize(int(w/2), int(w/2))
        self.depContLabel.setAlignment(Qt.AlignCenter)
        self.depContLabel.setStyleSheet(
            largeFont +
            "color: " + secondary_text_color + ";")
        
        # -------------------- 도착 --------------------
        self.arrFrame = QFrame()
        self.arrFrame.setSizePolicy(exExSP)
        self.arrFrame.setMaximumSize(w, int(h*0.1))
        self.arrFrame.setStyleSheet(
            "background-color: " + primary_color + ";"
            "border-radius: " + str(int(h*0.01)) + ";")
        
        self.arrTitleLabel = QLabel("도착")
        self.arrTitleLabel.setSizePolicy(exExSP)
        self.arrTitleLabel.setMaximumSize(int(w/2), int(w/2))
        self.arrTitleLabel.setAlignment(Qt.AlignCenter)
        self.arrTitleLabel.setStyleSheet(
            medianFont +
            "color: " + primary_text_color + ";")
        
        self.arrContLabel = QLabel(gVar.arrStat)
        self.arrContLabel.setSizePolicy(exExSP)
        self.arrContLabel.setMaximumSize(int(w/2), int(w/2))
        self.arrContLabel.setAlignment(Qt.AlignCenter)
        self.arrContLabel.setStyleSheet(
            largeFont +
            "color: " + primary_text_color + ";")


        # ==================== 날짜 선택 ====================
        # -------------------- 달력 --------------------
        # -------------------- 헤더 & 사전 준비 --------------------
        self.calHeaderFrame = QFrame()
        self.calHeaderFrame.setSizePolicy(exExSP)
        self.calHeaderFrame.maximumHeight = (int(h*0.1))

        self.calHeaderLabel = QLabel("출발일")
        self.calHeaderLabel.setSizePolicy(exExSP)
        self.calHeaderLabel.setAlignment(Qt.AlignCenter)
        self.calHeaderLabel.setStyleSheet(
            medianFont +
            "color: " + secondary_text_color + ";")

        # 현재 날짜와 시각 구하기
        now = datetime.now()
        # 형식 지정하여 날짜와 시각 출력
        YMD = now.strftime("%Y년 %m월 %d일")
        day_num = now.weekday()
        dayDic = {0: "월", 1: "화", 2: "수", 3: "목",
                  4: "금", 5: "토", 6: "일"}
        day = dayDic[day_num]
        HM = now.strftime("%H:%M")
        currentDT = YMD + " (" + day + "요일) " + HM
        self.calSelDTLabel = QLabel(currentDT)
        self.calSelDTLabel.setSizePolicy(exExSP)
        self.calSelDTLabel.setAlignment(Qt.AlignCenter)
        self.calSelDTLabel.setStyleSheet(
            largeFont +
            "color: " + secondary_text_color + ";")
        
        # -------------------- 요일 --------------------
        self.day_1 = QLabel()
        self.day_2 = QLabel()
        self.day_3 = QLabel()
        self.day_4 = QLabel()
        self.day_5 = QLabel()
        self.day_6 = QLabel()

        self.dayLabel = [self.day_1, self.day_2, self.day_3,
                     self.day_4, self.day_5, self.day_6]

        for i in range(0, 6):
            self.dayLabel[i].setText(dayDic[(day_num + i) % 7])
            self.dayLabel[i].setSizePolicy(exExSP)
            self.dayLabel[i].setMaximumSize(int(h*0.08), int(h*0.05))
            self.dayLabel[i].setAlignment(Qt.AlignCenter)

            if (day_num + i) % 7 == 6:
                self.dayLabel[i].setStyleSheet(
                    largeFont +
                    "color: " + red + ";")
            elif (day_num + i) % 7 == 5:
                self.dayLabel[i].setStyleSheet(
                    largeFont +
                    "color: " + lightBlue + ";")
            else:
                self.dayLabel[i].setStyleSheet(
                    largeFont +
                    "color: " + secondary_text_color + ";")

        # -------------------- 일 --------------------
        self.date_1 = QPushButton()
        self.date_2 = QPushButton()
        self.date_3 = QPushButton()
        self.date_4 = QPushButton()
        self.date_5 = QPushButton()
        self.date_6 = QPushButton()

        self.dateBtn = [self.date_1, self.date_2, self.date_3,
                    self.date_4, self.date_5, self.date_6]

        # 현재 날짜와 최대 일자를 얻어옴
        now = datetime.now()
        max_day = calendar.monthrange(now.year, now.month)[1]

        # 출력할 범위 설정
        start_day = now.day
        
        for i in range(0, 6):
            self.dateBtn[i].setText(str((start_day + i) % max_day).zfill(2))
            self.dateBtn[i].setCheckable(True)
            self.dateBtn[i].setSizePolicy(exExSP)
            self.dateBtn[i].setMaximumSize(int(h*0.08), int(h*0.08))
            self.dateBtn[i].setStyleSheet(
                largeFont)
            self.dateBtn[i].clicked.connect(UI_SelDepDate.clicked_dateBtn)
        
        self.date_1.setText(str((start_day + i) % max_day).zfill(2) +
                                     "\n출발일")
        self.date_1.setStyleSheet(
            largeFont +
            "color: " + primary_text_color + ";" +
            "background-color: " + primary_color + ";")
        

        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.hearderLayout = QHBoxLayout(self.headerFrame)
        self.deparrLayout = QHBoxLayout()
        self.depLayout = QVBoxLayout(self.depFrame)
        self.arrLayout = QVBoxLayout(self.arrFrame)
        self.calenderLayout = QVBoxLayout()
        self.calHeaderLayout = QVBoxLayout(self.calHeaderFrame)
        self.gridLayout = QGridLayout()

        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.hearderLayout.setContentsMargins(
            int(w*0.01), int(h*0.01), int(w*0.01), int(h*0.01))
        
        self.deparrLayout.setAlignment(Qt.AlignCenter)
        self.deparrLayout.setContentsMargins(
            int(w*0.05), int(h*0.05), int(w*0.05), int(h*0.05))
        
        self.calenderLayout.setAlignment(Qt.AlignCenter)
        self.calenderLayout.setContentsMargins(0, 0, 0, 0)
        self.calHeaderLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.setAlignment(Qt.AlignCenter)
        self.gridLayout.setContentsMargins(
            int(w*0.02), int(h*0.02), int(w*0.02), int(h*0.02))
        self.gridLayout.setSpacing(int(w*0.01))

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

        self.mainLayout.addLayout(self.calenderLayout)
        self.calenderLayout.addWidget(self.calHeaderFrame)
        self.calHeaderLayout.addWidget(self.calHeaderLabel)
        self.calHeaderLayout.addWidget(self.calSelDTLabel)
        self.calenderLayout.addLayout(self.gridLayout)
        
        for i in range(0, 6):
            self.gridLayout.addWidget(self.dayLabel[i], 0, i, 1, 1)
        for i in range(0, 6):
            self.gridLayout.addWidget(self.dateBtn[i], 1, i, 1, 1)

    