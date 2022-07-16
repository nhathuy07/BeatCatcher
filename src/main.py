import os
import pygame

pygame.init()
pygame.display.init()


def helpPage():
    print("Importing constants...")
    from common import WIN_W, WIN_H, WHITE_TEXT, FPS, PAUSE_BACKGROUND, FONT2, HELP_TEXT, GUIDE_TITLE, MAIN_MENU_BG, HELP_IMG, TAP_PROMPT
    
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWACCEL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    # dark overlay
    darkOverlay = PAUSE_BACKGROUND
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
        pygame.display.flip()
        clock.tick()
    
def licensePage():
    print("Importing constants...")
    from common import WIN_W, WIN_H, FONT2, PAUSE_BACKGROUND, VERSION_STRING, WHITE_TEXT, MENU_TITLE, LINK_COLOR, CWD, THIRD_PARTY_LIBS_LICENSE, ATTRIBUTION_TEXT, BACKGROUND_IMAGE, TAP_PROMPT, FPS, LICENSE
    from utils import textWrap
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWACCEL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT2, 22)
    font2 = pygame.font.Font(FONT2, 22)

    font.set_bold(True)


    # dark overlay
    darkOverlay = PAUSE_BACKGROUND

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
            y += textWrap(display, l, WHITE_TEXT, pygame.rect.Rect(left, top + y, width, height), font2, True, None)

        
        link1Rect.topleft = (20, 42 + y + smallMenuTitle.get_height() + name.get_rect().height * 1.5 + shortDesc.get_rect().height * 1.5 + copyrightText.get_height() * 1.5)
        link2Rect.topleft = (WIN_W - 20 - link2.get_width(), 42 + y + smallMenuTitle.get_height() + name.get_rect().height * 1.5 + shortDesc.get_rect().height * 1.5 + copyrightText.get_height() * 1.5)

        display.blit(link1, link1Rect.topleft)
        display.blit(link2, link2Rect.topleft)
        
        pygame.display.flip()
        clock.tick(FPS)
def mainMenu():
    print("Importing constants....")
    from common import WIN_W, WIN_H, PAUSE_BACKGROUND, LOADING_ICON, FPS, MUSIC_FOLDER
    import tkinter.filedialog
    print("Importing MainMenu module")
    from entities import MainMenu
    from customTypes import Part
    
    _mainMenu = MainMenu()
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWACCEL)
    clock = pygame.time.Clock()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None, Part.Exit
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if _mainMenu.playBtnRect.collidepoint(mousePos):
                    f = tkinter.filedialog.askopenfilename(title = "Select a song to play...", initialdir=MUSIC_FOLDER)
                    if f == "" or f == None:
                        pass
                    else:
                        display.blit(PAUSE_BACKGROUND, (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - LOADING_ICON.get_width()) / 2, (WIN_H - LOADING_ICON.get_width()) / 2))
                        pygame.display.flip()
                        return f, Part.Play
                elif _mainMenu.helpBtnRect.collidepoint(mousePos):
                    return None, Part.Help
                elif _mainMenu.aboutBtnRect.collidepoint(mousePos):
                    return None, Part.About
        
        _mainMenu.show(display)
        pygame.display.flip()
        clock.tick(FPS)

def analyze(f):
    print("Loading analyzer...")
    from entities import AudioAnalyzer
    print("Analyzer loaded! Finding notes...")
    audioObj = AudioAnalyzer(f)
    songName = audioObj.loadIntoLibrosa()
    noteStartList = audioObj.detectNotes()
    smallNoteStartList = audioObj.detectSmallNotes()

    # chorus detection feature will be implemented in the future
    chorusStartTime = None
    
    bpm = audioObj.calcBPM()

    return songName, noteStartList, smallNoteStartList, chorusStartTime, bpm

def session(f, songName, noteStartList, smallNoteStartList, bpm):
    print("Loading constants...")
    from common import WIN_W, WIN_H, PAD_Y_POS, SPEED_MULTIPLIER, FONT, FONT2, LOADING_ICON, PAUSE_BACKGROUND, BACKGROUND_IMAGE, FPS, WHITE_TEXT, LARGE_NOTE_SPRITE
    from common import HP_DEPLETION_RATE, LINK_COLOR
    print("Loading entities...")
    from entities import LargeNote, SmallNote, PauseMenu, PauseCountdown, Pad, Effect, ScoreDisp, LowHPWarning
    from utils import randomRange, cleanup
    from customTypes import PauseState, ExitReason, HitState
    import random

    pygame.mixer.music.load("temp2.wav")
    # create pygame window
    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWACCEL | pygame.SCALED, 0, 0, 1)

    # create pygame clock object
    clock = pygame.time.Clock()

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
    font = pygame.font.Font(FONT, 30)
    font2 = pygame.font.Font(FONT2, 15)

    # init warning var
    warning = LowHPWarning()

    pygame.mixer.music.play()
    while running:
        
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
                        display.blit(PAUSE_BACKGROUND, (0, 0))
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
                        display.blit(PAUSE_BACKGROUND, (0, 0))
                        display.blit(LOADING_ICON, ((WIN_W - loadingIconRect.width) / 2, (WIN_H - loadingIconRect.height) / 2))
                        pygame.display.flip()
                        return ExitReason.Restart, None, None, None
                    elif pauseText.exitBtnRect.collidepoint(mouseX, mouseY):
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
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
                    if (n.y + n.rect.height) >= PAD_Y_POS and (pad.x - n.rect.width + 10 <= n.x <= pad.x + pad.rect.width - 10):
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
            elif 100 >= hp > 32:
                warning.hide()
            elif 32 >= hp >= 0:
                warning.update()
            elif 0 > hp:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                return ExitReason.Failed, None, None, None


            score = largeNoteCount * 200 + smallNoteCount * 100
            scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
            hpDisp = font.render(f"{round(hp)}%", True, LINK_COLOR)
            songNameDisp = font2.render(songName, True, pygame.color.Color(WHITE_TEXT))

            if not warning.hidden:
                warning.render(display)
            display.blit(scoreDisp, (10, 10))
            display.blit(songNameDisp, (10, WIN_H - 30))
            display.blit(hpDisp, (WIN_W - hpDisp.get_width() - 10, 10))

            pad.render(display)
        elif paused == PauseState.Pausing:
            if not pauseTextDrawn:
                pygame.mixer.music.pause()
                scoreDisp = font.render(f"{str(score).zfill(9)}", True, WHITE_TEXT)
                songNameDisp = font2.render(songName, True, pygame.color.Color(WHITE_TEXT))
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
        
        
        
        pygame.display.flip()
        clock.tick(FPS)

def showFinalScore(ln, sn, scr, name):
    from common import WIN_W, WIN_H, FONT, PAUSE_BACKGROUND, FONT2, BACKGROUND_IMAGE, WHITE_TEXT, TAP_PROMPT, FINAL_SCORE_TITLE, FPS
    from entities import LargeNote, SmallNote

    lnIcon = LargeNote(0, 0)
    snIcon = SmallNote(0, 0)

    display = pygame.display.set_mode((WIN_W, WIN_H), pygame.HWACCEL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(FONT, 40)
    font2 = pygame.font.Font(FONT, 63)
    font3 = pygame.font.Font(FONT2, 20)

    lnCounter = 0
    snCounter = 0
    scrCounter = 0

    dark_overlay = PAUSE_BACKGROUND
    while True:
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.QUIT:
                return None
        display.blit(BACKGROUND_IMAGE, (0, 0))
        display.blit(dark_overlay, (0, 0))
        if lnCounter < ln:
            lnCounter += int(ln * 0.03)
        elif lnCounter >= ln:
            lnCounter = ln
        
        if snCounter < sn:
            snCounter += int(sn * 0.03)
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

def failedScreen():
    from entities import FailedScreen
    from common import WIN_H, WIN_W, FPS, PAUSE_BACKGROUND, LOADING_ICON
    from customTypes import ExitReason

    display = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()
    failedScreen = FailedScreen()
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                break
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if failedScreen.exitBtnRect.collidepoint(mouse):
                    return ExitReason.Exit
                elif failedScreen.retryBtnRect.collidepoint(mouse):
                    display.blit(PAUSE_BACKGROUND, (0, 0))
                    display.blit(LOADING_ICON, ((WIN_W - LOADING_ICON.get_width()) / 2, (WIN_H - LOADING_ICON.get_height()) / 2))
                    pygame.display.flip()
                    return ExitReason.Restart
        failedScreen.playAudio()
        failedScreen.show(display)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    
    from customTypes import ExitReason, Part
    from common import AUDIO_FREQ, AUDIO_CHANNELS, AUDIO_BUFFER_SIZE
    pygame.mixer.pre_init(AUDIO_FREQ, 16, AUDIO_CHANNELS, AUDIO_BUFFER_SIZE)

    pygame.init()
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])
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
        
    pygame.quit()
    
    quit()