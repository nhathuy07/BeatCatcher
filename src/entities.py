### IMPORT STATEMENTS
from os import path as os_path

from pygame import init as pg_init
from pygame import display as pg_disp

from common import HIT_FX_SPRITE, MISS_FX_SPRITE

pg_init()
pg_disp.init()

### ANALYZER
class AudioAnalyzer():
    def __init__(self, fileName: str) -> None:

        self.fileName = fileName
        self.noteStartList = []
        self.smallNotesList = []
    def loadIntoLibrosa(self):
        print("Loading song...")
        # import files
        from subprocess import run as s_run
        from common import (
            BLANK_AUDIO
        )
        from utils import (
            concatenateAudio
        )
        from librosa import load as l_load
        from librosa.onset import onset_strength

        # song name
        self.songName = os_path.basename(self.fileName)
        # convert if not wav
        print("The song's file type is not WAV. Converting...")
        if not self.fileName.endswith(".wav"):
            s_run(args=['./ffmpeg.exe', '-i', self.fileName, "temp.wav"])
            self.fileName = "temp.wav"
        print("Converting finished!")
        # append file:
        concatenateAudio([BLANK_AUDIO, self.fileName])
        self.fileName = "temp2.wav"
        # load into librosa
        self.soundData, self.sampleRate = l_load(self.fileName)
        self.oenv = onset_strength(y=self.soundData, sr=self.sampleRate)

        return self.songName
    def calcBPM(self):
        from librosa.beat import tempo as l_tempo

        self.bpm = float(l_tempo(y=self.soundData, sr=self.sampleRate))
        return self.bpm
    
    def detectNotes(self):
        from librosa.onset import onset_detect, onset_backtrack
        from librosa import frames_to_time

        print("Generating notes...")
        self.noteStartList = onset_detect(y=self.soundData, sr=self.sampleRate, normalize=True, backtrack=True)
        self.noteEndList = onset_backtrack(self.noteStartList, self.oenv)
        
        self.noteStartList = frames_to_time(self.noteStartList, sr=self.sampleRate)
        #self.noteStartList: tuple = tuple(map(numberRounding,list(self.noteStartList)))

        self.noteEndList = frames_to_time(self.noteEndList, sr=self.sampleRate)
        #self.noteEndList: tuple = tuple(map(numberRounding,list(self.noteEndList)))
        self.noteEndList = tuple(self.noteEndList)
        self.noteStartList = tuple(self.noteStartList)
        return (self.noteStartList)
    
    def detectSmallNotes(self):
        from common import LONG_NOTE_MINIMUM_DURATION

        noteLength = 15/self.bpm
        smallNotesList= [] 
        for i in range(len(self.noteStartList) - 1):
            noteDuration = self.noteEndList[i + 1] - self.noteStartList[i]
            smallNoteGroup = []
            if noteDuration >= LONG_NOTE_MINIMUM_DURATION:
                t = self.noteStartList[i]
                while t < self.noteEndList[i + 1] - 60 / self.bpm:
                    t += noteLength
                    smallNoteGroup.append(t)
            smallNotesList.append(smallNoteGroup)
        return smallNotesList
    

### UI CODE
class MainMenu():
    def __init__(self) -> None:
        from pygame import transform as pg_transform
        from common import (
            RESUME_BTN,
            INFO_BTN,
            HELP_BTN,
            WIN_W,
            MENU_TITLE,
            WIN_H
        )
        
        # images
        self.playBtn = pg_transform.smoothscale(RESUME_BTN, (200, 200))
        self.aboutBtn = pg_transform.smoothscale(INFO_BTN, (50, 50))
        self.helpBtn = pg_transform.smoothscale(HELP_BTN, (50, 50))

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

class PauseMenu():
    def __init__(self) -> None:
        from pygame import font as pg_font
        from pygame import transform as pg_transform
        from common import (
            FONT2,
            PAUSE_TEXT,
            RESTART_BTN,
            RESUME_BTN,
            EXIT_BTN,
            WHITE_TEXT,
            WIN_W,

        )

        self.font = pg_font.Font(FONT2, 28)


        # images 
        self.image = pg_transform.scale(PAUSE_TEXT, (400, 90))
        self.resumeBtn = pg_transform.scale(RESUME_BTN, (128, 128))
        self.restartBtn = pg_transform.scale(RESTART_BTN, (128, 128))
        self.exitBtn = pg_transform.scale(EXIT_BTN, (128, 128))
        
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

class FailedScreen():
    def __init__(self) -> None:
        # import
        from common import (
            FONT2,
            RESTART_BTN,
            EXIT_BTN,
            WHITE_TEXT,
            WIN_W,
            FAILED_SCREEN_TITLE,
            GAME_OVER_SOUND,
        )
        from pygame import transform as pg_transform
        from pygame import mixer as pg_mixer
        from pygame import font as pg_font
        # fonts
        font = pg_font.Font(FONT2, 28)

        # buttons
        self.retryBtn = pg_transform.smoothscale(RESTART_BTN, (200, 200))
        self.exitBtn = pg_transform.smoothscale(EXIT_BTN, (200, 200))

        # texts
        self.retryTxt = font.render("Retry", True, WHITE_TEXT)
        self.exitTxt = font.render("Exit", True, WHITE_TEXT)

        # rects
        self.retryBtnRect = self.retryBtn.get_rect()
        self.exitBtnRect = self.exitBtn.get_rect()

        # positions
        self.retryBtnPos = ((WIN_W / 2 - self.retryBtn.get_width()) / 2, 230)
        self.exitBtnPos = ((WIN_W / 2) + (WIN_W /2 - self.exitBtn.get_width()) / 2, 230)
        self.titlePos = ((WIN_W - FAILED_SCREEN_TITLE.get_width()) / 2, 30)

        self.retryTxtPos = ((WIN_W / 2 - self.retryTxt.get_width()) / 2, self.retryBtn.get_height() + 260)
        self.exitTxtPos = ((WIN_W / 2) + (WIN_W / 2 - self.exitTxt.get_width()) / 2, self.exitBtn.get_height() + 260)
        # update rect pos
        self.retryBtnRect.topleft = self.retryBtnPos
        self.exitBtnRect.topleft = self.exitBtnPos

        # audio
        self.sound = pg_mixer.Sound(GAME_OVER_SOUND)

        # is audio played?
        self.audioPlayed = False
    def show(self, window):
        from common import BACKGROUND_IMAGE, PAUSE_BACKGROUND, FAILED_SCREEN_TITLE
        window.blit(BACKGROUND_IMAGE, (0, 0))
        window.blit(PAUSE_BACKGROUND, (0, 0))
        window.blit(FAILED_SCREEN_TITLE, self.titlePos)
        window.blit(self.retryBtn, self.retryBtnPos)
        window.blit(self.exitBtn, self.exitBtnPos)
        window.blit(self.exitTxt, self.exitTxtPos)
        window.blit(self.retryTxt, self.retryTxtPos)

    def playAudio(self):
        if not self.audioPlayed:
            self.sound.play(loops=0)
            self.audioPlayed = True

class ShowFinalScore():
    def __init__(self, ln, sn, scr, name):
        from common import (
            FONT,
            FONT2
        )
        from pygame import font as pg_font

        self.ln = ln
        self.sn = sn
        self.scr = scr
        self.name = name
        self.font = pg_font.Font(FONT, 40)
        self.font2 = pg_font.Font(FONT, 67)
        self.font3 = pg_font.Font(FONT2, 20)

        self.counterProg = 0

    def show(self, window):
            from common import (
                WHITE_TEXT,
                BACKGROUND_IMAGE,
                PAUSE_BACKGROUND,
                FINAL_SCORE_TITLE,
                WIN_W,
                LARGE_NOTE_SPRITE,
                SMALL_NOTE_SPRITE,
                WIN_H,
                TAP_PROMPT
            )

            self.counterProg += 0.03
            if self.counterProg >= 1:
                self.counterProg = 1
            
            self.lnDisp = self.font.render(f" x {int(self.ln * self.counterProg)}", True, WHITE_TEXT)
            self.snDisp = self.font.render(f" x {int(self.sn * self.counterProg)}", True, WHITE_TEXT)
            self.scrDisp = self.font2.render(f"{int(self.scr * self.counterProg)}", True, WHITE_TEXT)
            self.nameDisp = self.font3.render(self.name, True, WHITE_TEXT)

            window.blit(BACKGROUND_IMAGE, (0, 0))
            window.blit(PAUSE_BACKGROUND, (0, 0))

            window.blit(FINAL_SCORE_TITLE, ((WIN_W - FINAL_SCORE_TITLE.get_width()) / 2, 50))
            
            window.blit(self.nameDisp, ((WIN_W - self.nameDisp.get_width()) / 2, 175))
            
            window.blit(LARGE_NOTE_SPRITE, ((WIN_W / 2 - self.lnDisp.get_width() - LARGE_NOTE_SPRITE.get_width()) / 2, (WIN_H - LARGE_NOTE_SPRITE.get_height()) / 2 - 75))
            window.blit(self.lnDisp, ((WIN_W / 2 - self.lnDisp.get_width() + LARGE_NOTE_SPRITE.get_width()) / 2, (WIN_H - self.lnDisp.get_height()) / 2 - 75))

            window.blit(SMALL_NOTE_SPRITE, ((WIN_W / 2 - self.snDisp.get_width() - SMALL_NOTE_SPRITE.get_width()) / 2 + (WIN_W / 2), (WIN_H - SMALL_NOTE_SPRITE.get_height()) / 2 - 75))
            window.blit(self.snDisp, ((WIN_W / 2 - self.snDisp.get_width() + SMALL_NOTE_SPRITE.get_width()) / 2 + (WIN_W / 2), (WIN_H - self.snDisp.get_height()) / 2 - 75))

            window.blit(TAP_PROMPT, ((WIN_W - TAP_PROMPT.get_width()) / 2, WIN_H - 10 - TAP_PROMPT.get_height()))
            window.blit(self.scrDisp, ((WIN_W - self.scrDisp.get_width()) / 2, (WIN_H - self.scrDisp.get_height()) / 2 + 70))

class PauseCountdown():
    def __init__(self) -> None:
        from pygame import font as pg_font
        from common import (
            FONT2,
            WHITE_TEXT,
            WIN_W,
        )

        self.font = pg_font.Font(FONT2, 28)
        self.countdownText = self.font.render("Game will start in...", True, WHITE_TEXT)
        self.countdownTextRect = self.countdownText.get_rect()
        self.countdownTextPos = ((WIN_W - self.countdownTextRect.width) / 2, 50)
        self.i = 0
    def countdown(self, window) -> None:
        from common import (
            RESUME_COUNTDOWN_SPRITES,
            WIN_W,
            PAUSE_BACKGROUND
        )

        self.image = RESUME_COUNTDOWN_SPRITES[int(self.i / 40)]
        self.rect = self.image.get_rect()
        self.x = int((WIN_W - self.rect.width) / 2)
        self.y = 90
        window.blit(PAUSE_BACKGROUND, (0, 0))
        window.blit(self.countdownText, self.countdownTextPos)
        window.blit(self.image, (self.x, self.y))



### GAME OBJECTS
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

class BaseNote():
    def update(self, bpm, fps):
        from common import (
            PAD_Y_POS,
            SPEED_MULTIPLIER,
        )
        self.y += PAD_Y_POS / ((1 / SPEED_MULTIPLIER) / bpm) / fps

class LargeNote(BaseNote):
    def __init__(self, x, y):
        from common import LARGE_NOTE_SPRITE
        from pygame import rect as pg_rect

        self.x = x
        self.y = y
        self.image = LARGE_NOTE_SPRITE
        self.rect = pg_rect.Rect(14, 14, 52, 52)
        
class SmallNote(BaseNote):
    def __init__(self, x, y):
        from common import SMALL_NOTE_SPRITE

        self.x = x
        self.y = y
        self.image = SMALL_NOTE_SPRITE
        self.rect = self.image.get_rect()


### VISUAL EFFECTS
class Effect():
    def __init__(self, window, x, y, t, padX = None) -> None:
        from common import (
            HIT_FX_SPRITE, MISS_FX_SPRITE
        )
        from customTypes import HitState
        from pygame import BLEND_RGBA_MULT

        self.img = 0
        self.alpha = 255
        self.t = t
        self.x = x
        self.y = y
        self.padX = padX
        self.sprites = [HIT_FX_SPRITE, MISS_FX_SPRITE]
        self.hitState = HitState
        self.blend = BLEND_RGBA_MULT
    def update(self):

        if self.alpha > 0:
            
            if self.t == self.hitState.Hit:
                self.img = self.sprites[0]
            elif self.t == self.hitState.Miss:
                self.img = self.sprites[1]
            self.img = self.img.convert_alpha()
            self.img.fill((255, 255, 255, self.alpha), None, self.blend)
            self.alpha -= 20

class LowHPWarning():
    def __init__(self) -> None:
        from common import LOW_HP_WARNING_FX
        from pygame import BLEND_RGBA_MULT

        self.image = LOW_HP_WARNING_FX
        self.alpha = 255
        self.glowing = True
        self.hidden = False
        self.blend = BLEND_RGBA_MULT
    def update(self):
        if self.hidden:
            self.alpha = 255
            self.hidden = False

        if self.alpha >= 255:           
            self.glowing = False
        elif self.alpha <= 150:
            self.glowing = True
        
        if self.glowing:
            self.alpha += 13
        elif not self.glowing:
            self.alpha -= 13
    def hide(self):
        self.alpha = 0
        self.hidden = True
        
    def render(self, window):
        self.i = self.image.copy()
        self.i.fill((255, 255, 255, self.alpha), None, self.blend)
        window.blit(self.i, (0, 0))

class ScoreDisp():
    def __init__(self, t) -> None:
        from pygame import BLEND_RGBA_MULT
        from common import SMALL_NOTE_SCORE, LARGE_NOTE_SCORE

        self.alpha = 255
        self.t = t
        self.snScore = SMALL_NOTE_SCORE
        self.lnScore = LARGE_NOTE_SCORE
        self.blend = BLEND_RGBA_MULT

    def show(self):

        if self.alpha > 0:
            if self.t == "SmallNote":
                self.img = self.snScore
            elif self.t == "LargeNote":
                self.img = self.lnScore
            self.rect = self.img.get_rect()
            self.img = self.img.convert_alpha()
            self.img.fill((255, 255, 255, self.alpha), None, self.blend)
            self.alpha -= 20
