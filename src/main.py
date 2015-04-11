import sys
import random

import pygame

import enemy


ICON = pygame.image.load('assets/icon.png')

class GameManager():

    enemies = []
    

def main():
    pygame.init()
    pygame.display.set_caption("Math Game")
    pygame.display.set_icon(ICON)
    display = pygame.display.set_mode((640, 480))
    gameLoop(display)

def terminate():
    pygame.quit()
    sys.exit()

def gameLoop(display):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

if __name__ == '__main__':
    main()
