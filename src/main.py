import random
import sys
import time

import pygame

import colors
import enemy


#HIGHSCORES = open('highscores.txt', 'r+')
ICON = pygame.image.load('assets/icon.png')
FNYC = pygame.image.load('assets/fnyc.png')


def main():

    display = init()

    fnyc = FNYC.copy()
    #pygame.transform.scale(fnyc, (960, 960))
    fnyc = pygame.transform.rotate(fnyc, 90)
    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                terminate()

        display.fill(colors.white)

        r = fnyc.get_rect()
        r.midbottom = (640, 1024)
        
        display.blit(fnyc, r)
        pygame.display.update()

def init():
    #HIGHSCORES.read
    pygame.init()
    pygame.display.set_caption("Math Game")
    pygame.display.set_icon(ICON)
    display = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
    return display

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
