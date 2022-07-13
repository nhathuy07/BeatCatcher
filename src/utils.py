import os
import wave
import pygame.rect
from common import WIN_W
from common import ROUNDING_DIGITS
import random

def cleanup(f: str):
    if os.path.exists(f):
        print("Cleaning up...")
        os.remove(f)

def numberRounding(x: float) -> float:
    return round(x, ROUNDING_DIGITS)

def randomRange(x: int, i: int) -> int:
    minimum, maximum = x - i, x + i
    if minimum < 10:
        minimum = 10
    if maximum > WIN_W - 80:
        maximum = WIN_W - 80
    return random.randint(minimum, maximum)

# code adapted from https://www.thepythoncode.com/article/concatenate-audio-files-in-python 
def concatenateAudio(clipPaths):
    data = []
    for c in clipPaths:
        with wave.open(c, "rb") as w:
            data.append((w.getparams(), w.readframes(w.getnframes())))
        with wave.open("temp2.wav", "wb") as o:
            o.setparams(data[0][0])
            for i in range(len(data)):
                o.writeframes(data[i][1])

# code adapted from https://www.pygame.org/wiki/TextWrap#:~:text=Simple%20Text%20Wrapping%20for%20pygame.&text=Simple%20function%20that%20will%20draw,make%20the%20line%20closer%20together.
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def textWrap(surface, text, color, rect, font, aa=False, bkg=None):
    textBoxHeight = 0
    rect = pygame.rect.Rect(rect)
    y = rect.top
    lineSpacing = 6

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i > len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        textBoxHeight += lineSpacing + image.get_rect().height

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]
    return textBoxHeight * 1.5
