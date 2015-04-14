import random
import sys
import time

import pygame

import enemy


HIGHSCORES = open('highscores.txt', 'r+')
ICON = pygame.image.load('assets/icon.png')

class GameInstance():

    display = None

    def loop(self):
        nextEnemySpawn = self.getNextSpawn()
        dt = time.time()
        while True:
            dt = time.time() - dt
            handleEvents()
            
    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                terminate()

    class EnemyHandler():

        enemies = []
        resolution = (0, 0)
        nextSpawn = 0

        def __init__(self, resolution):
            self.resolution = resolution
            self.nextSpawn = self.getNextSpawn()

        def newEnemy(self, level, enemy):
            self.enemies.append(enemy(level, self.resolution), height)
            self.nextSpawn = self.getNextSpawn()

        def update(self, playerInput):
            result = {'enemySuccess': []}
            for enemy in self.enemies:
                if enemy.isCorrect(playerInput):
                    self.enemies.remove(enemy)
                if enemy.getProgress() >= 1:
                    result['enemySuccess'].append(enemy)
            return result

        def drawEnemies(self, display):
            for enemy in self.enemies:
                display.blit(enemy.getSurface, enemy.getPos())

        def getNextSpawn(self):
            return time.time() + 1 + random.random() * 2

def main():
    
    gameLoop(display)

def init():
    #HIGHSCORES.read
    pygame.init()
    pygame.display.set_caption("Math Game")
    pygame.display.set_icon(ICON)
    display = pygame.display.set_mode((640, 480))

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
