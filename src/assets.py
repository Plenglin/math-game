import pygame

pygame.init()

def loadImg(file):
    return pygame.image.load('assets/{}.png'.format(file))

def loadSound(file):
    return pygame.mixer.Sound('assets/{}.ogg'.format(file))

abm = loadImg('abm')
abmLauncher = loadImg('abm-launcher')
city = loadImg('fnyc')
rocket1 = loadImg('rocket-1')
rocket2 = loadImg('rocket-2')
rocket3 = loadImg('rocket-3')

loop1 = loadSound('solve-or-die-loop')

def main():
    display = pygame.display.set_mode((640, 480))
    loop1.set_volume(1)
    loop1.play(1)

if __name__ == '__main__':
    main()
