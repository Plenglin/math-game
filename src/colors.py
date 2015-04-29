'''
Human-readable colors
'''

from random import randint

import pygame
from pygame import Color


# Named colors        R    G    B    A
black       = Color(  0,   0,   0, 255)
white       = Color(255, 255, 255, 255)
red         = Color(255,   0,   0, 255)
blue        = Color(  0,   0, 255, 255)
green       = Color(  0, 255,   0, 255)
dark_green  = Color(  0, 128,   0, 255)
yellow      = Color(255, 255,   0, 255)
magenta     = Color(255,   0, 255, 255)
cyan        = Color(  0, 255, 255, 255)
aqua        = Color(  0, 255, 128, 255)
purple      = Color(128,   0, 128, 255)
pink        = Color(255,   0, 128, 255)
light_blue  = Color(  0, 128, 255, 255)
sky_blue    = Color(  0, 192, 255, 255)
orange      = Color(255, 128,   0, 255)
tan         = Color(210, 180, 140, 255)
navy_blue   = Color(  0,   0,  92, 255)

def random():
    return Color(randint(0, 255), randint(0, 255), randint(0, 255), 255)

def gray(percent):
    '''0 is white, 100 is black'''
    assert percent <= 100, 'Percentage must not be more than 100'
    rgb = round(255 - (255 * percent / 100))
    return Color(rgb, rgb, rgb, 255)

def getColor(colorval):
    t = type(colorval)
    if t == Color:
        return colorval
    elif t in (list, tuple):
        color = list(colorval) + [255]
        return pygame.Color(*color)
    elif t == str:
        if 'gray' in colorval:
            intensity = colorval.split()[1]
            return gray(int(intensity))
        colorval = colorval.replace(' ', '_')
        return globals()[colorval]
    else:
        raise Exception('Colorval must be a str, list, or tuple')

def brighten(color, scale):
    if type(color) in (list, tuple):
        return brighten(Color(*color))
    r = int(color.r * scale)
    g = int(color.g * scale)
    b = int(color.b * scale)
    r = r if r <= 255 else 255
    g = g if g <= 255 else 255
    b = b if b <= 255 else 255
    return Color(r, g, b, 255)

_hue = lambda level: (level / 90) * 255

def hue(level):
    level = int(level)
    level %= 360
    level2 = level % 90
    r, g, b = 0, 0, 0
    if level in range(0, 90):
        r = 255 - _hue(level2)
        g = _hue(level2)
    elif level in range(90, 180):
        g = 255
        b = _hue(level2)
    elif level in range(180, 270):
        g = 255 - _hue(level2)
        b = 255
    elif level in range(270, 360):
        r = _hue(level2)
        b = 255 - _hue(level2)
    return Color(int(r), int(g), int(b), 255)

def invert(color):
    if type(color) in (tuple, list): color = pygame.Color(*color)
    return pygame.Color(255 - color.r, 255 - color.g, 255 - color.b, color.a)

if __name__ == '__main__':
    print(globals())
