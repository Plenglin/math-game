import json
import random
import sys
import time

import pygame

import assets
import colors
import enemy
import game
import title


class LevelFinished(Exception):
    pass

def init():
    highscores = None
    try:
        highscorefile = open('highscores.json', 'r')
        highscorefile.close()
    except FileNotFoundError:
        highscorefile = open('highscores.json', 'w+')
        defaultscorefile = open('assets/data/defaultscores.json', 'r')
        highscorefile.write(defaultscorefile.read())
        highscorefile.close()
        defaultscorefile.close()
    with open('highscores.json', 'r') as file:
        txt = file.read()
        highscores = json.loads(txt)
    pygame.init()
    pygame.display.set_caption("Math Game")
    display = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
    return display

def terminate():
    pygame.quit()
    sys.exit()

def main():
    d = init()
    while True:
        try:
            title.startscreen(d)
        except:
            pass
        try:
            game.initGame(d)
        except:
            pass


if __name__ == '__main__':
    main()
