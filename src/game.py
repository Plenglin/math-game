import sys
import time
from random import choice, randint

import pygame

import assets
import colors
import enemy


class Game():
    '''
    Main Game class. Holds all the variables critical
    to the game's function. Also acts as an interface
    between the player and enemy handlers.
    '''

    player = None
    enemy = None
    display = None
    music = None
    gui = None
    
    def __init__(self, resolution):
        self.resolution = resolution
        self.display = pygame.display.set_mode(resolution)
        pygame.display.set_caption('Solve or Die')
        self.channel = pygame.mixer.Channel(0)
        self.channel.queue(assets.loop1)
        self.player = Player(self)
        self.enemy = EnemyManager(
            self,
            enemy.Level1, enemy.Level2, enemy.Level3, enemy.Level4, enemy.Level5
        )
        gui = GUI(self)

    '''
    The update and draw functions meshed together
    '''    
    def updateGetSurface(self):
        
        surf = pygame.Surface(self.resolution)
        surf.fill(colors.white)
        surf.blit(self.enemy.getSurface(), (0, 0))
        
        for abm in self.player.abms:
            surf.blit(assets.abm, abm.getPos())
            if abm.hasArrived():
                self.enemy.explode(abm.enemy, abm.y)
                self.player.abms.remove(abm)

        for e, p in self.enemy.explosions:
            rect = e.getRect()
            rect.center = p
            surf.blit(e.getSurface(), rect)
            if e.isFinished():
                self.enemy.explosions.remove((e, p))
        
        return surf

    def getLabelFormat(self):
        return {
            'lives': self.player.hp,
            'score': self.player.score,
            'level': self.player.getLevel(),
            'mousepos': pygame.mouse.get_pos(),
            'input': self.player.answer,
        }

class Player():
    '''
    Player handler class. Handles the player's variables
    and ABMs.
    '''

    hp = 10
    score = 0
    answer = ''
    game = None
    abms = []

    def __init__(self, gameInstance):
        self.game = gameInstance
        self.lasers = [] # Prevent them from linking

    class ABM():
        
        speed = 250
        player = None
        target = 0
        enemy = None
        y = 0
        start = 0
        
        def __init__(self, player, target, e, y):
            self.player = player
            self.target = target
            self.enemy = e
            self.y = y
            self.start = time.time()

        def getX(self):
            elapsed = time.time() - self.start
            return self.player.game.resolution[0] - self.speed * elapsed

        def hasArrived(self):
            return self.getX() <= self.target

        def getPos(self):
            return (self.getX(), self.y)
            
    def isCorrect(self):
        e, y = self.getSelected()
        if e.isCorrect(self.answer):
            rect = e.getSurface().get_rect()
            x = self.game.enemy.getX(e)
            rect.topright = (x, y)
            self.abms.append(Player.ABM(self, rect.right, e, y))
    
    def getSelected(self):
        w, h = self.game.resolution
        for e, y in self.game.enemy.enemies:
            x = self.game.enemy.getX(e)
            rect = e.getSurface().get_rect()
            rect.topright = (x, y)
            if rect.collidepoint(pygame.mouse.get_pos()):
                return (e, y)
        return None

    def getLevel(self):
        return int(round(self.score / 1000))

class EnemyManager():
    '''
    Enemy handler class. Handles the enemies.
    '''

    available = []
    enemies = []
    explosions = []
    lastSpawn = 0
    game = None
    
    def __init__(self, gameInstance, *availableEnemies):
        self.game = gameInstance
        self.available = availableEnemies
        self.enemies = [] # Prevent them from linking
        self.explosions = []

    def spawnchoices(self):
        chips = []
        for enemy in self.available:
            toAdd = enemy.getChance(self.game.player.getLevel())
            for chip in range(0, toAdd):
                chips.append(enemy)
        return chips

    def canSpawn(self):
        return time.time() > self.nextSpawn() or self.enemies == []
            
    def nextSpawn(self):
        return self.lastSpawn + self.game.player.getLevel() + 10

    def spawn(self):
        w, h = self.game.resolution
        ToSpawn = choice(self.spawnchoices())
        e = ToSpawn(self.game.player.getLevel())
        eHeight = e.getSurface().get_height()
        self.enemies.append((e, randint(0, h - eHeight)))
        self.lastSpawn = time.time()

    def getX(self, enemy):
        w, h = self.game.resolution
        return int(w * enemy.getProgress())

    def getSurface(self):
        surf = pygame.Surface(self.game.resolution, pygame.SRCALPHA, 32)
        for e, y in self.enemies:
            x = self.getX(e)
            missile = e.getSurface()
            rect = missile.get_rect()
            rect.topright = (x, y)
            surf.blit(e.getSurface(), rect)
        return surf

    def handleEnemies(self):
        for e in self.enemies:
            if e.getProgress() >= 1:
                self.enemies.remove(e)
                self.game.player.hp -= 2

    def explode(self, e, y):
        rect = e.getRect()
        rect.topright = (self.getX(e), y)
        exp = e.getExplosion()
        exp.start()
        self.explosions.append((exp, rect.midright))
        self.enemies.remove((e, y))

class GUI():

    game = None
    elements = []

    def __init__(self, gameInstance, *elements):
        self.game = gameInstance
        self.elements = elements

    def add(self, label, size, pos):
        self.elements.append(GUIElement(label, size, pos))

class GUIElement():

    label = ''
    pos = (0, 0)
    font = None

    def __init__(self, label, size, pos):
        self.game = gameInstance
        self.label = label
        self.pos = pos
        self.font = pygame.Font(size)

    def getSurface(self, game):
        text = self.label.format(**self.game.getLabelFormat())
        return self.font.render(text, True, (0, 0, 0))


KEYPAD = '] ['.join('[1,2,3,4,5,6,7,8,9,0]'.split(',')).split(' ')
RESOLUTION = (640, 480)

def main():
    
    pygame.init()

    game = Game((640, 480))

    lastLevel = 1

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in '1234567890-':
                    game.player.answer += key
                elif key in KEYPAD:
                    game.player.answer += key[1:-1]
                elif event.key == pygame.K_KP_MINUS:
                    game.player.answer += '-'
                elif event.key == pygame.K_BACKSPACE:
                    game.player.answer = game.player.answer[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game.player.getSelected() != None:
                    e, y = game.player.getSelected()
                    game.player.isCorrect()
                    game.player.answer = ''

        if not pygame.mixer.get_busy():
            game.channel.queue(assets.loop1)
        
        if game.enemy.canSpawn():
            game.enemy.spawn()

        game.display.fill(colors.white)
        game.display.blit(game.updateGetSurface(), (0, 0))
        pygame.display.update()
        
if __name__ == '__main__':
    
    main()
