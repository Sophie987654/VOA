import mediapipe as mp
from datetime import *
from settings import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
global first_time, no_face_first_time
first_time = None
no_face_first_time = None

"""
    얼굴 인식 함수
    Parameters:
        image (ndarray): 웹캠으로부터 받아온 이미지
    Returns:
        bool: 얼굴이 감지되었는지 여부
"""

def faceDetection(image):
    global first_time, no_face_first_time
    
    if gVar.face_first:
        gVar.face_first = False
        first_time = datetime.now() # 현재 시간 저장

    with mp_face_detection.FaceDetection(
    model_selection = 0,    # 모델 선택 - 2m 이내의 얼굴만 인식
    min_detection_confidence = 0.5  # 최소 인식 신뢰도
    ) as face_detection:
        results = face_detection.process(image) # MediaPipe Facedetection 결과
        
        if results.detections: # 사람 있음
            for detection in results.detections: # 주석 그리기
                mp_drawing.draw_detection(image, detection)

            if first_time + timedelta(seconds=3) < datetime.now(): # 3초가 지났을 때
                gVar.face_first = True
                return True # True 반환
        else: # 사람 없음
            gVar.face_first = True
            
            if gVar.no_face_first:
                gVar.no_face_first = False
                no_face_first_time = datetime.now() # 현재 시간 저장
            
            if no_face_first_time + timedelta(seconds=10) < datetime.now():
                gVar.no_face_first = True
                return False