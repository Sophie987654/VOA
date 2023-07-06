import pygame, cv2
import mediapipe as mp

from gtts import gTTS
from datetime import *
from settings import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands


def faceDetection(image):
    with mp_face_detection.FaceDetection( #얼굴인식
    model_selection = 0,
    min_detection_confidence = 0.5
    ) as face_detection:
        results = face_detection.process(image)
        
        if results.detections: # 사람 있음
            for detection in results.detections: # 주석 그리기
                mp_drawing.draw_detection(image, detection)

            gVar.face_cnt += 1
            gVar.no_face_cnt = 0
            print(gVar.face_cnt)

            if gVar.face_cnt == 80:
                gVar.face_cnt = 0
                gVar.no_face_cnt = 0
                return True
        else:
            gVar.face_cnt = 0
            gVar.no_face_cnt += 1
            print("no face: " + str(gVar.no_face_cnt))

            if gVar.no_face_cnt == 80:
                gVar.face_cnt = 0
                gVar.no_face_cnt = 0
                return False
    