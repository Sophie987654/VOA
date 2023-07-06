import sys, datetime, cv2, winsound

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_material import *
from datetime import *
from whisper_mic.whisper_mic import WhisperMic
from konlpy.tag import Okt

from settings import *
from src.module.face_detection import *
from src.module.TAGO_data import *
from ui.mainUI import UI_MainWindow
from ui.selStationUI import UI_SelStation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # setup stylesheet
        # See this link for more information. -> https://pypi.org/project/qt-material/
        extra = {
            'font_family': '나눔고딕'
        }
        apply_stylesheet(app, theme='light_blue.xml',
                         invert_secondary=True, extra=extra)
        stylesheet = app.styleSheet()
        with open('src/theme/my_theme.css') as file:
            app.setStyleSheet(stylesheet + file.read().format(**os.environ))
        
        UI_MainWindow.setupUI(self)
        # self.showFullScreen()
        self.show()

        while True:
            if gVar.locateSelf:
                self.timer = QTimer()
                self.timer.timeout.connect(self.repeatThis)
                self.timer.start(10000)
            
            if (self.startCam()):
                if gVar.currentP == "main":
                    gVar.locateSelf = False
                    self.timer.stop()
                    gVar.currentP = "selStation"

                    if gVar.menu == 1:
                        self.setCentralWidget(None)
                        UI_SelStation.setupUI(self)
                        gVar.currentP = "selStation"
            else:
                pass
            
    def closeEvent(self, event):
        UI_MainWindow.cap.release()
        sys.exit()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            print("터치")
            if gVar.currentP == "main":
                if gVar.pause == 1: # 음성안내 종료
                    pyTTS("음성안내를 종료합니다.")
                    gVar.pause = -1
                elif gVar.pause == 2:
                    gVar.menu = 2
            elif gVar.currentP == "selStation":
                if gVar.pause == 1:
                    gVar.pause = 2
                
    
    def repeatThis(self):
        pyTTS("음성안내 기능이 있는 키오스크 입니다.")
        gVar.locateSelf = False

    def delay(self):
        self.now = datetime.now()
        if gVar.pause == -1:
            self.later = self.now + timedelta(seconds=20)
        else:
            self.later = self.now + timedelta(seconds=3)
    
    def go_to_main(self):
        gVar.gVarInit()
        gVar.face_cnt = -160

        self.setCentralWidget(None)
        UI_MainWindow.setupUI(self)

    def go_to_selStation(self):
        gVar.mode = "touch"
        gVar.locateSelf = False
        self.timer.stop()
        gVar.currentP = "selStation"

        self.setCentralWidget(None)
        UI_SelStation.setupUI(self)

    def startCam(self):
        # Camera preparation ###############################################################
        UI_MainWindow.cap = cv2.VideoCapture(0)
        camOff = False
        startAgain = 0

        while UI_MainWindow.cap.isOpened():
            # Process Key (ESC: end) #################################################
            key = cv2.waitKey(10)
            if key == 27:  # ESC
                break

            # Camera capture #####################################################
            ret, image = UI_MainWindow.cap.read()
            if not ret:
                break
            image = cv2.flip(image, 1)  # Mirror display

            # Detection implementation #############################################################
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            image.flags.writeable = True

            if (faceDetection(image) == False):
                self.go_to_main()
                text = "자리 비움이 감지되어 처음으로 돌아갑니다."
                pyTTS(text)
                return False

            if gVar.currentP == "main":
                if gVar.pause == -1:
                    if (faceDetection(image)):
                        startAgain += 1
                        if startAgain == 3:
                            gVar.pause = 0
                
                if gVar.pause == 0:
                    if (faceDetection(image)):
                        gVar.locateSelf = False
                        self.timer.stop()

                        text = "음성안내를 시작합니다. 음성안내를 원하지 않으면 화면을 터치해주세요."
                        pyTTS(text)
                        gVar.pause = 1
                        self.delay()

                if gVar.pause == 1:
                    if datetime.now() >= self.later:
                        text = "승차권 구매를 시작합니다. 구매가 아니라 승차권 환불, 예약표 찾기, 예약 취소를 원하시면 화면을 터치해주세요."
                        pyTTS(text)
                        gVar.pause = 2
                        self.delay()

                if gVar.pause == 2:
                    if datetime.now() >= self.later:
                        gVar.pause = 0
                        return True
            elif gVar.currentP == "selStation" and gVar.mode == "voice":
                if gVar.pause == 0:
                    if gVar.firstAsk:
                        pyTTS("지금부터 승차권 예매를 시작합니다. 삐이이 소리 후 도착역을 말씀해주세요.")
                        gVar.firstAsk = False
                    else:
                        pyTTS("삐이이 소리 후 다시 말씀해주세요.")
                    
                    self.mic = WhisperMic('small')
                    frequency = 500  # 소리의 주파수 (Hz)
                    duration = 500  # 소리의 지속 시간 (밀리초)
                    winsound.Beep(frequency, duration)
                    result = self.mic.listen()
                    print(result)

                    okt = Okt()
                    pos = okt.nouns(result)
                    print(pos)

                    for n in pos:
                        if n.endswith("역"):
                            n = n[:-1]

                        if n in station:
                            print(n + "역 있음")
                            gVar.station = n
                            
                            pyTTS(n + "역이 맞으면 화면을 터치해주세요.")
                            gVar.pause = 1

                            self.arrContLabel.setText(n)

                            self.delay()                                
                            break

                if datetime.now() >= self.later:
                    if gVar.pause == 2:
                        pyTTS(n + "역을 선택하셨습니다.")
                        gVar.currentP = "selDate"
                    else:
                        gVar.pause = 0
    def leave(self):
        self.go_to_main()
        text = "자리 비움이 감지되어 처음으로 돌아갑니다."
        pyTTS(text)
                

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())