import pygame

import sprites

pygame.init()

def loadImg(file):
    return pygame.image.load('assets/{}.png'.format(file))

def loadSound(file):
    return pygame.mixer.Sound('assets/{}.ogg'.format(file))

abm = loadImg('abm')
abmLauncherUp = loadImg('abm-launcher')
abmLauncherDown = pygame.transform.flip(abmLauncherUp, False, True)
city = loadImg('fnyc')
rocket1 = loadImg('rocket-1')
rocket2 = loadImg('rocket-2')
rocket3 = loadImg('rocket-3')
explosion1 = loadImg('explosion-1')
explosion2 = loadImg('explosion-2')

loop1 = loadSound('solve-or-die-loop')

def main():
    pass

if __name__ == '__main__':
    main()
