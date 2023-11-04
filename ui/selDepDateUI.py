from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_material import *
from datetime import *
import calendar
from functools import partial

from settings import *
from src.module.tts import *
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
        self.centralwidget.installEventFilter(self)  # eventFilter를 central_widget에 설치
        
        # ==================== Header ====================
        self.headerFrame = QFrame()
        self.headerFrame.setMaximumSize(w, int(h*0.1))
        self.headerFrame.setSizePolicy(exExSP)
        self.headerFrame.setStyleSheet(
            "background-color: " + myColor.primary_color + ";")
        
        self.headerLabel = QLabel("승차권 예매")
        self.headerLabel.setSizePolicy(exExSP)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headerLabel.setStyleSheet(
            extraLargeFont +
            "color: " + myColor.primary_text_color + ";")
        
        # -------------------- 뒤로가기 버튼 --------------------
        self.backBtn = QPushButton()
        self.backBtn.setFixedSize(int(h*0.15), int(h*0.08))
        self.backBtn.setSizePolicy(exExSP)
        self.backBtn.setText("뒤로\n가기")
        self.backBtn.setStyleSheet(
            largeFont +
            "color: " + myColor.secondary_text_color + ";"
            "background-color: " + myColor.secondary_color + ";")
        if gVar.mode == "touch":
            self.backBtn.clicked.connect(self.go_to_selStation)
        elif gVar.mode == "voice":
            self.backBtn.installEventFilter(self)

        # -------------------- 처음으로 버튼 --------------------
        self.homeBtn = QPushButton()
        self.homeBtn.setFixedSize(int(h*0.15), int(h*0.08))
        self.homeBtn.setSizePolicy(exExSP)
        self.homeBtn.setText("처음\n으로")
        self.homeBtn.setStyleSheet(
            largeFont +
            "color: " + myColor.secondary_text_color + ";"
            "background-color: " + myColor.secondary_color + ";")
        if gVar.mode == "touch":
            self.homeBtn.clicked.connect(self.go_to_main)
        elif gVar.mode == "voice":
            self.homeBtn.installEventFilter(self)


        # ==================== 출발 도착 ====================
        # -------------------- 출발 --------------------
        self.depFrame = QFrame()
        self.depFrame.setSizePolicy(exExSP)
        self.depFrame.setMaximumSize(w, int(h*0.1))
        self.depFrame.setStyleSheet(
            "background-color: " + myColor.secondary_color + ";"
            "border-radius: " + str(int(h*0.01)) + ";")
        
        self.depTitleLabel = QLabel("출발")
        self.depTitleLabel.setSizePolicy(exExSP)
        self.depTitleLabel.setMaximumSize(int(w/2), int(w/2))
        self.depTitleLabel.setAlignment(Qt.AlignCenter)
        self.depTitleLabel.setStyleSheet(
            medianFont +
            "color: " + myColor.secondary_text_color + ";")
        
        self.depContLabel = QLabel(gVar.depStat)
        self.depContLabel.setSizePolicy(exExSP)
        self.depContLabel.setMaximumSize(int(w/2), int(w/2))
        self.depContLabel.setAlignment(Qt.AlignCenter)
        self.depContLabel.setStyleSheet(
            largeFont +
            "color: " + myColor.secondary_text_color + ";")
        
        # -------------------- 도착 --------------------
        self.arrFrame = QFrame()
        self.arrFrame.setSizePolicy(exExSP)
        self.arrFrame.setMaximumSize(w, int(h*0.1))
        self.arrFrame.setStyleSheet(
            "background-color: " + myColor.primary_color + ";"
            "border-radius: " + str(int(h*0.01)) + ";")
        
        self.arrTitleLabel = QLabel("도착")
        self.arrTitleLabel.setSizePolicy(exExSP)
        self.arrTitleLabel.setMaximumSize(int(w/2), int(w/2))
        self.arrTitleLabel.setAlignment(Qt.AlignCenter)
        self.arrTitleLabel.setStyleSheet(
            medianFont +
            "color: " + myColor.primary_text_color + ";")
        
        self.arrContLabel = QLabel(gVar.arrStat)
        self.arrContLabel.setSizePolicy(exExSP)
        self.arrContLabel.setMaximumSize(int(w/2), int(w/2))
        self.arrContLabel.setAlignment(Qt.AlignCenter)
        self.arrContLabel.setStyleSheet(
            largeFont +
            "color: " + myColor.primary_text_color + ";")


        # ==================== 날짜 선택 ====================
        # -------------------- 달력 --------------------
        # -------------------- 헤더 & 사전 준비 --------------------
        self.calHeaderFrame = QFrame()
        self.calHeaderFrame.setSizePolicy(exExSP)
        self.calHeaderFrame.maximumHeight = (int(h*0.1))
        self.calHeaderFrame.setContentsMargins(0, int(h*0.04), 0, int(h*0.04))

        self.calHeaderLabel = QLabel("출발일")
        self.calHeaderLabel.setSizePolicy(exExSP)
        self.calHeaderLabel.setAlignment(Qt.AlignCenter)
        self.calHeaderLabel.setStyleSheet(
            medianFont +
            "color: " + myColor.secondary_text_color + ";")

        # 현재 날짜와 시각 구하기
        today = datetime.now()
        
        # 형식 지정하여 날짜와 시각 출력
        YMD = today.strftime("%Y년 %m월 %d일")
        day_num = today.weekday()
        dayDic = {0: "월", 1: "화", 2: "수", 3: "목",
                  4: "금", 5: "토", 6: "일"}
        day = dayDic[day_num]
        HM = today.strftime("%H:%M")
        currentDT = YMD + " (" + day + "요일) " + HM
        UI_SelDepDate.calSelDTLabel = QLabel(currentDT)
        UI_SelDepDate.calSelDTLabel.setSizePolicy(exExSP)
        UI_SelDepDate.calSelDTLabel.setAlignment(Qt.AlignCenter)
        UI_SelDepDate.calSelDTLabel.setStyleSheet(
            largeFont +
            "color: " + myColor.secondary_text_color + ";")
        
        # -------------------- 요일 --------------------
        self.dayLabels = []

        for i in range(6):
            self.dayLabel = QLabel(dayDic[(day_num + i) % 7])
            self.dayLabel.setSizePolicy(exExSP)
            self.dayLabel.setMinimumSize(int(h*0.1), int(h*0.05))
            self.dayLabel.setAlignment(Qt.AlignCenter)
            self.dayLabels.append(self.dayLabel)

            if (day_num + i) % 7 == 6:
                self.dayLabel.setStyleSheet(
                    largeFont +
                    "color: " + red + ";")
            elif (day_num + i) % 7 == 5:
                self.dayLabel.setStyleSheet(
                    largeFont +
                    "color: " + lightBlue + ";")
            else:
                self.dayLabel.setStyleSheet(
                    largeFont +
                    "color: " + myColor.secondary_text_color + ";")

        # -------------------- 일 --------------------
        UI_SelDepDate.dateBtns = []
        
        self.dateBtnGroup = QButtonGroup()
        for i in range(6):
            self.dateBtn = QPushButton(str((today + timedelta(days=i)).day).zfill(2))
            self.dateBtn.setSizePolicy(exExSP)
            self.dateBtn.setMinimumSize(int(h*0.1), int(h*0.1))
            self.dateBtn.setStyleSheet(
                largeFont +
                "border-radius: 10px;")
            UI_SelDepDate.dateBtns.append(self.dateBtn)
            self.dateBtnGroup.addButton(self.dateBtn)
            if gVar.mode == "touch":
                self.dateBtn.setCheckable(True)
                self.dateBtn.clicked.connect(UI_SelDepDate.clicked_dateBtn)
            elif gVar.mode == "voice":
                self.dateBtn.installEventFilter(self)

        UI_SelDepDate.selected_date = today
        UI_SelDepDate.dateBtns[0].setText(str(today.day)
                                          + "\n출발일")
        UI_SelDepDate.dateBtns[0].setStyleSheet(
            largeFont +
            "color: " + myColor.primary_text_color + ";" +
            "background-color: " + myColor.primary_color + ";" +
            "border-radius: 10px;" +
            "padding: 10px 30px 10px 10px;")
        gVar.depDate = datetime.today().strftime("%Y%m") + str(today.day).zfill(2)
        print(gVar.depDate)
        
        # -------------------- 시간 --------------------
        UI_SelDepDate.timeScrollArea = QScrollArea()
        UI_SelDepDate.timeScrollArea.setObjectName = "timeScrollArea"
        UI_SelDepDate.timeScrollArea.setSizePolicy(exExSP)
        UI_SelDepDate.timeScrollArea.setMaximumWidth(w)
        UI_SelDepDate.timeScrollArea.setMinimumHeight(int(h*0.12))
        UI_SelDepDate.timeScrollArea.setWidgetResizable(True)
        UI_SelDepDate.timeScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # UI_SelDepDate.timeScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.timeScrollContent = QWidget()
        UI_SelDepDate.timeScrollArea.setWidget(self.timeScrollContent)

        UI_SelDepDate.timeBtns = []
        UI_SelDepDate.timeBtnGroup = QButtonGroup()
        for i in range(24):
            self.timeBtn = QPushButton(str(i).zfill(2) + "시")
            self.timeBtn.setSizePolicy(exExSP)
            self.timeBtn.setMinimumSize(int(h*0.1), int(h*0.1))
            self.timeBtn.setStyleSheet(
                largeFont +
                "font-weight: bold;" +
                "border: none;")
            UI_SelDepDate.timeBtns.append(self.timeBtn)
            UI_SelDepDate.timeBtnGroup.addButton(self.timeBtn, i)
            self.timeBtn.installEventFilter(self)
            if gVar.mode == "touch":
                self.timeBtn.setCheckable(True)
                self.timeBtn.clicked.connect(UI_SelDepDate.clicked_timeBtn)
                
        UI_SelDepDate.timeBtns[today.hour].setText(str(today.hour).zfill(2) + "시")
        UI_SelDepDate.timeBtns[today.hour].setStyleSheet(
            largeFont +
            "font-weight: bold;" +
            "background-color: " + myColor.primary_color + ";" +
            "color: " + myColor.primary_text_color + ";")
        gVar.depTime = str(today.hour).zfill(2) + "00"
        print(gVar.depTime)
        
        # -------------------- 조회 --------------------
        self.searchBtn = QPushButton("조회")
        self.searchBtn.setSizePolicy(exExSP)
        self.searchBtn.setMinimumSize(int(h*0.2), int(h*0.1))
        self.searchBtn.setStyleSheet(
            extraLargeFont +
            "border-radius: 10px;" + 
            "margin: 20px 20px 20px 20px;")
        if gVar.mode == "touch":
            self.searchBtn.clicked.connect(self.go_to_selTrain)
        elif gVar.mode == "voice":
            self.searchBtn.installEventFilter(self)

        
        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.hearderLayout = QHBoxLayout(self.headerFrame)
        self.deparrLayout = QHBoxLayout()
        self.depLayout = QVBoxLayout(self.depFrame)
        self.arrLayout = QVBoxLayout(self.arrFrame)
        self.calenderLayout = QVBoxLayout()
        self.calHeaderLayout = QVBoxLayout(self.calHeaderFrame)
        self.gridLayout = QGridLayout()
        self.timeScrollLayout = QHBoxLayout(self.timeScrollContent)

        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.hearderLayout.setContentsMargins(
            int(w*0.01), int(h*0.01), int(w*0.01), int(h*0.01))
        
        self.deparrLayout.setAlignment(Qt.AlignCenter)
        self.deparrLayout.setContentsMargins(
            int(w*0.04), int(h*0.04), int(w*0.04), int(h*0.04))
        
        self.calenderLayout.setAlignment(Qt.AlignCenter)
        self.calenderLayout.setContentsMargins(0, 0, 0, int(h*0.1))
        self.calenderLayout.setSpacing(0)
        self.calHeaderLayout.setContentsMargins(0, 0, 0, 0)
        
        self.gridLayout.setAlignment(Qt.AlignCenter)
        self.gridLayout.setContentsMargins(
            int(w*0.02), int(h*0.02), int(w*0.02), int(h*0.02))
        self.gridLayout.setSpacing(int(w*0.01))

        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.timeScrollLayout.setSpacing(0)

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
        self.calHeaderLayout.addWidget(UI_SelDepDate.calSelDTLabel)
        self.calenderLayout.addLayout(self.gridLayout)
        for i in range(0, 6):
            self.gridLayout.addWidget(self.dayLabels[i], 0, i, 1, 1)
        for i in range(0, 6):
            self.gridLayout.addWidget(UI_SelDepDate.dateBtns[i], 1, i, 1, 1)
        
        self.calenderLayout.addWidget(UI_SelDepDate.timeScrollArea)
        for i in range(24):
            self.timeScrollLayout.addWidget(UI_SelDepDate.timeBtns[i])
        
        self.calenderLayout.addWidget(self.searchBtn)

        # self.mainLayout.addItem(self.spacer)

    def clicked_dateBtn(self):
        # 현재 날짜와 최대 일자를 얻어옴
        today = datetime.today()
        
        for i, btn in enumerate(UI_SelDepDate.dateBtns):
            if btn.isChecked():
                btn.setText(str((today + timedelta(days=i)).day).zfill(2) + "\n출발일")
                btn.setStyleSheet(
                    largeFont +
                    "background-color: " + myColor.primary_color + ";" +
                    "color: " + myColor.secondary_color + ";" +
                    "border-radius: 10px;"
                )
                gVar.depDate = datetime.today().strftime("%Y%m") + btn.text().split("\n")[0]
                print(gVar.depDate)

                today = datetime.today()
                UI_SelDepDate.selected_date = today + timedelta(days=i)
                YMD = UI_SelDepDate.selected_date.strftime("%Y년 %m월 %d일")
                day_num = UI_SelDepDate.selected_date.weekday()
                dayDic = {0: "월", 1: "화", 2: "수", 3: "목",
                            4: "금", 5: "토", 6: "일"}
                day = dayDic[day_num]
                HM = datetime.now().strftime("%H:%M")
                currentDT = YMD + " (" + day + "요일) " + gVar.depTime[:-2] + ":00"
                UI_SelDepDate.calSelDTLabel.setText(currentDT)
                
            else:
                btn.setText(str((today + timedelta(days=i)).day).zfill(2))

                btn.setStyleSheet(
                    largeFont +
                    "background-color: " + transparent + ";" +
                    "color: " + myColor.primary_color + ";" +
                    "border-radius: 10px;"
                )

    def clicked_timeBtn(self):
        for i, btn in enumerate(UI_SelDepDate.timeBtns):
            if UI_SelDepDate.selected_date.day == datetime.today().day:
                if btn.isChecked():
                    if i < datetime.today().hour:
                        btn.setChecked(False)
                        btn.setStyleSheet(
                            largeFont +
                            "background-color: " + transparent + ";" +
                            "color: " + myColor.primary_color + ";"
                            "border: none;"
                        )
                        
                        pyTTS("지나간 시간은 선택할 수 없습니다.")
                        break
                    else:
                        btn.setStyleSheet(
                            largeFont +
                            "background-color: " + myColor.primary_color + ";" +
                            "color: " + myColor.secondary_color + ";"
                            "border: none;"
                        )
                        gVar.depTime = btn.text().split("시")[0] + "00"
                        print(gVar.depTime)

                        currentDT = UI_SelDepDate.calSelDTLabel.text()[:-6]
                        UI_SelDepDate.calSelDTLabel.setText(currentDT + " " + btn.text()[:-1] + ":00")
                else:
                    btn.setStyleSheet(
                        largeFont +
                        "background-color: " + transparent + ";" +
                        "color: " + myColor.primary_color + ";"
                        "border: none;"
                    )
            else:
                if btn.isChecked():
                    btn.setStyleSheet(
                        largeFont +
                        "background-color: " + myColor.primary_color + ";" +
                        "color: " + myColor.secondary_color + ";"
                        "border: none;"
                    )
                    gVar.depTime = btn.text().split("시")[0] + "00"
                    print(gVar.depTime)

                    currentDT = UI_SelDepDate.calSelDTLabel.text()[:-6]
                    UI_SelDepDate.calSelDTLabel.setText(currentDT + " " + btn.text()[:-1] + ":00")
                else:
                    btn.setStyleSheet(
                        largeFont +
                        "background-color: " + transparent + ";" +
                        "color: " + myColor.primary_color + ";"
                        "border: none;"
                    )