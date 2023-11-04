import speech_recognition as sr

# 구글 웹 음성 API로 인식하기
# 마이크 시작
recognized_text = ""

def gglSTT(recognizer):
    with sr.Microphone() as source:
        # 마이크 입력 대기
        print("마이크 입력 대기 중...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("마이크 입력 종료")
            
            # 음성 인식 수행
            recognized_text = recognizer.recognize_google(audio, language="ko-KR")
            print("인식된 텍스트: ", recognized_text)
            
            return recognized_text
        
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return False
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return False
        except sr.WaitTimeoutError:
            print("마이크 입력이 없어서 마이크를 끕니다.")
            return False