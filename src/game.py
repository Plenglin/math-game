import sys
import time
from random import choice, randint

import pygame

import assets
import colors
import enemy
import sprites


pgrsFont = pygame.font.Font('freesansbold.ttf', 12)

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

    start = 0

    explosions = []
    
    def __init__(self, resolution):
        self.start = time.time()
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
        self.explosions = []

    '''
    The update and draw functions meshed together
    '''    
    def updateGetSurface(self):

        w, h = self.resolution

        self.player.score = int((time.time() - self.start) * 100) # FOR TEST ONLY
        
        surf = pygame.Surface(self.resolution)
        surf.fill(colors.white)
        surf.blit(self.enemy.getSurface(), (0, 0))
        
        for abm in self.player.abms:
            surf.blit(assets.abm, abm.getPos())
            if abm.hasArrived():
                if abm.correct:
                    self.enemy.explode(abm.enemy)
                abm.explode()

        for e, p in self.explosions:
            rect = e.getRect()
            rect.center = p
            surf.blit(e.getSurface(), rect)
            if e.isFinished():
                self.explosions.remove((e, p))

        surf.blit(self.player.getGUI(), (0, 0))
        
        return surf

    def mainLoop(game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in '1234567890':
                    game.player.answer += key
                elif key in KEYPAD:
                    game.player.answer += key[1:-1]
                elif event.key in (pygame.K_KP_MINUS, pygame.K_MINUS):
                    game.player.negative = not game.player.negative
                elif event.key == pygame.K_BACKSPACE:
                    game.player.answer = game.player.answer[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and game.player.getSelected() != None:
                    game.player.launch()

        if not pygame.mixer.get_busy():
            game.channel.queue(assets.loop1)
        
        if game.enemy.canSpawn():
            game.enemy.spawn()

        game.display.fill(colors.white)
        game.display.blit(game.updateGetSurface(), (0, 0))
        pygame.display.update()

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
    totalhp = 10
    score = 100
    answer = ''
    negative = False
    game = None
    abms = []
    lastFired = 0

    def __init__(self, gameInstance):
        self.game = gameInstance
        self.lasers = [] # Prevent them from linking

    class ABM():
        
        speed = 250
        player = None
        correct = False
        target = 0
        enemy = None
        y = 0
        start = 0
        
        def __init__(self, player, e, target):
            self.player = player
            self.correct = player.isCorrect()
            self.enemy = e
            self.target = target
            self.y = e.y
            self.start = time.time()

        def __repr__(self):
            template = 'Player.ABM(target={},x={},hasArrived={})'
            return template.format(self.target, self.getX(), self.hasArrived())

        def getX(self):
            elapsed = time.time() - self.start
            return int(self.player.game.resolution[0] - self.speed * elapsed)

        def hasArrived(self):
            return self.getX() <= self.target

        def getPos(self):
            return (self.getX(), self.y)

        def explode(self):
            explosion = None
            if self.correct:
                explosion = sprites.spriteAnimation(assets.explosionABMS, 30)
            else:
                explosion = sprites.spriteAnimation(assets.explosionABMF, 30)
            explosion.start()
            self.player.game.explosions.append((explosion, self.getPos()))
            self.player.abms.remove(self)

    def launch(self):
        e = self.getSelected()
        if e != None:
            rect = e.getRect()
            x = self.game.enemy.getX(e)
            rect.topright = (x, e.y)
            self.abms.append(Player.ABM(self, e, rect.right))
            self.answer = ''
            self.isNegative = False

    def getAnswer(self):
        return ('-' if self.negative else '') + self.answer
            
    def isCorrect(self):
        return self.getSelected().isCorrect(self.getAnswer())     
    
    def getSelected(self):
        w, h = self.game.resolution
        for e in self.game.enemy.enemies:
            x = self.game.enemy.getX(e)
            rect = e.getSurface().get_rect()
            rect.topright = (x, e.y)
            if rect.collidepoint(pygame.mouse.get_pos()):
                return e
        return None

    def getGUI(self):

        w, h = self.game.resolution
        
        gui = pygame.Surface(self.game.resolution, pygame.SRCALPHA, 32)
        
        level = self.getLevel()
        
        hpBarRect = pygame.Rect(0, 0, 150, 12)
        hpBarRect.topright = (w - 30, 10)
        hpBar = pgrsBar(
            self.hp / self.totalhp,
            hpBarRect,
            colors.blue, colors.navy_blue
        )

        hpText = pgrsFont.render('{}/{} lives'.format(self.hp, self.totalhp), True, colors.white)
        hpTextRect = hpText.get_rect()
        hpTextRect.center = hpBarRect.center

        timerText = pgrsFont.render(secToMS(int(time.time() - self.game.start)), True, colors.black)
        timerRect = timerText.get_rect()
        timerRect.midright = hpBarRect.midleft

        scoreToNextRect = pygame.Rect(0, 0, 150, 12)
        scoreToNextRect.topright = w - 30, 10 + 12 + 5
        scoreToNextBar = pgrsBar(
            self.getPgrsToNext(),
            scoreToNextRect,
            colors.red, colors.orange
        )
        
        scoreText = pgrsFont.render('{} pts'.format(self.score), True, colors.black)
        scoreRect = scoreText.get_rect()
        scoreRect.midright = scoreToNextRect.midleft

        levelText = pgrsFont.render('Level {}'.format(self.getLevel()), True, colors.black)
        levelRect = levelText.get_rect()
        levelRect.center = scoreToNextRect.center
        
        gui.blit(hpBar, hpBarRect)
        gui.blit(hpText, hpTextRect)
        gui.blit(timerText, timerRect)
        gui.blit(scoreToNextBar, scoreToNextRect)
        gui.blit(scoreText, scoreRect)
        gui.blit(levelText, levelRect)

        return gui.convert_alpha()

    @staticmethod
    def ptsToLevel(level):
        return 25 * level**2 - 25 * level # Level 2: 50, increases by 25

    @staticmethod
    def ptsBetweenLevels(l1, l2):
        return abs(Player.ptsToLevel(l1) - Player.ptsToLevel(l2))
    
    def getLevel(self):
        lvl = enemy.cap(((625 + 100*self.score)**0.5 + 25) / 50, 1, None)
        lvl = lvl - lvl % 1
        return int(lvl)

    def getScoreToNext(self):
        nextLevel = self.getLevel() + 1
        ptsToLast = Player.ptsToLevel(self.getLevel())
        ptsAfterLast = self.score - ptsToLast
        total = Player.ptsBetweenLevels(self.getLevel(), nextLevel)
        return total - ptsAfterLast

    def getPgrsToNext(self):
        nextLevel = self.getLevel() + 1
        ptsToLast = Player.ptsToLevel(self.getLevel())
        ptsAfterLast = self.score - ptsToLast
        total = Player.ptsBetweenLevels(self.getLevel(), nextLevel)
        return ptsAfterLast / total
        
        
class EnemyManager():
    '''
    Enemy handler class. Handles the enemies.
    '''

    available = []
    enemies = []    
    lastSpawn = 0
    game = None
    
    def __init__(self, gameInstance, *availableEnemies):
        self.game = gameInstance
        self.available = availableEnemies
        self.enemies = [] # Prevent them from linking

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
        e = ToSpawn(self.game.player.getLevel(), randint(0, h - 64))
        self.enemies.append(e)
        self.lastSpawn = time.time()

    def getX(self, enemy):
        w, h = self.game.resolution
        return int(w * enemy.getProgress())

    def getSurface(self):
        surf = pygame.Surface(self.game.resolution, pygame.SRCALPHA, 32)
        for e in self.enemies:
            x = self.getX(e)
            missile = e.getSurface()
            rect = missile.get_rect()
            rect.topright = (x, e.y)
            surf.blit(e.getSurface(), rect)
        return surf

    def handleEnemies(self):
        for e in self.enemies:
            if e.getProgress() >= 1:
                self.enemies.remove(e)
                self.game.player.hp -= 2

    def explode(self, e):
        rect = e.getRect()
        rect.topright = (self.getX(e), e.y)
        exp = e.getExplosion()
        exp.start()
        self.game.explosions.append((exp, rect.midright))
        self.enemies.remove(e)
        

def pgrsBar(progress, rect, fgColor, bgColor):
    surf = pygame.Surface(rect.size)
    surf.fill(bgColor)
    pgrs = pygame.Rect(0, 0, int(rect.w * progress), rect.h)
    pygame.draw.rect(surf, fgColor, pgrs)
    return surf

KEYPAD = '] ['.join('[1,2,3,4,5,6,7,8,9,0]'.split(',')).split(' ')
RESOLUTION = (640, 480)

def secToMS(t):
    minutes = int(t / 60)
    seconds = t % 60
    return '{0}:{1:0>2}'.format(minutes, seconds)

def main():
    
    pygame.init()

    game = Game((640, 480))

    while True:
        game.mainLoop()
        
if __name__ == '__main__':
    
    main()
