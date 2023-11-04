import pygame, pyttsx3
from gtts import gTTS


def pyTTS(txt):
    engine = pyttsx3.init()
    # 느린 말 속도로 설정 (기본값은 200)
    engine.setProperty('rate', 150)  # 속도를 낮춰보세요 (예: 100)
    engine.say(txt)
    engine.runAndWait()

def gglTTS(txt, fn):
    text = txt
    tts = gTTS(text=text, lang='ko')
    tts.save(fn + ".mp3")

    music_file = fn + ".mp3"   # mp3 or mid file

    freq = 16000    # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
    bitsize = -16   # signed 16 bit. support 8,-8,16,-16
    channels = 1    # 1 is mono, 2 is stereo
    buffer = 2048   # number of samples (experiment to get right sound)

    # default : pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(30)
    pygame.mixer.quit()