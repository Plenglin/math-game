import sys
from random import randint

import pygame

import assets
import colors
import main as MAIN
import sprites


def startscreen(display):

    miscfont = pygame.font.Font('freesansbold.ttf', 32)
    smallfont = pygame.font.Font('freesansbold.ttf', 16)

    displayrect = display.get_rect()
    
    city = assets.city.copy()
    cityrect = city.get_rect()
    cityrect.midbottom = displayrect.midbottom
    
    title = assets.title.copy()
    titlerect = title.get_rect()
    titlerect.midtop = (int(displayrect.w/2), int(displayrect.h/4))

    rocket = pygame.transform.rotate(assets.rocket3_2.copy(), 270)
    rocketrect = rocket.get_rect()
    rocketrect.midtop = displayrect.center

    coin = assets.coin.copy()
    coinrect = coin.get_rect()
    coinrect.center = (randint(0, displayrect.w-1), randint(0, displayrect.h-1))
    holdingCoin = False

    recep = sprites.spriteAnimation(assets.receptacle.copy(), 10)
    receprect = recep.getSurface().get_rect()
    receprect.bottomright = displayrect.midbottom

    insertcoin = smallfont.render('Please insert a coin', True, colors.white)
    insertcoinrect = insertcoin.get_rect()
    insertcoinrect.midbottom = receprect.midtop

    startingsoon = miscfont.render('Starting...', True, colors.white)
    startingsoonrect = startingsoon.get_rect()
    startingsoonrect.midbottom = displayrect.midbottom
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MAIN.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if coinrect.collidepoint(event.pos) and not holdingCoin:
                    holdingCoin = True
                if receprect.colliderect(coinrect) and holdingCoin:
                    holdingCoin = False
                    coinrect.bottomright = (0, 0)
                    recep.start()

        if holdingCoin:
            pygame.mouse.set_visible(False)
            coinrect.center = pygame.mouse.get_pos()
        else:
            pygame.mouse.set_visible(True)

        if recep.isFinished():
            raise MAIN.LevelFinished()
            
        display.fill(colors.white)
        display.blit(city, cityrect)
        display.blit(title, titlerect)
        display.blit(rocket, rocketrect)
        display.blit(recep.getSurface(), receprect)
        display.blit(insertcoin, insertcoinrect)
        if recep.hasStarted:
            display.blit(startingsoon, startingsoonrect)
        display.blit(coin, coinrect)
        
        pygame.display.update()     

def main():
    pygame.init()
    d = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
    startscreen(d)

if __name__ == '__main__':
    main()
