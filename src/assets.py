import random

import pygame

import sprites

pygame.init()

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
background = pygame.transform.rotozoom(city, 90, 0.5)
rocket1 = loadImg('rocket-1')
rocket2 = loadImg('rocket-2')
rocket3_1 = loadImg('rocket-3-hp1')
rocket3_2 = loadImg('rocket-3-hp2')
explosion1 = loadImg('explosion-r1')
explosion2 = loadImg('explosion-r2')
explosion3 = loadImg('explosion-r3')
explosionABMS = loadImg('explosion-abm-success')
explosionABMF = loadImg('explosion-abm-failure')

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
            jokes.append('"{}" -{}'.format(line, random.choice(_authors)))

def main():
    pass

if __name__ == '__main__':
    main()
