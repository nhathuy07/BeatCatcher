import os
import pygame

from time import time
print("Importing utils...")
from utils import cleanup, randomRange, textWrap, open_file_default_app, open_file_dialog

#from entities import AudioAnalyzer, LargeNote, Pad, PauseCountdown, PauseMenu, ScoreDisp, SmallNote, Effect
print("Importing filedialog...")
# import tkinter.filedialog
print("Importing random...")
import random
print("Importing custom types...")
from customTypes import Part, ExitReason, PauseState, HitState
from common import BUFFER_SEC

pygame.init()
pygame.display.init()

def helpPage():
    print("Importing constants...")
    from common import WIN_W, WIN_H, WHITE_TEXT, FPS, PAUSE_BACKGROUND, FONT2, HELP_TEXT, GUIDE_TITLE, MAIN_MENU_BG, HELP_IMG, TAP_PROMPT
    
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWSURFACE)
    clock = pygame.time.Clock()

    # dark overlay
    darkOverlay = pygame.image.load(PAUSE_BACKGROUND)
    font = pygame.font.Font(FONT2, 20)

    texts = HELP_TEXT
    # guide title:
    guideTitleRect = GUIDE_TITLE.get_rect()
    # page count
    page = 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            elif e.type == pygame.MOUSEBUTTONDOWN:
                page += 1
                if page >= len(HELP_TEXT):
                    return None
        display.blit(MAIN_MENU_BG, (0, 0))
        display.blit(darkOverlay, (0, 0))
        display.blit(GUIDE_TITLE, ((WIN_W - guideTitleRect.width) / 2, 20))
        
        # generate rect for image and text
        helpImgRect = HELP_IMG[page].get_rect()
        display.blit(HELP_IMG[page], ((WIN_W - helpImgRect.width) / 2, guideTitleRect.height + 30))
        

        _t = texts[page].split("|")
        spacing = 10
        for line in _t:
            lineRenderer = font.render(line, True, WHITE_TEXT)
            spacing += lineRenderer.get_rect().height
            display.blit(lineRenderer, ((WIN_W - lineRenderer.get_rect().width) / 2, guideTitleRect.height + spacing * 1.5 + helpImgRect.height))

        display.blit(TAP_PROMPT, ((WIN_W - TAP_PROMPT.get_width()) / 2, WIN_H - TAP_PROMPT.get_height() - 4))
        pygame.display.flip()
        clock.tick(FPS)
    
def licensePage():
    print("Importing constants...")
    from common import WIN_W, WIN_H, FONT2, PAUSE_BACKGROUND, VERSION_STRING, WHITE_TEXT, MENU_TITLE, LINK_COLOR, CWD, THIRD_PARTY_LIBS_LICENSE, ATTRIBUTION_TEXT, BACKGROUND_IMAGE, TAP_PROMPT, FPS, LICENSE
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWSURFACE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT2, 22)
    font2 = pygame.font.Font(FONT2, 22)

    font.set_bold(True)


    # dark overlay
    darkOverlay = pygame.image.load(PAUSE_BACKGROUND)

    # game info
    name = font.render(f"BeatCatcher v{VERSION_STRING}", True, WHITE_TEXT)
    shortDesc = font2.render("A rhythm game that lets you play with your own song library.", True, WHITE_TEXT)
    copyrightText = font2.render("Copyright (C) 2022 Huy Nguyen", True, WHITE_TEXT)
    
    # resized menu title
    smallMenuTitle = pygame.transform.smoothscale(MENU_TITLE, (MENU_TITLE.get_width() * 0.65, MENU_TITLE.get_height() * 0.65))
    
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
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if link1Rect.collidepoint(mouse):
                    open_file_default_app(os.path.join(CWD, THIRD_PARTY_LIBS_LICENSE))
                elif link2Rect.collidepoint(mouse):
                    open_file_default_app(os.path.join(CWD, ATTRIBUTION_TEXT))
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
            y += textWrap(display, l, WHITE_TEXT, pygame.rect.Rect(left, top + y, width, height), font2, True, None)

        
        link1Rect.topleft = (20, 42 + y + smallMenuTitle.get_height() + name.get_rect().height * 1.5 + shortDesc.get_rect().height * 1.5 + copyrightText.get_height() * 1.5)
        link2Rect.topleft = (WIN_W - 20 - link2.get_width(), 42 + y + smallMenuTitle.get_height() + name.get_rect().height * 1.5 + shortDesc.get_rect().height * 1.5 + copyrightText.get_height() * 1.5)

        display.blit(link1, link1Rect.topleft)
        display.blit(link2, link2Rect.topleft)
        
        pygame.display.flip()
        clock.tick(FPS)
def mainMenu():
    print("Importing constants....")
    from common import WIN_W, WIN_H, MENU_TITLE, RESUME_BTN, INFO_BTN, HELP_BTN, PAUSE_BACKGROUND, LOADING_ICON, MAIN_MENU_BG, FPS, MUSIC_FOLDER
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWSURFACE)
    clock = pygame.time.Clock()
    
    #title
    titleRect = MENU_TITLE.get_rect()

    #play btn
    playBtn = pygame.transform.smoothscale(pygame.image.load(RESUME_BTN), (200, 200))
    playBtnRect = playBtn.get_rect()

    #info btn
    infoBtn = pygame.transform.smoothscale(pygame.image.load(INFO_BTN), (50, 50))
    infoBtnRect = infoBtn.get_rect()

    #help btn
    helpBtn = pygame.transform.smoothscale(pygame.image.load(HELP_BTN), (50, 50))
    helpBtnRect = helpBtn.get_rect()

    # dark overlay
    dark_overlay = pygame.image.load(PAUSE_BACKGROUND)

    # loading icon
    loadingIconRect = LOADING_ICON.get_rect()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None, Part.Exit
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if playBtnRect.collidepoint(mousePos):

                    f = open_file_dialog(title = "Select a song to play...", initialdir=MUSIC_FOLDER)
                    if f == "" or f == None:
                        pass
                    else:
                        display.blit(dark_overlay, (0, 0))
                        display.blit(dark_overlay, (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - loadingIconRect.width) / 2, (WIN_H - loadingIconRect.height) / 2))
                        pygame.display.flip()
                        return f, Part.Play
                elif helpBtnRect.collidepoint(mousePos):
                    return None, Part.Help
                elif infoBtnRect.collidepoint(mousePos):
                    return None, Part.About
        display.blit(MAIN_MENU_BG, (0, 0))
        display.blit(MENU_TITLE, ((WIN_W - titleRect.width) / 2, 40))
        display.blit(playBtn, ((WIN_W - playBtnRect.width) / 2, 240))
        display.blit(infoBtn, (30, WIN_H - 20 - infoBtnRect.height))
        display.blit(helpBtn, (60 + helpBtnRect.width, WIN_H - 20 - helpBtnRect.height))
        
        playBtnRect.topleft = ((WIN_W - playBtnRect.width) / 2, 240)
        infoBtnRect.topleft = (30, WIN_H - 20 - infoBtnRect.height)
        helpBtnRect.topleft = (60 + helpBtnRect.width, WIN_H - 20 - helpBtnRect.height)

        pygame.display.flip()
        clock.tick(FPS)

def analyze(f):
    print("Loading analyzer...")
    from entities import AudioAnalyzer
    audioObj = AudioAnalyzer(f)
    print("load into librosa")
    duration, songName, filepath, converted = audioObj.loadIntoLibrosa()
    print("detecting notes")
    noteStartList = audioObj.detectNotes()
    print("detecting small notes")
    smallNoteStartList = audioObj.detectSmallNotes()
    print("detecting finished!")

    # chorus detection feature will be implemented in the future
    chorusStartTime = None
    
    # print("creating mixer object")
    # audioObj.createPygameMixerObj()
    bpm = audioObj.calcBPM()

    print("analyzation finished!")

    return duration, songName, noteStartList, smallNoteStartList, chorusStartTime, bpm, filepath, converted

def session(f, duration, songName, noteStartList, smallNoteStartList, _, bpm, filepath):
    print("Loading constants...")
    from common import WIN_W, WIN_H, PAD_Y_POS, SPEED_MULTIPLIER, FONT, FONT2, LOADING_ICON, PAUSE_BACKGROUND, BACKGROUND_IMAGE, FPS, WHITE_TEXT
    print("Loading entities...")
    from entities import LargeNote, SmallNote, PauseMenu, PauseCountdown, Pad, Effect, ScoreDisp

    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    
    # pygame.mixer.music.play()
    # pygame.mixer.music.load("temp2.wav")
    # create pygame window
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWSURFACE)

    # create pygame clock object
    clock = pygame.time.Clock()

    largenotes = []
    smallnotes = []

    prevX = None

    # generate large note
    for n in noteStartList:
        if n <= duration:
            if prevX == None:
                prevX = random.randint(10, WIN_W - 80)
                note = LargeNote(prevX, PAD_Y_POS - ((PAD_Y_POS) / ((1 / SPEED_MULTIPLIER) / bpm) * n))
                largenotes.append(note)
            else:
                if abs(noteStartList[noteStartList.index(n) - 1] - n) <= 0.008 and noteStartList.index(n) >= 1:
                    noteStartList.remove(n)
                else:
                    prevX = randomRange(prevX, 280)
                note = LargeNote(prevX, PAD_Y_POS - ((PAD_Y_POS) / ((1 / SPEED_MULTIPLIER) / bpm) * n))
                largenotes.append(note)
        else:
            break

    pad = Pad(100, PAD_Y_POS)

    # generate small notes
    n = 0
    for n in range(len(smallNoteStartList)):
        x = largenotes[n].x
        prevX = None
        for n2 in smallNoteStartList[n]:
            if prevX == None:
                note = SmallNote(x + 16.5, PAD_Y_POS - ((PAD_Y_POS) / ((1 / SPEED_MULTIPLIER) / bpm) * n2))
                prevX = x
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

    # init fonts
    font = pygame.font.Font(FONT, 30)
    font2 = pygame.font.Font(FONT2, 15)


    
    game_start_time = time()
    buffer_sec = BUFFER_SEC
    buffer_used = False
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0)
    
    while running:

        if not buffer_used:   
            if time() - game_start_time >= buffer_sec:
                
                pygame.mixer.music.set_pos(0)
                pygame.mixer.music.set_volume(1)
                buffer_used = True
        
        # fill display with black
        events = pygame.event.get()
        mouseX, mouseY = pygame.mouse.get_pos()

        
        
        for e in events:
            # keypress
            if e.type == pygame.KEYDOWN:
                # esc pressed
                if e.key == pygame.K_ESCAPE:
                    if paused == PauseState.NotPausing:
                        paused = PauseState.Pausing
                        pauseTextDrawn = False
                    elif paused == PauseState.Pausing:
                        paused = PauseState.Waiting
                # r key pressed
                elif e.key == pygame.K_r:
                    if paused == PauseState.Pausing:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        # loading icon
                        loadingIconRect = LOADING_ICON.get_rect()
                        display.blit(pygame.image.load(PAUSE_BACKGROUND), (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - loadingIconRect.width) / 2, (WIN_H - loadingIconRect.height) / 2))
                        pygame.display.flip()
                        return ExitReason.Restart, None, None, None
                        
                elif e.key == pygame.K_e and paused == PauseState.Pausing:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    return ExitReason.Exit, None, None, None

            # game exit
            elif e.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                cleanup("temp.wav")
                cleanup("temp2.wav")
                return ExitReason.Exit, None, None, None
                

            #mouse click
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if paused == PauseState.Pausing:
                    # click on resume btn to unpause the game
                    if pauseText.resumeBtnRect.collidepoint(mouseX, mouseY):
                        paused = PauseState.Waiting
                        pauseTextDrawn = False
                    # click on restart btn to restart the game
                    elif pauseText.restartBtnRect.collidepoint(mouseX, mouseY):
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        loadingIconRect = LOADING_ICON.get_rect()
                        display.blit(pygame.image.load(PAUSE_BACKGROUND), (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - loadingIconRect.width) / 2, (WIN_H - loadingIconRect.height) / 2))
                        pygame.display.flip()
                        return ExitReason.Restart, None, None, None
                    elif pauseText.exitBtnRect.collidepoint(mouseX, mouseY):
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        return ExitReason.Exit, None, None, None

        if paused == PauseState.NotPausing:
            display.blit(BACKGROUND_IMAGE, (0, 0))
            pad.x = mouseX
            
            for n in notes:
                if clock.get_fps() != 0 or clock.get_fps() > FPS:
                    n.update(bpm, clock.get_fps())
                else:
                    n.update(bpm, FPS)
                if (PAD_Y_POS + pad.rect.height / 2 >= n.y + n.rect.height >= PAD_Y_POS and (pad.x - n.rect.width + 10 <= n.x <= pad.x + pad.rect.width - 10)):
                    if type(n).__name__ == "LargeNote":
                        largeNoteCount += 1
                        fx.append(Effect(display, n.x + 14 + n.rect.width / 2 - 25, PAD_Y_POS - 50, HitState.Hit, padX=pad.x))
                        addScoreFx = ScoreDisp("LargeNote")
                    elif type(n).__name__ == "SmallNote":
                        smallNoteCount += 1
                        fx.append(Effect(display, n.x + n.rect.width / 2 - 25, PAD_Y_POS - 50, HitState.Hit, padX=pad.x))
                        addScoreFx = ScoreDisp("SmallNote")
                    notes.remove(n)
                elif (n.y + n.rect.height >= WIN_H + 20):
                    if type(n).__name__ == "LargeNote":
                        fx.append(Effect(display, n.x + 14 + n.rect.width / 2 - 25, WIN_H - 30, HitState.Miss))
                    elif type(n).__name__ == "SmallNote":
                        fx.append(Effect(display, n.x + n.rect.width / 2 - 25, WIN_H - 30, HitState.Miss))
                    notes.remove(n)
                else:
                    display.blit(n.image, (n.x, n.y))
            
            for f in fx:
                if f.alpha > 0:
                    f.update()
                    if f.t == HitState.Hit:
                        display.blit(f.img, (f.x - f.padX + pad.x, f.y))
                    else:
                        display.blit(f.img, (f.x, f.y))
                else:
                    fx.remove(f)
            
            if addScoreFx != None and addScoreFx.alpha > 0:
                addScoreFx.show()
                display.blit(addScoreFx.img, (pad.x + pad.rect.width / 2 - addScoreFx.rect.width / 2, PAD_Y_POS - addScoreFx.rect.height - 30))

            score = largeNoteCount * 200 + smallNoteCount * 100
            scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
            songNameDisp = font2.render(songName, True, pygame.color.Color(WHITE_TEXT))
    
            pad.render(display)
        elif paused == PauseState.Pausing:
            if not pauseTextDrawn:
                pygame.mixer.music.pause()
                display.blit(pygame.image.load(PAUSE_BACKGROUND), (0, 0)) 
                scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
                songNameDisp = font2.render(songName, True, pygame.color.Color(WHITE_TEXT))
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
                pygame.mixer.music.unpause()
                paused = PauseState.NotPausing
                ctd.i = 0

        # exit game if window is closed or song is ended
        if not pygame.mixer.music.get_busy() and paused == PauseState.NotPausing:
            
            notes = []
            display.blit((BACKGROUND_IMAGE), (0, 0))
            scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
            songNameDisp = font2.render(songName, True, pygame.color.Color(WHITE_TEXT))
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            return ExitReason.Finish, smallNoteCount, largeNoteCount, score
        
        
        display.blit(scoreDisp, (10, 10))
        display.blit(songNameDisp, (10, WIN_H - 30))
        pygame.display.flip()
        clock.tick(FPS)

def showFinalScore(ln, sn, scr, name):
    from common import WIN_W, WIN_H, FONT, PAUSE_BACKGROUND, FONT2, BACKGROUND_IMAGE, WHITE_TEXT, TAP_PROMPT, FINAL_SCORE_TITLE, FPS
    from entities import LargeNote, SmallNote

    lnIcon = LargeNote(0, 0)
    snIcon = SmallNote(0, 0)

    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWSURFACE)
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(FONT, 40)
    font2 = pygame.font.Font(FONT, 63)
    font3 = pygame.font.Font(FONT2, 20)

    lnCounter = 0
    snCounter = 0
    scrCounter = 0

    dark_overlay = pygame.image.load(PAUSE_BACKGROUND)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.QUIT:
                return None
        display.blit(BACKGROUND_IMAGE, (0, 0))
        display.blit(dark_overlay, (0, 0))
        if lnCounter < ln:
            lnCounter += 2
        elif lnCounter >= ln:
            lnCounter = ln
        
        if snCounter < sn:
            snCounter += 2
        elif snCounter >= sn:
            snCounter = sn
        
        if scrCounter < scr:
            scrCounter += int(scr * 0.03)
        elif scrCounter >= scr:
            scrCounter = scr
        
        lnDisp = font.render(f" x {lnCounter}", True, WHITE_TEXT)
        snDisp = font.render(f" x {snCounter}", True, WHITE_TEXT)
        scrDisp = font2.render(f"{scrCounter}", True, WHITE_TEXT)
        nameDisp = font3.render(name, True, WHITE_TEXT)

        lnDispRect = lnDisp.get_rect()
        snDispRect = snDisp.get_rect()
        scrDispRect = scrDisp.get_rect()
        nameDispRect = nameDisp.get_rect()
        promptRect = TAP_PROMPT.get_rect()
        titleRect = FINAL_SCORE_TITLE.get_rect()

        display.blit(FINAL_SCORE_TITLE, ((WIN_W - titleRect.width) / 2, 50))
        display.blit(nameDisp, ((WIN_W - nameDispRect.width) / 2, 175))
        display.blit(lnIcon.image, ((WIN_W / 2 - lnIcon.rect.width - lnDispRect.width) / 2, 240))
        display.blit(lnDisp, ((WIN_W / 2 - lnIcon.rect.width - lnDispRect.width) / 2 + lnIcon.rect.width, 240 + (lnIcon.rect.height + 28 - lnDispRect.height) / 2))

        display.blit(snIcon.image, ((WIN_W / 2 - snIcon.rect.width - snDispRect.width) / 2 + WIN_W / 2, 263))
        display.blit(snDisp, ((WIN_W / 2 - snIcon.rect.width - snDispRect.width) / 2 + WIN_W / 2 + snIcon.rect.width, 263 + (snIcon.rect.height - snDispRect.height) / 2))

        display.blit(scrDisp, ((WIN_W - scrDispRect.width) / 2, 360))
        
        display.blit(TAP_PROMPT, ((WIN_W - promptRect.width) / 2, WIN_H - 10 - promptRect.height))
        pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    # clean up
    # cleanup("temp.wav")
    pygame.init()

    from common import AUDIO_FREQ, AUDIO_CHANNELS, AUDIO_BUFFER_SIZE

    pygame.mixer.init()
    pygame.mixer.init(AUDIO_FREQ, -16, AUDIO_CHANNELS, AUDIO_BUFFER_SIZE)
    # display file dialog
    while True:
        f, part = mainMenu()
        if part == Part.Play:
            while True:
                d, name, n, sn, cst, bpm, filepath, converted = analyze(f)
                r, sn, ln, scr = session(f, d, name, n, sn, cst, bpm, filepath)
                # cleanup("temp.wav")
                # cleanup("temp2.wav")
                
                if converted:
                    cleanup(filepath)

                if r == ExitReason.Exit:         
                    break
                elif r == ExitReason.Finish:
                    showFinalScore(ln, sn, scr, name)
                    break
                elif r == ExitReason.Restart:
                    pass
        elif part == Part.About:
            licensePage()
        elif part == Part.Help:
            helpPage()
        elif part == Part.Exit:   
            break
        
    cleanup("temp2.wav")
    cleanup("temp.wav")
    pygame.quit()
    
    quit()
