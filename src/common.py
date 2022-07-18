from pygame import display
from pygame.transform import smoothscale, scale
from pygame import image as pg_image
from pygame import HWSURFACE
from pygame.rect import Rect
from pygame.mixer import Sound
from pygame.mixer import init as pg_mixer_init
from os import path, getenv, getcwd

display.init()
pg_mixer_init()

WIN_W = 1200
WIN_H = 700

display.set_mode((WIN_W, WIN_H), HWSURFACE)
ROUNDING_DIGITS = 5
AUDIO_CHANNELS = 1
AUDIO_BUFFER_SIZE = 32
AUDIO_FREQ = int(22050)
LONG_NOTE_MINIMUM_DURATION = 0.3
FALLING_TIME = 1

SPEED_MULTIPLIER = 0.015

FPS = 60

LARGE_NOTE_SPRITE = pg_image.load("assets/HitObject.png").convert_alpha()
SMALL_NOTE_SPRITE = pg_image.load("assets/HitObjectSmall.png").convert_alpha()
PAD_SPRITE = pg_image.load("assets/Pad.png").convert_alpha()

RESTART_BTN = pg_image.load("assets/ReloadBtn.png").convert_alpha()
RESUME_BTN = pg_image.load("assets/PlayButton.png").convert_alpha()
EXIT_BTN = pg_image.load("assets/logout.png").convert_alpha()
HELP_BTN = pg_image.load("assets/help.png").convert_alpha()
INFO_BTN = pg_image.load("assets/info.png").convert_alpha()

RESUME_COUNTDOWN_SPRITES = [
    pg_image.load("assets/3 (Custom).png").convert_alpha(), 
    pg_image.load("assets/2 (Custom).png").convert_alpha(), 
    pg_image.load("assets/1 (Custom).png").convert_alpha()]

MAIN_MENU_BG = pg_image.load("assets/MenuBackground.png").convert_alpha()
MENU_TITLE = pg_image.load("assets/menuTitle.png").convert_alpha()
GUIDE_TITLE = pg_image.load("assets/guideText.png").convert_alpha()
PAUSE_BACKGROUND = pg_image.load("assets/countdownBackground.png").convert_alpha()

HIT_FX_SPRITE = pg_image.load("assets/HitEffect.png").convert_alpha()
MISS_FX_SPRITE = pg_image.load("assets/MissEffect.png").convert_alpha()
LOW_HP_WARNING_FX = smoothscale(pg_image.load("assets/lowHealthFx.png").convert_alpha(), (WIN_W, WIN_H))

LARGE_NOTE_SCORE = smoothscale(pg_image.load("assets/200.png").convert_alpha(), (124, 78))
SMALL_NOTE_SCORE = smoothscale(pg_image.load("assets/100.png").convert_alpha(), (124, 78))

LOADING_ICON = smoothscale(pg_image.load("assets/loading.png").convert_alpha(), (200, 200))

FONT = "assets/04B_30__.TTF"
FONT2 = "assets/VCR_OSD_MONO_1.001.ttf"

PAUSE_TEXT = pg_image.load("assets/PauseText.png").convert_alpha()

BLANK_AUDIO = "assets/blank.wav"

# convert degree to radian to draw arc
DEG_TO_RAD = 0.0174532925

HP_DEPLETION_RATE = 8
HP_ARC_SIZE = 50
HP_ARC_BOUNDARY = Rect(WIN_W - 10 - HP_ARC_SIZE, 10, HP_ARC_SIZE, HP_ARC_SIZE)

BACKGROUND_COLOR = (0, 0, 0)
LINK_COLOR = (255, 161, 210)
HP_BAR_COLOR = (153, 239, 253)
BACKGROUND_IMAGE = smoothscale(pg_image.load("assets/output-onlinepngtools-min.png").convert(), (WIN_W, WIN_H))
WHITE_TEXT = (255, 255, 255)

PAD_Y_POS = 620

PROJECT_PATH = (getcwd())

FINAL_SCORE_TITLE = pg_image.load("assets/final score (Custom).png").convert_alpha()

FAILED_SCREEN_TITLE = pg_image.load("assets/failedText.png").convert_alpha()

MUSIC_FOLDER = path.join(getenv("USERPROFILE"), "Music")

TAP_PROMPT = scale(pg_image.load("assets/tapPrompt.png").convert_alpha(), (400 * 0.75, 70 * 0.75))

HELP_IMG = [pg_image.load(f"assets/helpPage{n}.png").convert_alpha() for n in range(5)]

HELP_TEXT = [
        "Press the Play button, then choose a song from the File Dialog|Non-WAV audio files may take longer to load, as they must be converted first.",
        "Throughout the game, Notes and Small Notes will fall from above|Move the pad with your mouse to catch the notes in tune to the rhythm of the song.",
        "Each Note gives 200 pts, while each Small Note gives 100 pts",
        "Your HP level is displayed at the top-right corner of the window.|Your HP level will drop each time you miss a note, and increase each time you hit a note.|Try to keep the HP level above 0 till the end of the game to win.",
        "At the end of the song, the number of notes catched and your total score will be shown."
    ]

VERSION_STRING = "0.1.1"

LICENSE = ["This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either  version 3 of the License, or (at your option) any later version.",
"This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR      PURPOSE. See the GNU General Public License for more details.",
"You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.",
]

THIRD_PARTY_LIBS_LICENSE = "./assets/Extras/thirdPartyLibsLicense.txt"
ATTRIBUTION_TEXT = "./assets/Extras/attribution.txt"

CWD = getcwd()

GAME_OVER_SOUND = Sound("assets/mixkit-sad-game-over-trombone-471.wav")

HP_ICON = pg_image.load("assets/heart.png").convert_alpha()