import pygame
import os
import sys

pygame.display.init()

ROUNDING_DIGITS = 5
AUDIO_CHANNELS = 1
AUDIO_BUFFER_SIZE = 32
AUDIO_FREQ = int(22050)
LONG_NOTE_MINIMUM_DURATION = 0.3
FALLING_TIME = 1

SPEED_MULTIPLIER = 0.015

FPS = 240

BUFFER_SEC = 1

LARGE_NOTE_SPRITE = "assets/HitObject.png"
SMALL_NOTE_SPRITE = "assets/HitObjectSmall.png"
PAD_SPRITE = "assets/Pad.png"

RESTART_BTN = "assets/ReloadBtn.png"
RESUME_BTN = "assets/PlayButton.png"
EXIT_BTN = "assets/logout.png"
HELP_BTN = "assets/help.png"
INFO_BTN = "assets/info.png"

RESUME_COUNTDOWN_SPRITES = ["assets/3 (Custom).png", "assets/2 (Custom).png", "assets/1 (Custom).png"]

MAIN_MENU_BG = pygame.image.load("assets/MenuBackground.png")
MENU_TITLE = pygame.image.load("assets/menuTitle.png")
GUIDE_TITLE = pygame.image.load("assets/guideText.png")
PAUSE_BACKGROUND = "assets/countdownBackground.png"

HIT_FX_SPRITE = pygame.image.load("assets/HitEffect.png")
MISS_FX_SPRITE = pygame.image.load("assets/MissEffect.png")

LARGE_NOTE_SCORE = pygame.transform.smoothscale(pygame.image.load("assets/200.png"), (124, 78))
SMALL_NOTE_SCORE = pygame.transform.smoothscale(pygame.image.load("assets/100.png"), (124, 78))

LOADING_ICON = pygame.transform.smoothscale(pygame.image.load("assets/loading.png"), (200, 200))

FONT = "assets/04B_30__.TTF"
FONT2 = "assets/VCR_OSD_MONO_1.001.ttf"

PAUSE_TEXT = "assets/PauseText.png"

WIN_W = 1200
WIN_H = 700

BACKGROUND_COLOR = (0, 0, 0)
LINK_COLOR = (255, 161, 210)
BACKGROUND_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/output-onlinepngtools-min.png"), (WIN_W, WIN_H))
WHITE_TEXT = (255, 255, 255)

PAD_Y_POS = 620

PROJECT_PATH = (os.getcwd())

FINAL_SCORE_TITLE = pygame.image.load("assets/final score (Custom).png")

if os.name == "nt":
    MUSIC_FOLDER = os.path.join(os.getenv("USERPROFILE"), "Music")
else:
    MUSIC_FOLDER = os.path.join(os.getenv("HOME"), "Music")

TAP_PROMPT = pygame.transform.smoothscale(pygame.image.load("assets/tapPrompt.png"), (400 * 0.75, 70 * 0.75))

HELP_IMG = [
    pygame.image.load("assets/helpPage0.png"),
    pygame.image.load("assets/helpPage1.png"),
    pygame.image.load("assets/helpPage2.png"),
    pygame.image.load("assets/helpPage3.png")
    ]

HELP_TEXT = [
        "Press the Play button, then choose a song from the File Dialog|Non-WAV audio files may take longer to load, as they must be converted first.",
        "Throughout the game, Notes and Small Notes will fall from above|Move the pad with your mouse to catch the notes in tune to the rhythm of the song.",
        "Each Note gives 200 pts, while each Small Note gives 100 pts",
        "At the end of the song, the number of notes catched and your total score will be shown."
    ]

VERSION_STRING = "0.1.0"

LICENSE = ["This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either  version 3 of the License, or (at your option) any later version.",
"This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR      PURPOSE. See the GNU General Public License for more details.",
"You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.",
]

THIRD_PARTY_LIBS_LICENSE = "./assets/Extras/thirdPartyLibsLicense.txt"
ATTRIBUTION_TEXT = "./assets/Extras/attribution.txt"

CWD = os.getcwd()


