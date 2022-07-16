import os
from pygame import quit as pg_quit
from pygame import mixer as pg_mix
from pygame import rect as pg_rect
from pygame import init as pg_init
from pygame import display as pg_disp
from pygame import time as pg_time
from pygame import (
    DOUBLEBUF,
    HWACCEL,
    QUIT,
    MOUSEBUTTONDOWN,
    SCALED,
    K_e,
    K_ESCAPE,
    K_r,
    KEYDOWN
    
)
from pygame import font as pg_font
from pygame import event as pg_ev
from pygame import transform as pg_transform
from pygame.mouse import get_pos as pg_mouse_get_pos

def helpPage():
    print("Importing constants...")
    from common import WIN_W, WIN_H, WHITE_TEXT, FPS, PAUSE_BACKGROUND, FONT2, HELP_TEXT, GUIDE_TITLE, MAIN_MENU_BG, HELP_IMG, TAP_PROMPT

    display = pg_disp.set_mode((WIN_W, WIN_H), HWACCEL | DOUBLEBUF)
    clock = pg_time.Clock()

    # dark overlay
    darkOverlay = PAUSE_BACKGROUND
    font = pg_font.Font(FONT2, 20)

    texts = HELP_TEXT
    # guide title:
    guideTitleRect = GUIDE_TITLE.get_rect()
    # page count
    page = 0
    while True:
        for e in pg_ev.get():
            if e.type == QUIT:
                return None
            elif e.type == MOUSEBUTTONDOWN:
                page += 1
                if page >= len(HELP_TEXT):
                    return None
        display.blit(MAIN_MENU_BG, (0, 0))
        display.blit(darkOverlay, (0, 0))
        display.blit(GUIDE_TITLE, ((WIN_W - GUIDE_TITLE.get_width()) / 2, 20))
        
        # generate rect for image and text
        helpImgRect = HELP_IMG[page].get_rect()
        display.blit(HELP_IMG[page], ((WIN_W - HELP_IMG[page].get_width()) / 2, guideTitleRect.height + 30))
        

        _t = texts[page].split("|")
        spacing = 10
        for line in _t:
            lineRenderer = font.render(line, True, WHITE_TEXT)
            spacing += lineRenderer.get_rect().height
            display.blit(lineRenderer, ((WIN_W - lineRenderer.get_rect().width) / 2, guideTitleRect.height + spacing * 1.5 + helpImgRect.height))

        display.blit(TAP_PROMPT, ((WIN_W - TAP_PROMPT.get_width()) / 2, WIN_H - TAP_PROMPT.get_height() - 4))
        pg_disp.flip()
        clock.tick()
    
def licensePage():
    print("Importing constants...")
    from common import WIN_W, WIN_H, FONT2, PAUSE_BACKGROUND, VERSION_STRING, WHITE_TEXT, MENU_TITLE, LINK_COLOR, CWD, THIRD_PARTY_LIBS_LICENSE, ATTRIBUTION_TEXT, BACKGROUND_IMAGE, TAP_PROMPT, FPS, LICENSE
    from utils import textWrap
    display = pg_disp.set_mode((WIN_W, WIN_H), HWACCEL | DOUBLEBUF)
    clock = pg_time.Clock()
    font = pg_font.Font(FONT2, 22)
    font2 = pg_font.Font(FONT2, 22)

    font.set_bold(True)


    # dark overlay
    darkOverlay = PAUSE_BACKGROUND

    # game info
    name = font.render(f"BeatCatcher v{VERSION_STRING}", True, WHITE_TEXT)
    shortDesc = font2.render("A rhythm game that lets you play with your own song library.", True, WHITE_TEXT)
    copyrightText = font2.render("Copyright (C) 2022 Huy Nguyen", True, WHITE_TEXT)
    
    # resized menu title
    smallMenuTitle = pg_transform.smoothscale(MENU_TITLE, (MENU_TITLE.get_width() * 0.65, MENU_TITLE.get_height() * 0.65))
    
    # license info box
    left = 20
    top = 60 + smallMenuTitle.get_height() + name.get_rect().height * 2 + shortDesc.get_rect().height + copyrightText.get_rect().height
    width = WIN_W - 60
    height = WIN_H - top


    # links to third party software license file

    link1 = font.render("THIRD-PARTY SOFTWARE LICENSES", True, LINK_COLOR)
    link2 = font.render("THIRD-PARTY ASSETS ATTRIBUTION", True, LINK_COLOR)

    # link hitboxes
    link1Rect = link1.get_rect()
    link2Rect = link2.get_rect()

    while True:
        mouse = pg_mouse_get_pos()
        for e in pg_ev.get():
            if e.type == QUIT:
                return None
            elif e.type == MOUSEBUTTONDOWN:
                if link1Rect.collidepoint(mouse):
                    os.startfile(os.path.join(CWD, THIRD_PARTY_LIBS_LICENSE))
                elif link2Rect.collidepoint(mouse):
                    os.startfile(os.path.join(CWD, ATTRIBUTION_TEXT))
                else:
                    return None
        display.blit(BACKGROUND_IMAGE, (0, 0))
        display.blit(darkOverlay, (0, 0))
        display.blit(smallMenuTitle, ((WIN_W - smallMenuTitle.get_width()) / 2, 30))
        display.blit(name, (20, 27 + smallMenuTitle.get_height()) )
        display.blit(shortDesc, (20, 27 + smallMenuTitle.get_height() + name.get_rect().height * 1.5))
        display.blit(copyrightText, (20, 27 + smallMenuTitle.get_height() + name.get_rect().height * 1.5 + shortDesc.get_rect().height * 1.5))
        display.blit(TAP_PROMPT, ((WIN_W - TAP_PROMPT.get_width()) / 2, WIN_H - 20 - TAP_PROMPT.get_height()))
        y = 0

        for l in LICENSE:
            y += textWrap(display, l, WHITE_TEXT, pg_rect.Rect(left, top + y, width, height), font2, True, None)

        
        link1Rect.topleft = (20, 42 + y + smallMenuTitle.get_height() + name.get_rect().height * 1.5 + shortDesc.get_rect().height * 1.5 + copyrightText.get_height() * 1.5)
        link2Rect.topleft = (WIN_W - 20 - link2.get_width(), 42 + y + smallMenuTitle.get_height() + name.get_rect().height * 1.5 + shortDesc.get_rect().height * 1.5 + copyrightText.get_height() * 1.5)

        display.blit(link1, link1Rect.topleft)
        display.blit(link2, link2Rect.topleft)
        
        pg_disp.flip()
        clock.tick(FPS)
def mainMenu():
    print("Importing constants....")
    from common import WIN_W, WIN_H, PAUSE_BACKGROUND, LOADING_ICON, FPS, MUSIC_FOLDER
    import tkinter.filedialog
    print("Importing MainMenu module")
    from entities import MainMenu
    from customTypes import Part
    
    _mainMenu = MainMenu()
    display = pg_disp.set_mode((WIN_W, WIN_H), HWACCEL)
    clock = pg_time.Clock()
    while True:
        for e in pg_ev.get():
            if e.type == QUIT:
                return None, Part.Exit
            elif e.type == MOUSEBUTTONDOWN:
                mousePos = pg_mouse_get_pos()
                if _mainMenu.playBtnRect.collidepoint(mousePos):
                    f = tkinter.filedialog.askopenfilename(title = "Select a song to play...", initialdir=MUSIC_FOLDER)
                    if f == "" or f == None:
                        pass
                    else:
                        display.blit(PAUSE_BACKGROUND, (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - LOADING_ICON.get_width()) / 2, (WIN_H - LOADING_ICON.get_width()) / 2))
                        pg_disp.flip()
                        return f, Part.Play
                elif _mainMenu.helpBtnRect.collidepoint(mousePos):
                    return None, Part.Help
                elif _mainMenu.aboutBtnRect.collidepoint(mousePos):
                    return None, Part.About
        
        _mainMenu.show(display)
        pg_disp.flip()
        clock.tick(FPS)

def analyze(f):
    print("Loading analyzer...")
    from entities import AudioAnalyzer
    print("Analyzer loaded! Finding notes...")
    audioObj = AudioAnalyzer(f)
    songName = audioObj.loadIntoLibrosa()
    noteStartList = audioObj.detectNotes()
    bpm = audioObj.calcBPM()
    smallNoteStartList = audioObj.detectSmallNotes()

    # chorus detection feature will be implemented in the future
    chorusStartTime = None

    return songName, noteStartList, smallNoteStartList, chorusStartTime, bpm

def session(f, songName, noteStartList, smallNoteStartList, bpm):
    print("Loading constants...")
    from common import WIN_W, WIN_H, PAD_Y_POS, SPEED_MULTIPLIER, FONT, FONT2, LOADING_ICON, PAUSE_BACKGROUND, BACKGROUND_IMAGE, FPS, WHITE_TEXT, LARGE_NOTE_SPRITE
    from common import HP_DEPLETION_RATE, LINK_COLOR
    print("Loading entities...")
    from entities import LargeNote, SmallNote, PauseMenu, PauseCountdown, Pad, Effect, ScoreDisp, LowHPWarning
    from utils import randomRange
    from customTypes import PauseState, ExitReason, HitState
    import random
    from os import path as os_path
    from os import remove as os_rem

    pg_mix.music.load("temp2.wav")
    # create pygame window
    display = pg_disp.set_mode((WIN_W, WIN_H), HWACCEL | SCALED, 0, 0, 1)

    # create pygame clock object
    clock = pg_time.Clock()

    largenotes = []
    smallnotes = []

    prevX = None

    # generate large note
    print("Generating level...")
    for n in noteStartList:
        if prevX == None:
            prevX = random.randint(10, WIN_W - 80)
            note = LargeNote(prevX, PAD_Y_POS - (LARGE_NOTE_SPRITE.get_height() / 2) - ((PAD_Y_POS - LARGE_NOTE_SPRITE.get_height() / 2) / ((1 / SPEED_MULTIPLIER) / bpm) * n))
            largenotes.append(note)
        else:
            if abs(noteStartList[noteStartList.index(n) - 1] - n) <= 0.008 and noteStartList.index(n) >= 1:
                noteStartList.remove(n)
            else:
                prevX = randomRange(prevX, 280)
            note = LargeNote(prevX, PAD_Y_POS - ((PAD_Y_POS) / ((1 / SPEED_MULTIPLIER) / bpm) * n))
            largenotes.append(note)


    pad = Pad(100, PAD_Y_POS)

    # generate small notes
    n = 0
    for n in range(len(smallNoteStartList)):
        x = largenotes[n].x
        prevX = None
        for n2 in smallNoteStartList[n]:
            if prevX == None:
                pass
            else:
                x = randomRange(prevX, 46)
            note = SmallNote(x + 16.5, PAD_Y_POS - ((PAD_Y_POS) / ((1 / SPEED_MULTIPLIER) / bpm) * n2))
            prevX = x

            smallnotes.append(note)

    notes = [*largenotes, *smallnotes]
    fx = []
    addScoreFx = None
    # init pause menu
    pauseText = PauseMenu()
    ctd = PauseCountdown()

    
    running = True
    paused = PauseState.NotPausing
    pauseTextDrawn = False

    largeNoteCount = 0
    smallNoteCount = 0
    score = 0
    hp = 80

    # init fonts
    font = pg_font.Font(FONT, 30)
    font2 = pg_font.Font(FONT2, 15)

    # init warning var
    warning = LowHPWarning()

    pg_mix.music.play()
    while running:
        
        # fill display with black
        events = pg_ev.get()
        mouseX, mouseY = pg_mouse_get_pos()
        
        for e in events:
            # keypress
            if e.type == KEYDOWN:
                # esc pressed
                if e.key == K_ESCAPE:
                    if paused == PauseState.NotPausing:
                        paused = PauseState.Pausing
                        pauseTextDrawn = False
                    elif paused == PauseState.Pausing:
                        paused = PauseState.Waiting
                # r key pressed
                elif e.key == K_r:
                    if paused == PauseState.Pausing:
                        pg_mix.music.stop()
                        pg_mix.music.unload()
                        # loading icon
                        loadingIconRect = LOADING_ICON.get_rect()
                        display.blit(PAUSE_BACKGROUND, (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - loadingIconRect.width) / 2, (WIN_H - loadingIconRect.height) / 2))
                        pg_disp.flip()
                        return ExitReason.Restart, None, None, None
                        
                elif e.key == K_e and paused == PauseState.Pausing:
                    pg_mix.music.stop()
                    pg_mix.music.unload()
                    return ExitReason.Exit, None, None, None

            # game exit
            elif e.type == QUIT:
                pg_mix.music.stop()
                pg_mix.music.unload()
                for i in range["temp.wav", "temp2.wav"]:
                    if os_path.exists(i):
                        os_rem(i)

                return ExitReason.Exit, None, None, None
                

            #mouse click
            elif e.type == MOUSEBUTTONDOWN:
                if paused == PauseState.Pausing:
                    # click on resume btn to unpause the game
                    if pauseText.resumeBtnRect.collidepoint(mouseX, mouseY):
                        paused = PauseState.Waiting
                        pauseTextDrawn = False
                    # click on restart btn to restart the game
                    elif pauseText.restartBtnRect.collidepoint(mouseX, mouseY):
                        pg_mix.music.stop()
                        pg_mix.music.unload()
                        loadingIconRect = LOADING_ICON.get_rect()
                        display.blit(PAUSE_BACKGROUND, (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - loadingIconRect.width) / 2, (WIN_H - loadingIconRect.height) / 2))
                        pg_disp.flip()
                        return ExitReason.Restart, None, None, None
                    elif pauseText.exitBtnRect.collidepoint(mouseX, mouseY):
                        pg_mix.music.stop()
                        pg_mix.music.unload()
                        return ExitReason.Exit, None, None, None
        
        # game is running
        if paused == PauseState.NotPausing:
            display.blit(BACKGROUND_IMAGE, (0, 0))
            if mouseX != pad.x:
                pad.x = mouseX
            
            for n in notes:
                if clock.get_fps() != 0:
                    n.update(bpm, clock.get_fps())
                else:
                    n.update(bpm, FPS)
                # if note is in screen
                if n.y > 0 - n.rect.height:
                # if note is catched
                    if  PAD_Y_POS + pad.rect.height * 0.8 >= (n.y + n.rect.height) >= PAD_Y_POS and (pad.x - n.rect.width + 20 <= n.x <= pad.x + pad.rect.width - 20):
                        if type(n).__name__ == "LargeNote":
                            largeNoteCount += 1
                            fx.append(Effect(display, n.x + 14 + n.rect.width / 2 - 25, PAD_Y_POS - 50, HitState.Hit, padX=pad.x))
                            addScoreFx = ScoreDisp("LargeNote")
                            hp += HP_DEPLETION_RATE * 0.25
                        elif type(n).__name__ == "SmallNote":
                            smallNoteCount += 1
                            fx.append(Effect(display, n.x + n.rect.width / 2 - 25, PAD_Y_POS - 50, HitState.Hit, padX=pad.x))
                            addScoreFx = ScoreDisp("SmallNote")
                            hp += HP_DEPLETION_RATE * 0.1
                        notes.remove(n)
                    # if note is missed
                    elif (n.y + n.rect.height >= WIN_H + 20):
                        if type(n).__name__ == "LargeNote":
                            fx.append(Effect(display, n.x + 14 + n.rect.width / 2 - 25, WIN_H - 30, HitState.Miss))
                        elif type(n).__name__ == "SmallNote":
                            fx.append(Effect(display, n.x + n.rect.width / 2 - 25, WIN_H - 30, HitState.Miss))
                        hp -= HP_DEPLETION_RATE
                        notes.remove(n)
                    else:
                        display.blit(n.image, (n.x, n.y))
            
            for f in fx:
                if f.alpha > 0:
                    f.update()
                    if f.t == HitState.Hit:
                        display.blit(f.img, (f.x - f.padX + pad.x, f.y))
                    elif f.t == HitState.Miss:
                        display.blit(f.img, (f.x, f.y))
                else:
                    fx.remove(f)
            
            if addScoreFx != None and addScoreFx.alpha > 0:
                addScoreFx.show()
                display.blit(addScoreFx.img, (pad.x + pad.rect.width / 2 - addScoreFx.rect.width / 2, PAD_Y_POS - addScoreFx.rect.height - 30))


            if hp > 100:
                hp = 100
            elif 100 >= hp > 35:
                warning.hide()
            elif 35 >= hp >= 0:
                warning.update()
            elif 0 > hp:
                pg_mix.music.stop()
                pg_mix.music.unload()
                return ExitReason.Failed, None, None, None


            score = largeNoteCount * 200 + smallNoteCount * 100
            scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
            hpDisp = font.render(f"{round(hp)}%", True, LINK_COLOR)
            songNameDisp = font2.render(songName, True, WHITE_TEXT)

            if not warning.hidden:
                warning.render(display)
            display.blit(scoreDisp, (10, 10))
            display.blit(songNameDisp, (10, WIN_H - 30))
            display.blit(hpDisp, (WIN_W - hpDisp.get_width() - 10, 10))

            pad.render(display)
        elif paused == PauseState.Pausing:
            if not pauseTextDrawn:
                pg_mix.music.pause()
                scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
                songNameDisp = font2.render(songName, True, WHITE_TEXT)
                display.blit(scoreDisp, (10, 10))
                display.blit(songNameDisp, (10, WIN_H - 30))
                display.blit(PAUSE_BACKGROUND, (0, 0)) 
                
                pauseText.show(display)
                pauseTextDrawn = True
                
            
        elif paused == PauseState.Waiting:
            if ctd.i <= 100:
                display.blit((BACKGROUND_IMAGE), (0, 0))
                for n in notes:
                    display.blit(n.image, (n.x, n.y))
                pad.render(display)
                ctd.i += 1
                ctd.countdown(display)
            else:
                pg_mix.music.unpause()
                paused = PauseState.NotPausing
                ctd.i = 0

        # exit game if window is closed or song is ended
        if not pg_mix.music.get_busy() and paused == PauseState.NotPausing:
            
            notes = []
            display.blit((BACKGROUND_IMAGE), (0, 0))
            scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
            songNameDisp = font2.render(songName, True, WHITE_TEXT)
            pg_mix.music.stop()
            pg_mix.music.unload()
            return ExitReason.Finish, smallNoteCount, largeNoteCount, score
        
        
        
        pg_disp.flip()
        clock.tick(FPS)

def showFinalScore(ln, sn, scr, name):
    from entities import ShowFinalScore
    from common import FPS, WIN_H, WIN_W
    display = pg_disp.set_mode((WIN_W, WIN_H), HWACCEL)
    showFinalScore = ShowFinalScore(ln, sn, scr, name)
    clock = pg_time.Clock()
    while 1:
        for e in pg_ev.get():
            if e.type == MOUSEBUTTONDOWN or e.type == QUIT:
                return None
        showFinalScore.show(display)
        pg_disp.flip()
        clock.tick(FPS)

def failedScreen():
    from entities import FailedScreen
    from common import WIN_H, WIN_W, FPS, PAUSE_BACKGROUND, LOADING_ICON
    from customTypes import ExitReason

    display = pg_disp.set_mode((WIN_W, WIN_H))
    clock = pg_time.Clock()
    failedScreen = FailedScreen()
    while 1:
        for e in pg_ev.get():
            if e.type == QUIT:
                break
            elif e.type == MOUSEBUTTONDOWN:
                mouse = pg_mouse_get_pos()
                if failedScreen.exitBtnRect.collidepoint(mouse):
                    return ExitReason.Exit
                elif failedScreen.retryBtnRect.collidepoint(mouse):
                    display.blit(PAUSE_BACKGROUND, (0, 0))
                    display.blit(LOADING_ICON, ((WIN_W - LOADING_ICON.get_width()) / 2, (WIN_H - LOADING_ICON.get_height()) / 2))
                    pg_disp.flip()
                    return ExitReason.Restart
        failedScreen.playAudio()
        failedScreen.show(display)
        pg_disp.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    
    from customTypes import ExitReason, Part
    from common import AUDIO_FREQ, AUDIO_CHANNELS, AUDIO_BUFFER_SIZE
    pg_mix.pre_init(AUDIO_FREQ, 16, AUDIO_CHANNELS, AUDIO_BUFFER_SIZE)

    pg_init()
    pg_ev.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN])
    # display file dialog
    while True:
        f, part = mainMenu()
        if part == Part.Play:
            while True:
                name, n, sn, cst, bpm = analyze(f)
                r, sn, ln, scr = session(f, name, n, sn, bpm)

                for i in ["temp.wav", "temp2.wav"]:
                    if os.path.exists(i):
                        os.remove(i)
                if r == ExitReason.Exit:         
                    break
                elif r == ExitReason.Finish:
                    showFinalScore(ln, sn, scr, name)
                    break
                elif r == ExitReason.Restart:
                    pass
                elif r == ExitReason.Failed:
                    failed = failedScreen()
                    if failed == ExitReason.Exit:
                        break
                    elif failed == ExitReason.Restart:
                        pass
        elif part == Part.About:
            licensePage()
        elif part == Part.Help:
            helpPage()
        elif part == Part.Exit:   
            break
        
    pg_quit()
    
    quit()