import pygame.mixer
import pygame.sprite
import pygame.image
import pygame.rect
import pygame.font
import pygame.transform
import pygame.display
import os.path
pygame.init()
pygame.display.init()

class AudioAnalyzer():
    def __init__(self, fileName: str) -> None:

        self.fileName = fileName
        self.noteStartList = []
        self.smallNotesList = []
    def loadIntoLibrosa(self):
        # import files
        from subprocess import run as s_run
        from librosa.onset import onset_strength
        from librosa import load as l_load
        from utils import concatenateAudio
        # song name
        self.songName = os.path.basename(self.fileName)
        # convert if not wav
        if not self.fileName.endswith(".wav"):
            s_run(args=['./ffmpeg.exe', '-i', self.fileName, "temp.wav"])
            self.fileName = "temp.wav"

        # append file:
        concatenateAudio(["assets/blank.wav", self.fileName])
        self.fileName = "temp2.wav"
        # load into librosa
        self.soundData, self.sampleRate = l_load(self.fileName)
        self.oenv = onset_strength(y=self.soundData, sr=self.sampleRate)

        return self.songName
    def calcBPM(self):
        from librosa.beat import tempo as l_tempo

        bpm = float(l_tempo(y=self.soundData, sr=self.sampleRate))
        return bpm
    
    def detectNotes(self):
        from librosa import frames_to_time
        from librosa.onset import onset_backtrack, onset_detect
        from numpy import array

        self.noteStartList = onset_detect(y=self.soundData, sr=self.sampleRate, normalize=True, backtrack=True)
        self.noteEndList = onset_backtrack(self.noteStartList, self.oenv)
        
        self.noteStartList: array = frames_to_time(self.noteStartList, sr=self.sampleRate)
        #self.noteStartList: tuple = tuple(map(numberRounding,list(self.noteStartList)))

        self.noteEndList: array = frames_to_time(self.noteEndList, sr=self.sampleRate)
        #self.noteEndList: tuple = tuple(map(numberRounding,list(self.noteEndList)))
        self.noteEndList = tuple(self.noteEndList)
        self.noteStartList = tuple(self.noteStartList)
        return (self.noteStartList)
    
    def detectSmallNotes(self):
        from common import LONG_NOTE_MINIMUM_DURATION

        bpm = self.calcBPM()
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


class BaseNote():
    def update(self, bpm, fps):
        from common import PAD_Y_POS, SPEED_MULTIPLIER
        self.y += PAD_Y_POS / ((1 / SPEED_MULTIPLIER) / bpm) / fps

class LargeNote(BaseNote):
    def __init__(self, x, y):
        from common import LARGE_NOTE_SPRITE
        self.x = x
        self.y = y
        self.image = LARGE_NOTE_SPRITE
        self.rect = pygame.rect.Rect(14, 14, 52, 52)
        

class SmallNote(BaseNote):
    def __init__(self, x, y):
        from common import SMALL_NOTE_SPRITE
        self.x = x
        self.y = y
        self.image = SMALL_NOTE_SPRITE
        self.rect = self.image.get_rect()
    
class MainMenu():
    def __init__(self) -> None:
        from common import RESUME_BTN, INFO_BTN, WIN_W, HELP_BTN, MENU_TITLE, WIN_H
        
        # images
        self.playBtn = pygame.transform.smoothscale(RESUME_BTN, (200, 200))
        self.aboutBtn = pygame.transform.smoothscale(INFO_BTN, (50, 50))
        self.helpBtn = pygame.transform.smoothscale(HELP_BTN, (50, 50))

        # positions
        self.titlePos = ((WIN_W - MENU_TITLE.get_width()) / 2, 40)
        self.playBtnPos = ((WIN_W - self.playBtn.get_width()) / 2, 240)
        self.aboutBtnPos = (30, WIN_H - 20 - self.aboutBtn.get_height())
        self.helpBtnPos = (60 + self.aboutBtn.get_width(), WIN_H - 20 - self.helpBtn.get_height())

        # rects
        self.titleRect = MENU_TITLE.get_rect()
        self.playBtnRect = self.playBtn.get_rect()
        self.aboutBtnRect = self.aboutBtn.get_rect()
        self.helpBtnRect = self.helpBtn.get_rect()

        # set rect coords
        self.titleRect.topleft = self.titlePos
        self.playBtnRect.topleft = self.playBtnPos
        self.aboutBtnRect.topleft = self.aboutBtnPos
        self.helpBtnRect.topleft = self.helpBtnPos

    def show(self, window):
        from common import MAIN_MENU_BG, MENU_TITLE

        window.blit(MAIN_MENU_BG, (0, 0))
        window.blit(self.playBtn, self.playBtnPos)
        window.blit(self.aboutBtn, self.aboutBtnPos)
        window.blit(self.helpBtn, self.helpBtnPos)
        window.blit(MENU_TITLE, self.titlePos)

class Pad():
    def __init__(self, x, y):
        from common import PAD_SPRITE

        self.x = x
        self.y = y
        self.image = PAD_SPRITE
        self.rect = self.image.get_rect()
    def render(self, window):
        self.rect.topleft = (self.x, self.y)
        window.blit(self.image, (self.x, self.y))

class PauseMenu():
    def __init__(self) -> None:
        self.font = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 28)
        
        from common import PAUSE_BACKGROUND, PAUSE_TEXT, EXIT_BTN, WHITE_TEXT, RESTART_BTN, RESUME_BTN, WIN_W

        # images 
        self.image = pygame.transform.scale(PAUSE_TEXT, (400, 90))
        self.resumeBtn = pygame.transform.scale(RESUME_BTN, (128, 128))
        self.restartBtn = pygame.transform.scale(RESTART_BTN, (128, 128))
        self.exitBtn = pygame.transform.scale(EXIT_BTN, (128, 128))
        
        # texts
        self.resumeBtnText = self.font.render("Resume [ESC]", True, WHITE_TEXT)
        self.restartBtnText = self.font.render("Restart [R]", True , WHITE_TEXT)
        self.exitBtnText = self.font.render("Exit [E]", True, WHITE_TEXT)

        # rects
        self.rect = self.image.get_rect()
        self.resumeBtnRect = self.resumeBtn.get_rect()
        self.restartBtnRect = self.restartBtn.get_rect()
        self.exitBtnRect = self.exitBtn.get_rect()

        # positions
        self.pos = ((WIN_W - self.image.get_width()) / 2, 30)
        self.resumeBtnPos = (((WIN_W / 3) - self.resumeBtn.get_width()) / 2, 300)
        self.restartBtnPos = ((WIN_W / 3) + ((WIN_W / 3) - self.restartBtn.get_width()) / 2, 300)
        self.exitBtnPos = ((WIN_W / 3) * 2 + ((WIN_W / 3) - self.exitBtn.get_width()) / 2, 300)
        self.resumeBtnTextPos = (((WIN_W / 3) - self.resumeBtnText.get_width()) / 2, 500)
        self.restartBtnTextPos = ((WIN_W / 3) + ((WIN_W / 3) - self.restartBtnText.get_width()) / 2, 500)
        self.exitBtnTextPos = ((WIN_W / 3) * 2 + ((WIN_W / 3) - self.exitBtnText.get_width()) / 2, 500)

        # update rects' positions
        self.resumeBtnRect.topleft = self.resumeBtnPos
        self.restartBtnRect.topleft = self.restartBtnPos
        self.exitBtnRect.topleft = self.exitBtnPos

    def show(self, window) -> None:
        window.blit(self.image, self.pos)
        window.blit(self.resumeBtn, self.resumeBtnPos)
        window.blit(self.restartBtn, self.restartBtnPos)
        window.blit(self.exitBtn, self.exitBtnPos)
        window.blit(self.restartBtnText, self.restartBtnTextPos)
        window.blit(self.resumeBtnText, self.resumeBtnTextPos)
        window.blit(self.exitBtnText, self.exitBtnTextPos)


class PauseCountdown():
    def __init__(self) -> None:
        from common import WHITE_TEXT, WIN_W

        self.font = pygame.font.Font("assets/VCR_OSD_MONO_1.001.ttf", 28)
        self.countdownText = self.font.render("Game will start in...", True, pygame.color.Color(WHITE_TEXT))
        self.countdownTextRect = self.countdownText.get_rect()
        self.countdownTextPos = ((WIN_W - self.countdownTextRect.width) / 2, 50)
        self.i = 0
    def countdown(self, window) -> None:
        from common import RESUME_COUNTDOWN_SPRITES, WIN_W, PAUSE_BACKGROUND

        self.image = RESUME_COUNTDOWN_SPRITES[int(self.i / 40)]
        self.rect = self.image.get_rect()
        self.x = int((WIN_W - self.rect.width) / 2)
        self.y = 90
        window.blit(PAUSE_BACKGROUND, (0, 0))
        window.blit(self.countdownText, self.countdownTextPos)
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
        from common import HIT_FX_SPRITE, MISS_FX_SPRITE
        from customTypes import HitState
        if self.alpha > 0:
            
            if self.t == HitState.Hit:
                self.img = HIT_FX_SPRITE
            elif self.t == HitState.Miss:
                self.img = MISS_FX_SPRITE
            self.img = self.img.convert_alpha()
            self.img.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
            self.alpha -= 20


class LowHPWarning():
    def __init__(self) -> None:
        from common import LOW_HP_WARNING_FX

        self.image = LOW_HP_WARNING_FX
        self.alpha = 255
        self.glowing = True
        self.hidden = False
    def update(self):
        if self.hidden:
            self.alpha = 255
            self.hidden = False

        if self.alpha >= 255:           
            self.glowing = False
        elif self.alpha <= 150:
            self.glowing = True
        
        if self.glowing:
            self.alpha += 18
        elif not self.glowing:
            self.alpha -= 18
    def hide(self):
        self.alpha = 0
        self.hidden = True
        
    def render(self, window):
        self.i = self.image.copy()
        self.i.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
        window.blit(self.i, (0, 0))

class ScoreDisp():
    def __init__(self, t) -> None:
        self.alpha = 255
        self.t = t

    def show(self):
        from common import LARGE_NOTE_SCORE, SMALL_NOTE_SCORE

        if self.alpha > 0:
            if self.t == "SmallNote":
                self.img = SMALL_NOTE_SCORE
            elif self.t == "LargeNote":
                self.img = LARGE_NOTE_SCORE
            self.rect = self.img.get_rect()
            self.img = self.img.convert_alpha()
            self.img.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
            self.alpha -= 20

