import subprocess
import librosa
from common import EXIT_BTN, HIT_FX_SPRITE, LARGE_NOTE_SCORE, LARGE_NOTE_SPRITE, LONG_NOTE_MINIMUM_DURATION, MISS_FX_SPRITE, PAD_SPRITE, PAUSE_BACKGROUND, PAUSE_TEXT, PROJECT_PATH, RESTART_BTN, RESUME_BTN, RESUME_COUNTDOWN_SPRITES, SMALL_NOTE_SCORE, SMALL_NOTE_SPRITE, SPEED_MULTIPLIER, PAD_Y_POS, WHITE_TEXT, WIN_W
from customTypes import *

from utils import concatenateAudio, numberRounding, cleanup
import numpy


import pygame.mixer
import pygame.sprite
import pygame.image
import pygame.rect
import pygame.font
import pygame.transform
import pygame.display
import os
# import platform
pygame.init()
pygame.display.init()

class AudioAnalyzer():
    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
        self.noteStartList = []
        self.smallNotesList = []
    def loadIntoLibrosa(self):
        # print("step1")
        # song name
        self.songName = os.path.basename(self.fileName)
        # convert if not wav
        if not self.fileName.endswith(".wav"):
            subprocess.run(args=['ffmpeg', '-i', self.fileName, f"{self.songName}.wav"])
            self.fileName = os.path.join(f"{self.songName}.wav")

        # append file:
        # concatenateAudio(["assets/blank.wav", self.fileName])
        cleanup(f"{self.songName}.wav")
        # self.fileName = "temp2.wav"
        # load into librosa
        print(self.fileName)
        self.soundData, self.sampleRate = librosa.load(self.fileName)
        print('load_complete')
        self.duration = librosa.get_duration(y = self.soundData, sr = self.sampleRate)
        self.oenv = librosa.onset.onset_strength(y=self.soundData, sr=self.sampleRate)

        return self.duration, self.songName, self.fileName
    def calcBPM(self):
        bpm = float(librosa.beat.tempo(y=self.soundData, sr=self.sampleRate))
        return bpm
    
    def detectNotes(self):
        self.noteStartList = librosa.onset.onset_detect(y=self.soundData, sr=self.sampleRate, normalize=True, backtrack=True)
        self.noteEndList = librosa.onset.onset_backtrack(self.noteStartList, self.oenv)
        
        self.noteStartList: numpy.array = librosa.frames_to_time(self.noteStartList, sr=self.sampleRate)
        self.noteStartList: list = list(map(numberRounding,list(self.noteStartList)))

        self.noteEndList: numpy.array = librosa.frames_to_time(self.noteEndList, sr=self.sampleRate)
        self.noteEndList: list = list(map(numberRounding,list(self.noteEndList)))
        return self.noteStartList
    
    def detectSmallNotes(self):
        print("obtaining track BPM")
        bpm = self.calcBPM()
        print("obtained track BPM")
        noteLength = 15/bpm
        smallNotesList= [] 
        for i in range(len(self.noteStartList) - 1):
            noteDuration = self.noteEndList[i + 1] - self.noteStartList[i]
            smallNoteGroup = []
            if noteDuration >= LONG_NOTE_MINIMUM_DURATION:
                t = self.noteStartList[i]
                while t < self.noteEndList[i + 1] - 60 / bpm:
                    t += noteLength
                    smallNoteGroup.append(t)
            smallNotesList.append(smallNoteGroup)
        return smallNotesList


    def createPygameMixerObj(self):
        pygame.mixer.music.load(self.fileName)

class BaseNote():
    def update(self, bpm, fps):
        self.y += PAD_Y_POS / ((1 / SPEED_MULTIPLIER) / bpm) / fps

class LargeNote(BaseNote):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(LARGE_NOTE_SPRITE)
        self.rect = pygame.rect.Rect(14, 14, 52, 52)
        

class SmallNote(BaseNote):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(SMALL_NOTE_SPRITE)
        self.rect = self.image.get_rect()
    
    

class Pad():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(PAD_SPRITE)
        self.rect = self.image.get_rect()
    def render(self, window):
        window.blit(self.image, (self.x, self.y))
        

class PauseMenu():
    def __init__(self) -> None:
        self.font = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 28)
        self.image = pygame.image.load(PAUSE_TEXT)
        self.resumeBtn = pygame.image.load(RESUME_BTN)
        self.restartBtn = pygame.image.load(RESTART_BTN)
        self.exitBtn = pygame.image.load(EXIT_BTN)
        self.image = pygame.transform.scale(self.image, (400, 90))

        self.resumeBtn = pygame.transform.scale(self.resumeBtn, (128, 128))
        self.restartBtn = pygame.transform.scale(self.restartBtn, (128, 128))
        self.exitBtn = pygame.transform.scale(self.exitBtn, (128, 128))
        
        self.resumeBtnText = self.font.render("Resume [ESC]", True, WHITE_TEXT)
        self.restartBtnText = self.font.render("Restart [R]", True , WHITE_TEXT)
        self.exitBtnText = self.font.render("Exit [E]", True, WHITE_TEXT)

        self.resumeBtnTextRect = self.resumeBtnText.get_rect()
        self.restartBtnTextRect = self.restartBtnText.get_rect()
        self.exitBtnTextRect = self.exitBtnText.get_rect()

        self.rect = self.image.get_rect()
        self.resumeBtnRect = self.resumeBtn.get_rect()
        self.restartBtnRect = self.restartBtn.get_rect()
        self.exitBtnRect = self.exitBtn.get_rect()

        self.x = int((WIN_W - self.rect.width) / 2)
        self.y = 30

        self.resumeBtnX = int(((WIN_W / 3) - self.resumeBtnRect.width) / 2)
        self.resumeBtnY = 300
        
        self.restartBtnX = int((WIN_W / 3) + ((WIN_W / 3) - self.restartBtnRect.width) / 2)
        self.restartBtnY = 300

        self.exitBtnX = int((WIN_W / 3) * 2 + ((WIN_W / 3) - self.exitBtnRect.width) / 2)
        self.exitBtnY = 300

        self.resumeBtnTextX = int(((WIN_W / 3) - self.resumeBtnTextRect.width) / 2)
        self.resumeBtnTextY = 500

        self.restartBtnTextX = int((WIN_W / 3) + ((WIN_W / 3) - self.restartBtnTextRect.width) / 2)
        self.restartBtnTextY = 500

        self.exitBtnTextX = int((WIN_W / 3) * 2 + ((WIN_W / 3) - self.exitBtnTextRect.width) / 2)
        self.exitBtnTextY = 500

        self.resumeBtnRect.topleft = (self.resumeBtnX, self.resumeBtnY)
        self.restartBtnRect.topleft = (self.restartBtnX, self.restartBtnY)
        self.exitBtnRect.topleft = (self.exitBtnX, self.exitBtnY)

    def show(self, window) -> None:
        window.blit(self.image, (self.x, self.y))
        window.blit(self.resumeBtn, (self.resumeBtnX, self.resumeBtnY))
        window.blit(self.restartBtn, (self.restartBtnX, self.restartBtnY))
        window.blit(self.exitBtn, (self.exitBtnX, self.exitBtnY))
        window.blit(self.restartBtnText, (self.restartBtnTextX, self.restartBtnTextY))
        window.blit(self.resumeBtnText, (self.resumeBtnTextX, self.resumeBtnTextY))
        window.blit(self.exitBtnText, (self.exitBtnTextX, self.exitBtnTextY))
class PauseCountdown():
    def __init__(self) -> None:
        
        self.font = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 28)
        self.countdownText = self.font.render("Game will start in...", True, pygame.color.Color(WHITE_TEXT))
        self.countdownTextRect = self.countdownText.get_rect()
        self.countdownTextX = int((WIN_W - self.countdownTextRect.width) / 2)
        self.countdownTextY = 50
        self.i = 0
    def countdown(self, window) -> None:
        self.image = pygame.image.load(RESUME_COUNTDOWN_SPRITES[int(self.i / 40)])
        self.rect = self.image.get_rect()
        self.x = int((WIN_W - self.rect.width) / 2)
        self.y = 90
        window.blit(pygame.image.load(PAUSE_BACKGROUND), (0, 0))
        window.blit(self.countdownText, (self.countdownTextX, self.countdownTextY))
        window.blit(self.image, (self.x, self.y))
            
class Effect():
    def __init__(self, window, x, y, t, padX = None) -> None:
        self.img = 0
        self.alpha = 255
        self.t = t
        self.x = x
        self.y = y
        self.padX = padX
    def update(self):
        if self.alpha > 0:
            
            if self.t == HitState.Hit:
                self.img = HIT_FX_SPRITE
            elif self.t == HitState.Miss:
                self.img = MISS_FX_SPRITE
            self.img = self.img.convert_alpha()
            self.img.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
            self.alpha -= 5

class ScoreDisp():
    def __init__(self, t) -> None:
        self.alpha = 255
        self.t = t
    def show(self):
        if self.alpha > 0:
            if self.t == "SmallNote":
                self.img = SMALL_NOTE_SCORE
            elif self.t == "LargeNote":
                self.img = LARGE_NOTE_SCORE
            self.rect = self.img.get_rect()
            self.img = self.img.convert_alpha()
            self.img.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
            self.alpha -= 5

