import sys
from random import randint, choice

import pygame

import assets
import colors
import main as MAIN
import sprites
import gameover


def startscreen(display):

    miscfont = pygame.font.Font('freesansbold.ttf', 32)
    smallfont = pygame.font.Font('freesansbold.ttf', 16)
    largeFont = pygame.font.Font('freesansbold.ttf', 30)
    textFont = pygame.font.Font('freesansbold.ttf', 20)

    displayrect = display.get_rect()

    city = assets.city.copy()
    cityrect = city.get_rect()
    cityrect.midbottom = displayrect.midbottom

    title = assets.title.copy()
    titlerect = title.get_rect()
    titlerect.midtop = (int(displayrect.w/2), int(displayrect.h/4))

    rockets = []
    for i in range(0, 5):
        r = choice([assets.rocket1, assets.rocket2, assets.rocket3_2])
        rocket = pygame.transform.rotate(r.copy(), 270)
        rocketrect = rocket.get_rect()
        rocketrect.center = randint(0, displayrect.w), randint(0, displayrect.h)
        rockets.append((rocket, rocketrect))

    coin = assets.coin.copy()
    coinrect = coin.get_rect()
    coinrect.center = (randint(0, displayrect.w-1), randint(0, displayrect.h-1))
    holdingCoin = False

    recep = sprites.spriteAnimation(assets.receptacle.copy(), 10)
    receprect = recep.getSurface().get_rect()
    receprect.midbottom = displayrect.midbottom

    insertcoin = smallfont.render('Please insert 3.14 cents', True, colors.aqua)
    insertcoinrect = insertcoin.get_rect()
    insertcoinrect.midbottom = receprect.midtop

    startingsoon = miscfont.render('Starting...', True, colors.white)
    startingsoonrect = startingsoon.get_rect()
    startingsoonrect.midbottom = displayrect.midbottom

    highscores = pygame.Surface((350, 210), pygame.SRCALPHA, 32)
    highscoresrect = highscores.get_rect()
    highscoresrect.midtop = displayrect.center
    highscoresborder = highscoresrect.copy()
    highscoresborder.top -= 10
    highscoresborder.left -= 10
    n = 0
    c = colors.black
    for name, s in gameover.getHighScores():
        highscores.blit(miscfont.render(str(n+1), True, c), (0, n*40))
        highscores.blit(textFont.render(name.upper(), True, c), (50, n*40))
        highscores.blit(textFont.render(str(s), True, c), (250, n*40))
        n += 1
        if n == 5:
            break


    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MAIN.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if holdingCoin:
                    if receprect.colliderect(coinrect):
                        holdingCoin = False
                        coinrect.bottomright = (0, 0)
                        recep.start()
                    else:
                        holdingCoin = False
                else:
                    if coinrect.collidepoint(event.pos):
                        holdingCoin = True

        if holdingCoin:
            pygame.mouse.set_visible(False)
            coinrect.center = pygame.mouse.get_pos()
        else:
            pygame.mouse.set_visible(True)

        if recep.isFinished():
            raise MAIN.LevelFinished()

        display.fill(colors.sky_blue)
        display.blit(city, cityrect)
        for rocket, rect in rockets:
            display.blit(rocket, rect)
        display.blit(title, titlerect)
        display.blit(recep.getSurface(), receprect)
        display.blit(insertcoin, insertcoinrect)
        pygame.draw.rect(display, colors.yellow, highscoresborder)
        display.blit(highscores, highscoresrect)
        if recep.hasStarted:
            display.blit(startingsoon, startingsoonrect)
        display.blit(coin, coinrect)

        if not pygame.mixer.get_busy():
            assets.loop1.play()

        pygame.display.update()

def main():
    pygame.init()
    d = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
    startscreen(d)

if __name__ == '__main__':
    main()
