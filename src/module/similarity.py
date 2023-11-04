from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from src.module.TAGO_data import *


def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    # 거리 배열 초기화
    distances = np.arange(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances

    return distances[-1]

def split_jamo(s):
    # 유니코드 번호
    START_CODE, END_CODE = 44032, 55203  # '가', '힣'
    CHOSUNG_BASE, JUNGSUNG_BASE, JONGSUNG_BASE = 588, 28, 1
    CHOSUNG_LIST = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]
    JUNGSUNG_LIST = [
        'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
    ]
    JONGSUNG_LIST = [
        '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
        'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]

    result = []
    for char in s:
        # 한글 아닌 경우
        if not START_CODE <= ord(char) <= END_CODE:
            result.append(char)
            continue
        # 한글인 경우
        code = ord(char) - START_CODE
        cho, jung, jong = code // CHOSUNG_BASE, (code % CHOSUNG_BASE) // JUNGSUNG_BASE, (code % CHOSUNG_BASE) % JUNGSUNG_BASE
        result.extend([CHOSUNG_LIST[cho], JUNGSUNG_LIST[jung], JONGSUNG_LIST[jong]])

    return ''.join(result)


def find_most_similar_jamo(input_text, text_list):
    input_text_jamo = split_jamo(input_text)
    min_distance = float('inf')
    most_similar_text = None

    for text in text_list:
        text_jamo = split_jamo(text)
        distance = levenshtein_distance(input_text_jamo, text_jamo)

        if distance < min_distance:
            min_distance = distance
            most_similar_text = text
            print(most_similar_text, min_distance)
    
    return most_similar_text