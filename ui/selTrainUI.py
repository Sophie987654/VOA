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


class UI_SelTrain(object):
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
            self.backBtn.clicked.connect(self.go_to_selDepDate)
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
        self.arrTitleLabel.setMaximumSize(int(w/2), int(h*0.2))
        self.arrTitleLabel.setAlignment(Qt.AlignCenter)
        self.arrTitleLabel.setStyleSheet(
            medianFont +
            "color: " + myColor.primary_text_color + ";")
        
        self.arrContLabel = QLabel(gVar.arrStat)
        self.arrContLabel.setSizePolicy(exExSP)
        self.arrContLabel.setMaximumSize(int(w/2), int(h*0.2))
        self.arrContLabel.setAlignment(Qt.AlignCenter)
        self.arrContLabel.setStyleSheet(
            largeFont +
            "color: " + myColor.primary_text_color + ";")
        
        # -------------------- 날짜 --------------------
        # datetime 객체 생성
        year = int(str(gVar.depDate)[0:4])
        month = int(str(gVar.depDate)[4:6])
        day = int(str(gVar.depDate)[6:8])
        print(year, month, day)
        date_obj = datetime(year, month, day)

        # 요일 가져오기
        day_num = date_obj.weekday()
        dayDic = {0: "월", 1: "화", 2: "수", 3: "목",
                  4: "금", 5: "토", 6: "일"}
        day_of_week = dayDic[day_num]

        self.dateLabel = QLabel(str(year) + "년 " +
                                str(month) + "월 " +
                                str(day) + "일" +
                                " (" + str(day_of_week) + ")")
        self.dateLabel.setSizePolicy(exExSP)
        self.dateLabel.setMaximumSize(w, int(h*0.1))
        self.dateLabel.setMargin(int(h*0.03))
        self.dateLabel.setAlignment(Qt.AlignCenter)
        self.dateLabel.setStyleSheet(
            largeFont +
            "color: " + myColor.secondary_text_color + ";")
        

        # ==================== 열차 표 ====================
        # 열의 데이터를 문자열로 변환 후 필요한 형식으로 슬라이싱
        self.df = self.trainDf.copy()
        self.df['arrplandtime'] = self.df['arrplandtime'].astype(str)
        self.df['arrplandtime'] = self.df['arrplandtime'].str[8:10] + ':' + self.df['arrplandtime'].str[10:12]

        self.df['depplandtime'] = self.df['depplandtime'].astype(str)
        self.df['depplandtime'] = self.df['depplandtime'].str[8:10] + ':' + self.df['depplandtime'].str[10:12]
        
        # 열 내용 변경
        self.df['arrplandtime'] = self.df['arrplandtime'] + "\n" + self.df['arrplacename'].astype(str)
        self.df['depplandtime'] = self.df['depplandtime'] + "\n" + self.df['depplacename'].astype(str)
        self.df['traingradename'] = self.df['traingradename'] + "\n" + self.df['trainno'].astype(str)
        # 불필요한 열 삭제
        self.df.drop('arrplacename', axis=1, inplace=True)
        self.df.drop('depplacename', axis=1, inplace=True)
        self.df.drop('trainno', axis=1, inplace=True)
        # 열 이름 변경
        self.df = self.df.rename(columns={'arrplandtime': '도착', 'depplandtime': '출발'})
        self.df = self.df.rename(columns={'traingradename': '열차', 'adultcharge': '요금'})
        #열 순서 변경
        self.df = self.df[['열차', '출발', '도착', '요금']]


        # -------------------- 테이블 --------------------
         # DataFrame의 열 이름을 레이블로 추가
        headerLabels = []
        for col_idx, col_name in enumerate(self.df.columns):
            headerLabel = QLabel(col_name)
            headerLabel.setSizePolicy(exExSP)
            headerLabel.setAlignment(Qt.AlignCenter)
            headerLabel.setMinimumHeight(int(h*0.1))
            headerLabel.setMaximumSize(int(w/4), int(h*0.2))
            headerLabel.setStyleSheet(
                extraLargeFont +
                "background-color: " + myColor.primary_color + ";" +
                "color: " + myColor.primary_text_color + ";" +
                "border: 1px solid " + lightGray + ";" +
                "border-radius: 0px;")
            headerLabels.append(headerLabel)

        self.trainTable = QTableWidget()
        self.trainTable.setColumnCount(len(self.df.columns))
        self.trainTable.setRowCount(len(self.df))
        self.trainTable.setSizePolicy(exExSP)
        self.trainTable.setMinimumHeight(int(h*0.6))
        
        self.trainTable.horizontalHeader().setVisible(False)
        self.trainTable.horizontalHeader().setStretchLastSection(True)
        self.trainTable.verticalHeader().setVisible(False)
        self.trainTable.verticalScrollBar().setMinimumWidth(int(h*0.03))
        self.trainTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.trainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.trainTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.trainTable.setSortingEnabled(False)
        self.trainTable.setWordWrap(True)
        
        # 헤더 높이 설정
        self.trainTable.horizontalHeader().setMinimumHeight(int(h*0.1))
        # 행 높이 설정
        self.trainTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 행 높이를 가장 큰 행에 맞게 조절
        max_row_height = max(self.trainTable.rowHeight(row) for row in range(self.trainTable.rowCount()))
        for row in range(self.trainTable.rowCount()):
            self.trainTable.setRowHeight(row, max_row_height)
        # 열 너비 설정
        self.trainTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 표 머릿글 설정
        self.trainTable.setHorizontalHeaderLabels(self.df.columns)
        # 스타일 설정
        self.trainTable.setStyleSheet(
            extraLargeFont)
        
        # DataFrame 데이터를 표에 넣기
        for i, row in self.df.iterrows():
            for j, item in enumerate(row):
                self.trainTable.setItem(i, j, QTableWidgetItem(str(item)))
        
        self.last_selected_row = -1  # 최근에 선택한 행을 저장하기 위한 변수
        
        # 행 선택 이벤트 연결
        if gVar.mode == "touch":
            self.trainTable.itemSelectionChanged.connect(self.onItemSelected)

        self.trainTable.viewport().installEventFilter(self)


        # # ==================== Footer ====================
        # # -------------------- 이전 페이지 --------------------
        # if gVar.darkMode:
        #     icon = QIcon(img_path + "offPreBtn_dark.png")
        # else:
        #     icon = QIcon(img_path + "offPreBtn.png")
        # self.preBtn = QPushButton()
        # self.preBtn.setSizePolicy(exExSP)
        # self.preBtn.setMaximumSize(int(w*0.5), int(h*0.07))
        # self.preBtn.setStyleSheet(
        #     "background-color: " + transparent + ";" +
        #     "border-color: " + transparent)
        # self.preBtn.setIcon(icon)
        # self.preBtn.setIconSize(
        #     QSize(self.preBtn.sizeHint().height(),
        #           self.preBtn.sizeHint().height()))
        # if gVar.mode == "touch":
        #     self.preBtn.clicked.connect(UI_SelTrain.clicked_preBtn)
        # elif gVar.mode == "voice":
        #     self.preBtn.installEventFilter(self)

        # # -------------------- 다음 페이지 --------------------
        # if gVar.darkMode:
        #     icon = QIcon(img_path + "nextBtn_dark.png")
        # else:
        #     icon = QIcon(img_path + "nextBtn.png")
        # self.nextBtn = QPushButton()
        # self.nextBtn.setSizePolicy(exExSP)
        # self.nextBtn.setMaximumSize(int(w*0.5), int(h*0.07))
        # self.nextBtn.setStyleSheet(
        #     "background-color: " + transparent + ";" +
        #     "border-color: " + transparent)
        # self.nextBtn.setIcon(icon)
        # self.nextBtn.setIconSize(
        #     QSize(self.nextBtn.sizeHint().height(),
        #           self.nextBtn.sizeHint().height()))
        # if gVar.mode == "touch":
        #     self.nextBtn.clicked.connect(UI_SelTrain.clicked_nextBtn)
        # elif gVar.mode == "voice":
        #     self.nextBtn.installEventFilter(self)
        
        # global GpreBtn, GnextBtn
        # GpreBtn = self.preBtn
        # GnextBtn = self.nextBtn


        # ==================== Layout ====================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.hearderLayout = QHBoxLayout(self.headerFrame)
        self.deparrLayout = QHBoxLayout()
        self.depLayout = QVBoxLayout(self.depFrame)
        self.arrLayout = QVBoxLayout(self.arrFrame)
        self.tabelHeaderLayout = QHBoxLayout()

        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.hearderLayout.setContentsMargins(
            int(w*0.01), int(h*0.01), int(w*0.01), int(h*0.01))
        
        self.deparrLayout.setAlignment(Qt.AlignCenter)
        self.deparrLayout.setContentsMargins(
            int(w*0.04), int(h*0.04), int(w*0.04), int(h*0.04))
        
        self.tabelHeaderLayout.setAlignment(Qt.AlignCenter)
        self.tabelHeaderLayout.setContentsMargins(0, 0, 0, 0)
        self.tabelHeaderLayout.setSpacing(0)

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

        self.mainLayout.addWidget(self.dateLabel)
        self.mainLayout.addLayout(self.tabelHeaderLayout)
        for col_idx, col_name in enumerate(self.df.columns):
            self.tabelHeaderLayout.addWidget(headerLabels[col_idx])
        self.mainLayout.addWidget(self.trainTable)
        

        # # 표 생성 및 설정
        # self.trainTableLayout = QGridLayout()
        # self.mainLayout.addLayout(self.trainTableLayout)

        # # DataFrame의 열 이름을 레이블로 추가
        # for col_idx, col_name in enumerate(self.df.columns):
        #     if col_idx < 6:
        #         headerLabel = QLabel(col_name)
        #         headerLabel.setSizePolicy(exExSP)
        #         headerLabel.setAlignment(Qt.AlignCenter)
        #         headerLabel.setMinimumSize(int(w/4), int(h*0.15))
        #         headerLabel.setStyleSheet(
        #             extraLargeFont +
        #             "background-color: " + myColor.primary_color + ";" +
        #             "color: " + myColor.primary_text_color + ";" +
        #             "border: 1px solid " + lightGray + ";" +
        #             "border-radius: 0px;")
        #         self.trainTableLayout.addWidget(headerLabel, 0, col_idx)

        # # DataFrame의 내용을 레이블로 추가
        # for row_idx, row in self.df.iterrows():
        #     for col_idx, value in enumerate(row):
        #         itemLabel = QLabel(str(value))
        #         itemLabel.setSizePolicy(exExSP)
        #         itemLabel.setAlignment(Qt.AlignCenter)
        #         itemLabel.setStyleSheet(
        #             extraLargeFont +
        #             "color: " + myColor.secondary_text_color + ";"
        #             "border: 1px solid " + lightGray + ";" +
        #             "border-radius: 0px;")
        #         self.trainTableLayout.addWidget(itemLabel, row_idx + 1, col_idx)

        # self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.mainLayout.addItem(self.spacer)