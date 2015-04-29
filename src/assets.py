import random

import pygame
import pygame.camera

import sprites

pygame.init()
pygame.camera.init()

def loadImg(file):
    return pygame.image.load('assets/sprites/{}.png'.format(file))

def loadSound(file):
    return pygame.mixer.Sound('assets/sound/{}.ogg'.format(file))

def loadText(file):
    return open('assets/data/{}'.format(file))


abm = loadImg('abm')
abmLauncherUp = loadImg('abm-launcher')
abmLauncherDown = pygame.transform.flip(abmLauncherUp, False, True)
abmHolder = loadImg('abm-holder')
city = loadImg('fnyc')
coin = loadImg('picoin')
background = pygame.transform.rotozoom(city, 90, 1)
explosion1 = loadImg('explosion-r1')
explosion2 = loadImg('explosion-r2')
explosion3 = loadImg('explosion-r3')
explosionABMS = loadImg('explosion-abm-success')
explosionABMF = loadImg('explosion-abm-failure')
explosionEnd1 = loadImg('explosion-gameover-1')
explosionEnd2 = loadImg('explosion-gameover-2')
explosionEnd3 = loadImg('explosion-gameover-3')
title = pygame.transform.rotozoom(loadImg('title'), 0, 2)
receptacle = loadImg('receptacle')
recordBreak = loadImg('recordbreak')
rocket1 = loadImg('rocket-1')
rocket2 = loadImg('rocket-2')
rocket3_1 = loadImg('rocket-3-hp1')
rocket3_2 = loadImg('rocket-3-hp2')
sun = pygame.transform.rotozoom(loadImg('sun'), 0, 2)

loop1 = loadSound('solve-or-die-loop')

_authors = []
with loadText('authors.txt') as file:
    for line in file:
        if line != '':
            _authors.append(line)

jokes = []
with loadText('puns.txt') as file:
    for line in file:
        if line != '':
            jokes.append('"{}" -{}'.format(line, random.choice(_authors)).replace('\n', ''))

def main():
    pass

if __name__ == '__main__':
    main()
