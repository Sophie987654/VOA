from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from settings import *

    
class UI_MainWindow(object):
    def setupUI(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        # ====================== Button ======================        
        self.buyBtn = QPushButton(self.centralwidget)
        self.buyBtn.setText("승차권 구매")
        self.buyBtn.setSizePolicy(exExSP)
        self.buyBtn.setMinimumSize(int(w*0.2), int(h*0.1))
        self.buyBtn.clicked.connect(self.go_to_selStation)
        self.buyBtn.setStyleSheet(
            extraLargeFont
        )

        self.refundBtn = QPushButton(self.centralwidget)
        self.refundBtn.setText("승차권 환불")
        self.refundBtn.setSizePolicy(exExSP)
        self.refundBtn.setMinimumSize(int(w*0.2), int(h*0.1))
        self.refundBtn.setStyleSheet(
            extraLargeFont
        )

        self.findBtn = QPushButton(self.centralwidget)
        self.findBtn.setText("예약표 찾기")
        self.findBtn.setSizePolicy(exExSP)
        self.findBtn.setMinimumSize(int(w*0.2), int(h*0.1))
        self.findBtn.setStyleSheet(
            extraLargeFont
        )

        self.cancelBtn = QPushButton(self.centralwidget)
        self.cancelBtn.setText("예약 취소")
        self.cancelBtn.setSizePolicy(exExSP)
        self.cancelBtn.setMinimumSize(int(w*0.2), int(h*0.1))
        self.cancelBtn.setStyleSheet(
            extraLargeFont
        )

        
        # ====================== Layout ======================
        self.mainLayout = QVBoxLayout(self.centralwidget)
        # -------------------- Settings --------------------
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setContentsMargins(
            int(w*0.1), int(h*0.1), int(w*0.1), int(h*0.1))
        self.mainLayout.setSpacing(int(h*0.05))
        # -------------------- Add Widgets & Layouts --------------------
        self.mainLayout.addWidget(self.buyBtn)
        self.mainLayout.addWidget(self.refundBtn)
        self.mainLayout.addWidget(self.findBtn)
        self.mainLayout.addWidget(self.cancelBtn)
    
    