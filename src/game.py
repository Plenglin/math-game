import sys
import time
from random import choice, randint

import pygame

import assets
import colors
import enemy

def main():

    kp = '] ['.join('1,2,3,4,5,6,7,8,9,0]'.split(',')).split(' ')
    pygame.init()
    disp = pygame.display.set_mode((640, 480))
    enemies = []
    enemySpawn = enemy.SpawnHandler(
        enemy.Level1, enemy.Level2, enemy.Level3, enemy.Level4, enemy.Level5
    )
    lastEnemySpawn = 0
    level = 1
    dt = time.time()

    abms = []
    
    channel = pygame.mixer.Channel(0)
    channel.queue(assets.loop1)

    playerinput = ''
    selected = None
    lives = 10
    
    while True:
        
        dt = time.time() - dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in '1234567890-':
                    playerinput += key
                elif key in kp:
                    playerinput += key[1:-1]
                elif event.key == pygame.K_KP_MINUS:
                    playerinput += '-'
                elif event.key == pygame.K_BACKSPACE:
                    playerinput = playerinput[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and selected != None:
                    print(playerinput)
                    e, y = selected
                    abms.append((0, y, e))

        if not pygame.mixer.get_busy():
            channel.queue(assets.loop1)
        
        if time.time() > lastEnemySpawn + 5:
            lastEnemySpawn = time.time()
            enemies.append((enemySpawn.spawn(), randint(0, 400)))

        # Find the enemy that the player has selected
        for e, y in enemies:
            x = int(480 * e.getProgress())
            rect = e.getSurface().get_rect()
            rect.topright = (x, y)
            if rect.collidepoint(pygame.mouse.get_pos()):
                selected = (e, y)
                break
        else:
            selected = None
        #print(playerinput)
        
        disp.fill(colors.white)

        # Draw enemies
        for e, y in enemies:
            x = int(480 * e.getProgress())
            missile = e.getSurface()
            rect = missile.get_rect()
            rect.topright = (x, y)
            disp.blit(e.getSurface(), rect)

        pygame.display.update()
        
if __name__ == '__main__':
    
    main()
