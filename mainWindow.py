import sys, datetime, calendar, cv2, winsound, random, re
import time as t

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qt_material import *
from datetime import *
import speech_recognition as sr
from konlpy.tag import Okt

from settings import *
from src.module.face_detection import *
from src.module.similarity import *
from src.module.tts import *
from src.module.stt import *
from src.module.TAGO import *
from src.module.TAGO_data import *
from src.module.sms import *
from ui.mainUI import UI_MainWindow
from ui.selStationUI import UI_SelStation
from ui.selDepDateUI import UI_SelDepDate
from ui.selTrainUI import UI_SelTrain
from ui.peopleUI import UI_People
from ui.selSitUI import UI_SelSit
from ui.checkUI import UI_Check
from ui.smsDialog import SMS_Dialog
from ui.smsUI import UI_SMS

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
        
        # Camera preparation ###############################################################
        UI_MainWindow.cap = cv2.VideoCapture(0)

        UI_MainWindow.setupUI(self)
        # self.showFullScreen()
        self.show()

        global nlp
        nlp = Okt()
        
        while True:
            if gVar.locateSelf:
                print("locateSelf")
                self.timer = QTimer()
                self.timer.timeout.connect(self.repeatThis)
                self.timer.start(10000)
            
            start = self.startCam()
            if start == True:
                if gVar.currentP == "main":
                    if gVar.menu == 1:
                        gVar.currentP = "selStation"
                        self.go_to_selStation()
                elif gVar.currentP == "selStation":
                    self.go_to_selDepDate()
                elif gVar.currentP == "selDepDate":
                    self.go_to_selTrain()
                elif gVar.currentP == "selTrain":
                    self.go_to_people()
                elif gVar.currentP == "People":
                    self.go_to_selSit()
                elif gVar.currentP == "selSit":
                    self.go_to_check()
                elif gVar.currentP == "Check":
                    self.go_to_sms()
                elif gVar.currentP == "SMS":
                    self.finish_sms()

            elif start == False:
                if gVar.currentP == "selTrain":
                    if gVar.pause == 5:
                        gVar.currentP = "selDepDate"
                        self.go_to_selDepDate()
                    elif gVar.pause == 6:
                        self.go_to_main()
                elif gVar.currentP == "People":
                    if gVar.pause == 4:
                        gVar.currentP = "selDepDate"
                        self.go_to_selDepDate()
                    elif gVar.pause == 5:
                        self.go_to_main()
                elif gVar.currentP == "Check":
                    if gVar.pause == 4:
                        gVar.currentP = "selDepDate"
                        self.go_to_selDepDate()
                    elif gVar.pause == 5:
                        self.go_to_main()
                        

    def closeEvent(self, event):
        UI_MainWindow.cap.release()
        sys.exit()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            # 마우스 클릭 이벤트가 발생하면 이 부분이 실행됩니다.
            print('Mouse Clicked at', event.pos())
            self.drag_start_x = event.x()
            
            if gVar.currentP == "main":
                if gVar.pause == 1: # 음성안내 종료
                    pyTTS("음성안내를 종료합니다.")
                    gVar.gVarInit()
                elif gVar.pause == 2: # 승차권 구매 아님
                    print("승차권 구매 아님 처음으로")
                    gVar.gVarInit()

            elif gVar.currentP == "selStation":
                if gVar.pause == 1 or 2:
                    gVar.pause = 3

            elif gVar.currentP == "selDepDate":
                if gVar.pause == 1:
                    gVar.pause = 2
                elif gVar.pause == 4:
                    gVar.pause = 5

            elif gVar.currentP == "selTrain":
                if gVar.pause == 1:
                    gVar.pause = 2
                elif gVar.pause == 3:
                    gVar.pause = 4
                elif gVar.pause == 5:
                    gVar.pause = 6
            
            elif gVar.currentP == "People":
                if gVar.pause == 1:
                    gVar.pause = 6
                elif gVar.pause == 2:
                    gVar.pause = 3
                elif gVar.pause == 4:
                    gVar.pause = 5
                elif gVar.pause == 7:
                    gVar.pause = 8

            elif gVar.currentP == "selSit":
                if gVar.pause == 1:
                    gVar.pause = 2

            elif gVar.currentP == "Check":
                if gVar.pause == 1:
                    gVar.pause = 6
                elif gVar.pause == 2:
                    gVar.pause = 3
                elif gVar.pause == 4:
                    gVar.pause = 5
                elif gVar.pause == 7:
                    gVar.pause = 8

            elif gVar.currentP == "SMS":
                if gVar.pause == 1:
                    gVar.pause = 2
                elif gVar.pause == 3:
                    gVar.pause = 5
                elif gVar.pause == 4:
                    gVar.pause = 5
        
        return super().eventFilter(obj, event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_x = None

    def mouseMoveEvent(self, event):
        try:
            if self.drag_start_x is not None:
                delta = event.x() - self.drag_start_x
                self.drag_start_x = event.x()

                if gVar.currentP == "selDepDate":
                    h_bar = UI_SelDepDate.timeScrollArea.horizontalScrollBar()
                    h_bar.setValue(h_bar.value() - delta)
        except:
            pass
        
    def repeatThis(self):
        pyTTS("음성안내 기능이 있는 키오스크 입니다.")
        gVar.locateSelf = False

    def delay(self):
        self.now = datetime.now()
        if gVar.pause == -1:
            self.later = self.now + timedelta(seconds=20)
        else:
            self.later = self.now + timedelta(seconds=2)
    
    def go_to_main(self):
        extra = {
            'font_family': '나눔고딕'
        }
        apply_stylesheet(app, theme='light_blue.xml',
                            invert_secondary=True, extra=extra)
        myColor.primary_color = blue
        myColor.secondary_color = white
        myColor.primary_text_color = white
        myColor.secondary_text_color = black
        
        gVar.gVarInit()

        self.setCentralWidget(None)
        UI_MainWindow.setupUI(self)

    def go_to_selStation(self):
        print(gVar.mode, gVar.currentP, gVar.pause, gVar.menu)

        if gVar.mode == "touch":
            gVar.locateSelf = False
            self.timer.stop()

            UI_SelStation.page = 1
            gVar.currentP = "selStation"
            self.setCentralWidget(None)
            UI_SelStation.setupUI(self)

        elif gVar.mode == "voice":
            if gVar.currentP == "main":
                virtual_event = QMouseEvent(QEvent.MouseButtonPress, QPoint(0, 0), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                self.eventFilter(self, virtual_event)
            else:
                gVar.pause = 0
                arrStat = ""
                gVar.firstAsk = True

                gVar.darkMode = True
                extra = {
                    'font_family': '나눔고딕'
                }
                apply_stylesheet(app, theme='dark_teal.xml',
                                invert_secondary=False, extra=extra)
                myColor.primary_color = teal
                myColor.secondary_color = darkGray
                myColor.primary_text_color = darkGray
                myColor.secondary_text_color = teal
                
                if gVar.currentP == "selStation":
                    if gVar.pause == 1:
                        gVar.pause = 2
            
                UI_SelStation.page = 1
                self.setCentralWidget(None)
                UI_SelStation.setupUI(self)

    @pyqtSlot()
    def go_to_selDepDate(self):
        gVar.pause = 0
        gVar.firstAsk = True

        if gVar.mode == "touch":
            clicked_button = self.sender()
            if gVar.currentP == "selStation":
                gVar.arrStat = clicked_button.text()
        
        # if gVar.depStat != gVar.arrStat:
        #     self.setCentralWidget(None)
        #     UI_SelDepDate.setupUI(self)
        #     gVar.currentP = "selDepDate"
            
        #     if gVar.mode == "voice":
        #         gVar.pause = 0
        #         gVar.firstAsk = True
        # else:
        #     pyTTS("출발역과 도착역이 같습니다. 다시 선택해주세요.")
        #     gVar.arrStat = ""

        if isExist(gVar.depStat, gVar.arrStat, gVar.depDate):
            self.setCentralWidget(None)
            UI_SelDepDate.setupUI(self)
            gVar.currentP = "selDepDate"
            
            if gVar.mode == "voice":
                gVar.pause = 0
                gVar.firstAsk = True
        else:
            pyTTS("해당 역으로 가는 열차가 없습니다. 다시 선택해주세요.")
            arrStat = ""
    
    def go_to_selTrain(self):
        print(gVar.depStat, gVar.arrStat, gVar.depDate, gVar.depTime)                
        self.trainDf = getData(gVar.depStat, gVar.arrStat, gVar.depDate, gVar.depTime)
        print(self.trainDf)

        if not self.trainDf.empty:
            self.setCentralWidget(None)
            UI_SelTrain.setupUI(self)
            gVar.currentP = "selTrain"
        else:
            pyTTS("해당 시간대의 열차가 없습니다. 다시 선택해주세요.")

        gVar.pause = 0
        gVar.firstAsk = True

    def go_to_people(self):
        self.setCentralWidget(None)
        UI_People.setupUI(self)
        gVar.currentP = "People"

        gVar.pause = 0
        gVar.firstAsk = True
        
    def onItemSelected(self):
        selected_items = self.trainTable.selectedItems()

        if selected_items:
            row = selected_items[0].row()  # 첫 번째 선택 아이템의 행 인덱스 가져오기
            print(row)
            row_data = []  # 선택된 행의 데이터를 저장할 리스트

            for col in range(self.trainTable.columnCount()):
                item = self.trainTable.item(row, col)  # 선택된 행의 각 셀 아이템 가져오기
                if item:
                    row_data.append(item.text())  # 셀 아이템의 텍스트를 리스트에 추가

            print("Selected Row Data:", row_data)
            gVar.trainInfo = row_data[0].replace("\n", " ")
            gVar.depTime = row_data[1].split("\n")[0]
            gVar.arrTime = row_data[2].split("\n")[0]
            gVar.adultPrice = row_data[3]

        self.go_to_people()

    def increase_personnel(self, p_type):
        print(p_type)
        if gVar.totalPeople < 10:
            self.personnel[p_type] += 1
            gVar.totalPeople += 1

            if "성인" in p_type:
                print("성인")
                gVar.adultNum += 1
            elif "어린이" in p_type:
                gVar.childNum += 1
            elif "노인" in p_type:
                gVar.oldNum += 1
            elif "장애인" in p_type:
                gVar.disabledNum += 1
            
            print(gVar.adultNum, gVar.childNum, gVar.oldNum, gVar.disabledNum)

            for p, label in self.personnel_buttons:
                if p == p_type:
                    label.setText(f"{self.personnel[p_type]}")
                    gVar.totalPrice += self.price[p_type]
                    self.priceLabel.setText(f"{gVar.totalPrice}원")

    def decrease_personnel(self, p_type):
        if self.personnel[p_type] > 0:
            self.personnel[p_type] -= 1
            gVar.totalPeople -= 1

            if "성인" in p_type:
                gVar.adultNum -= 1
            elif "어린이" in p_type:
                gVar.childNum -= 1
            elif "노인" in p_type:
                gVar.oldNum -= 1
            elif "장애인" in p_type:
                gVar.disabledNum -= 1

            for p, label in self.personnel_buttons:
                if p == p_type:
                    label.setText(f"{self.personnel[p_type]}")
                    gVar.totalPrice -= self.price[p_type]
                    self.priceLabel.setText(f"{gVar.totalPrice}원")

    def go_to_selSit(self):
        if gVar.totalPeople > 0:
            self.setCentralWidget(None)
            UI_SelSit.setupUI(self)
            gVar.currentP = "selSit"

            gVar.pause = 0
            gVar.firstAsk = True
        else:
            pyTTS("최소 1명 이상의 인원을 선택해주세요.")

    def go_to_check(self):
        if gVar.seatNum == gVar.totalPeople:
            self.setCentralWidget(None)
            UI_Check.setupUI(self)

            gVar.currentP = "Check"
            gVar.pause = 0
            gVar.firstAsk = True
        else:
            pyTTS("좌석을 선택해주세요.")
    
    @pyqtSlot()
    def dlg_sms(self):
        gVar.currentP = "SMS"
        gVar.pause = 0
        gVar.firstAsk = True

        # self.sender().setEnabled(False) # 이전 페이지 버튼 비활성화
        self.smsWidget = SMS_Dialog()
        self.smsWidget.exec_()
        self.go_to_sms()
        # self.sender().setEnabled(True)

    def finish_sms(self):
        flag = True

        if len(gVar.phoneNum) != 11:
            flag = False

        if flag:
            pyTTS("IC칩을 위로 향하게 하여 카드 투입구에 꽂아주세요.")
            # 5초 멈춤
            t.sleep(5)
            pyTTS("결제가 완료되었습니다. 감사합니다.")

            self.go_to_main()

            send_sms("예매 정보\n" +
                "출발역: " + gVar.depStat + "\n" +
                "도착역: " + gVar.arrStat + "\n" +
                "출발일: " + gVar.depDate + "\n" +
                "출발시간: " + gVar.depTime + "\n" +
                "열차: " + gVar.trainInfo + "\n" +
                "좌석: " + gVar.selCar + " " + str(gVar.selSeats) + "\n" +
                "인원: " + str(gVar.totalPeople) + "\n" +
                "가격: " + str(gVar.totalPrice) + "원")
            
    def go_to_sms(self):
        self.setCentralWidget(None)
        UI_SMS.setupUI(self)
        gVar.currentP = "SMS"

        gVar.pause = 0
        gVar.firstAsk = True



    def startCam(self):        
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

            if gVar.retry == 3:
                pyTTS("혹시 이전 단계로 돌아가고 싶으시면 화면을 터치해주세요.")

            if gVar.mode == "voice":
                if (faceDetection(image) == False):
                    self.go_to_main()
                    text = "자리 비움이 감지되어 처음으로 돌아갑니다."
                    pyTTS(text)
                    return False
            
            if gVar.currentP == "main":
                if gVar.pause == 0:
                    if (faceDetection(image)):
                        gVar.locateSelf = False
                        self.timer.stop()
                        
                        gVar.mode = "voice"
                        text = "음성안내를 시작합니다. 음성안내를 원하지 않으면 화면을 터치해주세요."
                        pyTTS(text)

                        gVar.pause = 1
                        self.delay()

                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        text = "승차권 구매를 시작합니다. 구매가 아니라 승차권 환불, 예약표 찾기, 예약 취소를 원하시면 화면을 터치해주세요."
                        pyTTS(text)
                        gVar.pause = 2
                        self.delay()

                elif gVar.pause == 2:
                    if datetime.now() >= self.later:
                        gVar.menu = 1
                        gVar.pause = 3
                        return True
                    
            elif gVar.currentP == "selStation" and gVar.mode == "voice":
                if gVar.pause == 0:
                    if gVar.firstAsk:
                        pyTTS("지금부터 승차권 예매를 시작합니다. 삐이이 소리 후 도착역의 이름을 말씀해주세요.")
                        gVar.firstAsk = False
                    else:
                        pyTTS("삐이이 소리 후 다시 말씀해주세요.")
                    
                    recognizer = sr.Recognizer()

                    frequency = 500  # 소리의 주파수 (Hz)
                    duration = 500  # 소리의 지속 시간 (밀리초)
                    winsound.Beep(frequency, duration) # 마이크 입력 시작 알림음 재생

                    self.stt_result = gglSTT(recognizer)
                    self.stat_result = ""
                    self.match = 0

                    if self.stt_result != False:
                        # 형태소 분석
                        self.nouns = nlp.nouns(self.stt_result)
                        print(self.nouns)

                        for n in self.nouns:
                            if n.endswith("역"):
                                n = n[:-1]

                            if n in station:
                                print(n + "역 있음")
                                self.stat_result += n
                                self.match += 1
               
                        if self.match == 0:
                            pyTTS("역을 찾을 수 없습니다.")
                        elif self.match > 0:
                            pyTTS(self.stat_result + "역이 맞으면 화면을 터치해주세요.")
                            gVar.arrStat = self.stat_result
                        
                        gVar.pause = 1
                        self.delay()
                    else:
                        pyTTS("음성을 이해할 수 없습니다.")

                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        res = find_most_similar_jamo(self.stt_result, all_stations)
                        self.stat_result = res
                        print(self.stat_result)

                        if self.stat_result != False:
                            pyTTS("유사한 역을 찾습니다."
                                + self.stat_result + "역이 맞으면 화면을 터치해주세요.")
                        gVar.arrStat = self.stat_result
                        gVar.pause = 2
                        self.delay()

                elif gVar.pause == 2:
                    if datetime.now() >= self.later:
                        gVar.pause = 0
                        self.delay()

                elif gVar.pause == 3:
                    if datetime.now() >= self.later:
                        self.arrContLabel.setText(gVar.arrStat)
                        pyTTS(gVar.arrStat + "역이 선택되었습니다.")
                        return True

            elif gVar.currentP == "selDepDate" and gVar.mode == "voice":
                if gVar.pause == 0:
                    if gVar.firstAsk:
                        self.today = datetime.today()
                        self.today_plus5 = self.today + timedelta(days=5)
                        date = self.today.strftime("%Y년 %m월 %d일")
                        plus5 = (self.today_plus5).strftime("%m월 %d일")
                        print(plus5)
                        pyTTS("지금부터 출발 날짜를 선택합니다." +
                            "현재 날짜는 " + date + "입니다. " +
                            "날짜는 금일로부터 5일 후인" + plus5 + " 까지 선택 가능합니다. " +
                            "삐이이 소리 후 출발 날짜를 말씀해주세요.")
                        gVar.firstAsk = False
                    else:
                        pyTTS("삐이이 소리 후 다시 말씀해주세요.")
                
                    recognizer = sr.Recognizer()
                    
                    frequency = 500  # 소리의 주파수 (Hz)
                    duration = 500  # 소리의 지속 시간 (밀리초)
                    winsound.Beep(frequency, duration)

                    stt_result = gglSTT(recognizer)
                    

                    if stt_result != False:
                        # 형태소 분석
                        pos = nlp.pos(stt_result)
                        print(pos)

                        num_pattern = re.compile(r'\d')

                        for i in range(len(pos)):
                            if num_pattern.match(pos[i][0]):
                                day = pos[i][0]
                                day = int(re.sub(r'[^0-9]', '', day))
                                
                                # 내가 원하는 datetime 객체 생성
                                max_day = calendar.monthrange(self.today.year, self.today.month)[1]
                                
                                try:
                                    if (max_day - 5) < self.today.day:
                                        if day < 6:
                                            inputDate = datetime(self.today.year, self.today.month + 1, day)
                                        else:
                                            inputDate = datetime(self.today.year, self.today.month, day)
                                    else:
                                        inputDate = datetime(self.today.year, self.today.month, day)
                                    
                                    if (inputDate - self.today).days >= 0 and (self.today_plus5 - inputDate).days >= 0:
                                        gVar.depDate = self.today.strftime("%Y%m") + str(day)
                                        print(gVar.depDate)
                                        pyTTS(str(day) + "   일이 맞으면 화면을 터치해주세요.")
                                        
                                        gVar.pause = 1
                                        self.delay()
                                    else:
                                        pyTTS("선택할 수 없는 날짜입니다. 날짜를 다시 선택해주세요.")
                                except:
                                    pyTTS("선택할 수 없는 날짜입니다. 날짜를 다시 선택해주세요.")

                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        gVar.pause = 0
                        self.delay()

                elif gVar.pause == 2:
                    if datetime.now() >= self.later:
                        gVar.day = int(day)
                        pyTTS(str(gVar.day) + "   일이 선택되었습니다.")
                        gVar.firstAsk = True

                        # 기존 버튼 해제
                        for i, btn in enumerate(UI_SelDepDate.dateBtns):
                            btn.setChecked(False)
                            btn.setText(str((self.today + timedelta(days=i)).day).zfill(2))
                            btn.setStyleSheet(
                                largeFont +
                                "background-color: " + transparent + ";" +
                                "color: " + myColor.primary_color + ";" +
                                "border-radius: 10px;"
                            )
                        
                        # 새로운 버튼 선택
                        for i, btn in enumerate(UI_SelDepDate.dateBtns):
                            if btn.text() == str(gVar.day).zfill(2):
                                btn.setChecked(True)
                                btn.setText(btn.text() + "\n출발일")
                                btn.setStyleSheet(
                                    largeFont +
                                    "color: " + myColor.primary_text_color + ";" +
                                    "background-color: " + myColor.primary_color + ";" +
                                    "border-radius: 10px;" +
                                    "padding: 10px 30px 10px 10px;")
                        
                        max_day = calendar.monthrange(self.today.year, self.today.month)[1]
                        if (max_day - 5) < self.today.day:
                            if day < 6:
                                gVar.depDate = datetime(self.today.year, self.today.month + 1, gVar.day).strftime("%Y%m%d")
                            else:
                                gVar.depDate = datetime(self.today.year, self.today.month, gVar.day).strftime("%Y%m%d")
                        else:
                            gVar.depDate = datetime(self.today.year, self.today.month, gVar.day).strftime("%Y%m%d")
                       
                        print(gVar.depDate)

                        # 날짜 라벨 변경
                        currentDT = self.today + timedelta(days=gVar.day - self.today.day)
                        print(currentDT)
                        dayDic = {0: "월", 1: "화", 2: "수", 3: "목",
                            4: "금", 5: "토", 6: "일"}
                        day = dayDic[currentDT.weekday()]
                        currentDT = currentDT.strftime("%Y년 %m월 %d일") + "(" + day  + "요일) " + gVar.depTime[:-2] + ":" + gVar.depTime[-2:]
                        UI_SelDepDate.calSelDTLabel.setText(currentDT)

                        gVar.pause = 3
                    
                elif gVar.pause == 3:
                    if gVar.firstAsk:
                        pyTTS("지금부터 출발 시간을 선택합니다. " +
                                "현재 시간은 " + datetime.today().strftime("%H시 %M분") + "입니다." +
                                "지난 시점의 시간은 선택할 수 없으며, " +
                                "오전 또는 오후를 말하지 않으면 이십사 시간 형식을 사용합니다. " +
                                "삐이이 소리 후 출발 시간을 분까지 말씀해주세요.")
                        gVar.firstAsk = False
                    else:
                        pyTTS("삐이이 소리 후 다시 말씀해주세요.")

                    recognizer = sr.Recognizer()

                    frequency = 500  # 소리의 주파수 (Hz)
                    duration = 500  # 소리의 지속 시간 (밀리초)
                    winsound.Beep(frequency, duration)

                    self.stt_result = str(gglSTT(recognizer))
                    
                    # 형태소 분석
                    pos = nlp.pos(self.stt_result)
                    print(pos)
                    
                    ampm_pattern = re.compile(r'오전|오후')
                    hour_pattern = re.compile(r'\d+시')
                    min_pattern = re.compile(r'\d+분')

                    self.ampm = 0
                    self.hour = 0
                    self.minute = 0

                    for i in range(len(pos)):
                        if ampm_pattern.match(pos[i][0]):
                            self.ampm = pos[i][0]
                        if hour_pattern.match(pos[i][0]):
                            self.hour = pos[i][0]        
                            self.hour = int(self.hour[:-1])
                            
                            if self.ampm == "오전":
                                if self.hour == 12:
                                    self.hour = 0
                            elif self.ampm == "오후":
                                self.hour = self.hour + 12
                        elif min_pattern.match(pos[i][0]):
                            self.minute = pos[i][0]
                            self.minute = int(self.minute[:-1])

                    if  self.hour < 0 or self.hour > 23:
                        pyTTS("선택할 수 없는 시간입니다. 시간을 다시 선택해주세요.")
                        break
                    elif self.minute < 0 or self.minute > 59:
                        pyTTS("선택할 수 없는 시간입니다. 시간을 다시 선택해주세요.")
                        break 

                    if gVar.day == self.today.day:
                        if self.hour < self.today.hour:
                            pyTTS("선택할 수 없는 시간입니다. 시간을 다시 선택해주세요.")
                            break
                        elif self.hour == self.today.hour and self.minute < self.today.minute:
                            pyTTS("선택할 수 없는 시간입니다. 시간을 다시 선택해주세요.")
                            break
                    
                    pyTTS("출발 시간이 " + str(self.hour) + "시 " +
                        str(self.minute) + "분이 맞으면 화면을 터치해주세요.")
                    
                    gVar.pause = 4
                    self.delay()
                
                elif gVar.pause == 4:
                    if datetime.now() >= self.later:
                        gVar.pause = 3
                        self.delay()

                elif gVar.pause == 5:
                    if datetime.now() >= self.later:
                        gVar.ampm = self.ampm
                        if self.hour < 10:
                            gVar.hour = "0" + str(self.hour)
                        else:
                            gVar.hour = self.hour
                        if self.minute < 10:
                            gVar.minute = "0" + str(self.minute)
                        else:
                            gVar.minute = self.minute
                        gVar.depTime = str(gVar.hour) + str(gVar.minute)

                        pyTTS(str(self.hour) + "시 " +
                            str(self.minute) + "분이 선택되었습니다.")
                        
                        # 시간 라벨 변경
                        currentDT = UI_SelDepDate.calSelDTLabel.text()[:-5]
                        UI_SelDepDate.calSelDTLabel.setText(
                            currentDT + " " + str(gVar.hour) + ":" + str(gVar.minute))

                        # 기존 버튼 해제
                        for i, btn in enumerate(UI_SelDepDate.timeBtns):
                            btn.setChecked(False)
                            btn.setStyleSheet(
                                largeFont +
                                "background-color: " + transparent + ";" +
                                "color: " + myColor.primary_color + ";"
                                "border: none;"
                            )

                        # 새로운 버튼 선택
                        selected_tBtn = UI_SelDepDate.timeBtns[self.hour]
                        selected_tBtn.setChecked(True)
                        selected_tBtn.setStyleSheet(
                            largeFont +
                            "background-color: " + myColor.primary_color + ";" +
                            "color: " + myColor.secondary_color + ";"
                            "border: none;"
                        )
                        
                        gVar.pause = -1
                        return True
                    
            elif gVar.currentP == "selTrain" and gVar.mode == "voice":
                if gVar.pause == 0:
                    if gVar.firstAsk:
                        depTime = str(self.trainDf.iloc[0]['depplandtime'])
                        depHour = depTime[8:10]
                        depMinute = depTime[10:12]
                        arrTime = str(self.trainDf.iloc[0]['arrplandtime'])
                        arrHour = arrTime[8:10]
                        arrMinute = arrTime[10:12]
                        type = str(self.trainDf.iloc[0]['traingradename'])
                        price = str(self.trainDf.iloc[0]['adultcharge'])

                        pyTTS("지금부터 승차할 열차를 선택합니다. " +
                            "말씀하신 시간과 첫 번째로 가까운 시간대의 열차는 " +
                            depHour + "시 " + depMinute + "분에 출발하는 " + type + "열차입니다. " +
                            "해당 열차의 도착 시간은 " + arrHour + "시 " + arrMinute + "분입니다. " +
                            "가격은 일반실 성인 1인에 " + price + "원 입니다. " +
                            "해당 열차를 선택하시려면 화면을 터치해주세요.")
                    else:
                        depTime = str(self.trainDf.iloc[1]['depplandtime'])
                        depHour = depTime[8:10]
                        depMinute = depTime[10:12]
                        arrTime = str(self.trainDf.iloc[1]['arrplandtime'])
                        arrHour = arrTime[8:10]
                        arrMinute = arrTime[10:12]
                        type = str(self.trainDf.iloc[1]['traingradename'])
                        price = str(self.trainDf.iloc[1]['adultcharge'])

                        print(depHour, depMinute, arrHour, arrMinute, type, price)

                        pyTTS("말씀하신 시간과 두 번째로 가까운 시간대의 열차는 " +
                            depHour + "시 " + depMinute + "분에 출발하는 " + type + "열차입니다. " +
                            "해당 열차의 도착 시간은 " + arrHour + "시 " + arrMinute + "분입니다. " +
                            "가격은 일반실 성인 1인에 " + price + "원 입니다. " +
                            "해당 열차를 선택하시려면 화면을 터치해주세요.")
                    
                    gVar.pause = 1
                    self.delay()
                
                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        if gVar.firstAsk:
                            gVar.firstAsk = False
                            gVar.pause = 0
                        else:
                            pyTTS("다시 듣기를 시작합니다. " +
                                  "다시 듣기가 아니라 이전 단계로 돌아가시려면 화면을 터치해주세요.")
                            gVar.pause = 3
                        self.delay()
                
                elif gVar.pause == 2: # 열차 정보 말하기
                    if datetime.now() >= self.later:
                        if gVar.firstAsk == True:
                            pyTTS("첫 번째 열차가 선택되었습니다.")
                            selected_train = self.trainDf.iloc[0]
                            
                        else:
                            pyTTS("두 번째 열차가 선택되었습니다.")
                            selected_train = self.trainDf.iloc[1]
                        
                        # print(gVar.trainInfo)

                        gVar.depTime = str(selected_train['depplandtime'])[8:10] + ":" + str(selected_train['depplandtime'])[10:12]
                        gVar.arrTime = str(selected_train['arrplandtime'])[8:10] + ":" + str(selected_train['arrplandtime'])[10:12]
                        gVar.trainInfo = str(selected_train['traingradename']) + " " + str(selected_train['trainno'])
                        gVar.adultPrice = str(selected_train['adultcharge'])
                        return True

                elif gVar.pause == 3:
                    if datetime.now() >= self.later:
                        gVar.pause = 0
                        gVar.firstAsk = True
                        
                elif gVar.pause == 4:
                    if datetime.now() >= self.later:
                        pyTTS("날짜와 시간을 선택하는 단계로 되돌아 갑니다." +
                              "이전 단계가 아니라 처음으로 돌아가길 원하시면 화면을 터치해주세요.")
                        gVar.pause = 5
                        self.delay()

                elif gVar.pause == 5:
                    if datetime.now() >= self.later:
                        return False
                
                elif gVar.pause == 6:
                    if datetime.now() >= self.later:
                        pyTTS("처음으로 돌아갑니다.")
                        return False

            elif gVar.currentP == "People" and gVar.mode == "voice":
                if gVar.pause == 0:
                    pyTTS("선택하신 열차 정보를 다시 확인합니다. " +
                        "출발역은 " + gVar.depStat + "역입니다. " +
                        "도착역은 " + gVar.arrStat + "역입니다. " +
                        "출발 날짜는 " + gVar.depDate[4:6] + "월 "
                          + gVar.depDate[6:] + "일입니다. " +
                        "출발 시간은 " + gVar.depTime[:-2] + "시 " + gVar.depTime[-2:] + "분입니다. " +
                        "도착 시간은 " + gVar.arrTime[:-2] + "시 " + gVar.arrTime[-2:] + "분입니다. " +
                        "열차는 " + gVar.trainInfo + " 입니다. " +
                        "가격은 일반실 성인 1인에 " + gVar.adultPrice + "원 입니다. " +
                        "맞으면 화면을 터치해주세요. ")
                    
                    gVar.pause = 1
                    self.delay()
                
                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        pyTTS("다시 듣기를 시작합니다. " +
                              "다시 듣기가 아니라 이전 단계로 돌아가시려면 화면을 터치해주세요.")
                        gVar.pause = 2
                        self.delay()
                
                elif gVar.pause == 2:
                    gVar.pause = 0

                elif gVar.pause == 3:
                    if datetime.now() >= self.later:
                        pyTTS("날짜와 시간 선택 단계로 돌아갑니다. " +
                              "날짜와 시간 선택 단계가 아니라 " +
                              "처음으로 돌아가시려면 화면을 터치해주세요.")
                        gVar.pause = 4
                        self.delay()
                
                elif gVar.pause == 4:
                    if datetime.now() >= self.later:
                        pyTTS("날짜와 시간 선택 단계로 돌아갑니다.")
                        return False

                elif gVar.pause == 5:
                    if datetime.now() >= self.later:
                        pyTTS("처음으로 돌아갑니다.")
                        return False
                    
                elif gVar.pause == 6:
                    if datetime.now() >= self.later:
                        pyTTS("지금부터 할인을 위한 정보를 입력합니다. " +
                            "중증 장애인이신 경우에는 화면을 터치해주세요. ")
                        gVar.pause = 7
                        self.delay()

                elif gVar.pause == 7:
                    if datetime.now() >= self.later:
                        p_type = f"성인({gVar.adultPrice}원)"
                        self.increase_personnel(p_type)
                        gVar.totalPrice = int(gVar.adultPrice)

                        pyTTS("할인이 적용되지 않습니다. " +
                            "할인이 적용되지 않은 가격은 " + str(gVar.totalPrice) + "원 입니다. ")
                        return True
                
                elif gVar.pause == 8:
                    if datetime.now() >= self.later:
                        self.disabledPrice = int(round(int(gVar.adultPrice) * 0.5, -2))
                        gVar.totalPrice = int(self.disabledPrice)
                        p_type = f"중증장애인({self.disabledPrice}원)"
                        self.increase_personnel(p_type)
                        gVar.totalPrice = int(round(int(gVar.adultPrice) * 0.5, -2))

                        pyTTS("할인이 적용되었습니다. " +
                            "할인이 적용된 가격은 " + str(gVar.totalPrice) + "원 입니다. ")
                        return True

            elif gVar.currentP == "selSit" and gVar.mode == "voice":
                if gVar.pause == 0:
                    # gVar.toalPeople = 1
                    pyTTS("지금부터 좌석을 선택합니다. " +
                        "좌석은 통로측 좌석으로 자동으로 배정됩니다. " +
                        "통로측이 아니라 창측으로 좌석을 변경하시려면 화면을 터치해주세요.")

                    gVar.pause = 1
                    self.delay()

                # 창측: 0~7, 16~23
                # 통로측: 8~15, 24~31

                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        pyTTS("통로측 좌석으로 자동 배정되었습니다.")
                        
                        # 0~7, 16~23 중 랜덤으로 선택
                        n = random.choice([i for i in range(0, 8)] + [i for i in range(16, 24)])
                        # gVar.selSeats.append(UI_SelSit.seatBtns[n])
                        UI_SelSit.seatBtns[n].setChecked(True)
                        UI_SelSit.clicked_seatBtn(n)

                        return True

                elif gVar.pause == 2:
                    if datetime.now() >= self.later:
                        pyTTS("창측 좌석으로 자동 배정되었습니다.")

                        # 8~15, 24~31 중 랜덤으로 선택
                        n = random.choice([i for i in range(8, 16)] + [i for i in range(24, 32)])
                        # gVar.selSeats.append(UI_SelSit.seatBtns[n])
                        UI_SelSit.seatBtns[n].setChecked(True)
                        UI_SelSit.clicked_seatBtn(n)

                        return True

            elif gVar.currentP == "Check" and gVar.mode == "voice":
                if gVar.pause == 0:
                    pyTTS("선택하신 열차 정보를 다시 확인합니다. " +
                        "출발역은 " + gVar.depStat + "역입니다. " +
                        "도착역은 " + gVar.arrStat + "역입니다. " +
                        "출발 날짜는 " + gVar.depDate[4:6] + "월 "
                          + gVar.depDate[6:] + "일입니다. " +
                        "출발 시간은 " + gVar.depTime[:-2] + "시 " + gVar.depTime[-2:] + "분입니다. " +
                        "도착 시간은 " + gVar.arrTime[:-2] + "시 " + gVar.arrTime[-2:] + "분입니다. " +
                        "열차는 " + gVar.trainInfo + " 입니다. " +
                        "가격은 " + str(gVar.totalPrice) + "원 입니다. " +
                        "좌석은 " + gVar.selSeats[0] + "입니다. " +
                        "맞으면 화면을 터치해주세요. ")

                    gVar.pause = 1
                    self.delay()

                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        pyTTS("다시 듣기를 시작합니다. " +
                              "다시 듣기가 아니라 이전 단계로 돌아가시려면 화면을 터치해주세요.")
                        gVar.pause = 2
                        self.delay()

                elif gVar.pause == 2:
                    if datetime.now() >= self.later:
                        gVar.pause = 0

                elif gVar.pause == 3:
                    if datetime.now() >= self.later:
                        pyTTS("열차 선택 단계로 돌아갑니다. " +
                              "열차 선택 단계가 아니라 " +
                              "처음으로 돌아가시려면 화면을 터치해주세요.")
                        gVar.pause = 4
                        self.delay()

                elif gVar.pause == 4:
                    if datetime.now() >= self.later:
                        return False

                elif gVar.pause == 5:
                    if datetime.now() >= self.later:
                        pyTTS("처음으로 돌아갑니다.")
                        return False

                elif gVar.pause == 6:
                    if datetime.now() >= self.later:
                        return True

            elif gVar.currentP == "SMS" and gVar.mode == "voice":
                if gVar.pause == 0:
                    pyTTS("지금부터 결제를 진행합니다. " +
                        "예매 정보를 휴대폰으로 수신하시려면 화면을 터치해주세요.")
                    gVar.pause = 1
                    self.delay()

                elif gVar.pause == 1:
                    if datetime.now() >= self.later:
                        return True

                elif gVar.pause == 2:
                    if datetime.now() >= self.later:
                        pyTTS("휴대폰 번호를 말씀해주세요. ")

                        recognizer = sr.Recognizer()

                        frequency = 500  # 소리의 주파수 (Hz)
                        duration = 500  # 소리의 지속 시간 (밀리초)
                        winsound.Beep(frequency, duration)

                        self.stt_result = str(gglSTT(recognizer))
                        
                        # 형태소 분석
                        pos = nlp.pos(self.stt_result)
                        print(pos)

                        num_pattern = re.compile(r'\d')
                        
                        gVar.phoneNum = ""
                        for i in range(len(pos)):
                            if num_pattern.match(pos[i][0]):
                                gVar.phoneNum += pos[i][0]
                        
                        print(gVar.phoneNum)
                        numbers = [int(char) for char in gVar.phoneNum if char.isdigit()]
                        gVar.phoneNum = ''.join(map(str, numbers))
                        print(gVar.phoneNum)
                        nums = '  '.join(map(str, numbers))
                        print(numbers)
                        print(nums)

                        pyTTS("휴대폰 번호가 " + nums + "이 맞으면 화면을 터치해주세요.")
                        
                        gVar.pause = 3
                        self.delay()

                elif gVar.pause == 3:
                    if datetime.now() >= self.later:
                        pyTTS("모바일 예매표 서비스를 취소하시려면 화면을 터치해주세요.")
                        gVar.pause = 4
                        self.delay()
                        
                elif gVar.pause == 4:
                    if datetime.now() >= self.later:
                        pyTTS("휴대폰 번호를 다시 입력받습니다.")
                        gVar.pause = 2

                elif gVar.pause == 5:
                    if datetime.now() >= self.later:
                        return True

                elif gVar.pause == 6:
                    if datetime.now() >= self.later:
                        if len(gVar.phoneNum) == 11:
                            return True
                        else:
                            pyTTS("휴대폰 번호를 다시 확인해주세요.")
                            gVar.pause = 2


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    
    sys.exit(app.exec_())