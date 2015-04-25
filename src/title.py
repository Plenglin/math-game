import sys

import pygame

import assets
import colors
import main as MAIN


def startscreen(display):

    miscfont = pygame.font.Font('freesansbold.ttf', 32)

    displayrect = display.get_rect()
    
    city = assets.city.copy()
    cityrect = city.get_rect()
    cityrect.midbottom = displayrect.midbottom
    
    title = assets.title.copy()
    titlerect = title.get_rect()
    titlerect.midtop = (int(displayrect.w/2), int(displayrect.h/4))

    button = assets.rocket3_2.copy()
    buttonrect = button.get_rect()
    buttonrect.midtop = displayrect.center

    start = miscfont.render('START', True, colors.white)
    startrect = start.get_rect()
    startrect.midleft = buttonrect.center
    MAIN.cam.get_image()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MAIN.terminate()

        display.fill(colors.white)
        display.blit(city, cityrect)
        display.blit(title, titlerect)
        display.blit(button, buttonrect)
        display.blit(start, startrect)
        pygame.display.update()     

def main():
    pygame.init()
    d = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
    startscreen(d)

if __name__ == '__main__':
    main()
