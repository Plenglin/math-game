import sys
import time
from random import choice, randint, random

import pygame

import assets
import colors
import enemy
import sprites


pgrsFont = pygame.font.Font('freesansbold.ttf', 12)
abmlFont = pygame.font.Font('freesansbold.ttf', 20)

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
    
    def __init__(self, display):
        self.start = time.time()
        self.resolution = display.get_size()
        self.display = display
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
        screenrect = pygame.Rect(0, 0, w, h)
        mx, my = pygame.mouse.get_pos()

        #self.player.score = int((time.time() - self.start) * 100) # FOR TEST ONLY
        
        surf = pygame.Surface(self.resolution)
        surf.fill(colors.white)

        bgRect = assets.background.get_rect()
        bgRect.midright = screenrect.midright
        surf.blit(assets.background, bgRect)
        
        surf.blit(self.enemy.getSurface(), (0, 0))
        
        for abm in self.player.abms:
            surf.blit(abm.getSurface(), abm.getPos())
            if abm.hasArrived():
                abm.explode()

        for e, p in self.explosions:
            rect = e.getRect()
            rect.center = p
            surf.blit(e.getSurface(), rect)
            if e.isFinished():
                self.explosions.remove((e, p))

        for e in self.enemy:
            if e.getProgress() >= 1:
                e.explode()
                self.player.hp -= 1
                self.player.combo = 1
            elif e.canExplode():
                e.explode()

        if self.player.hp == 0:
            raise Exception()

        abml = None
        if self.player.lastMouseY == my:
            abml = self.player.lastABML
        elif self.player.lastMouseY < my:
            abml = assets.abmLauncherDown.copy()
        elif self.player.lastMouseY > my:
            abml = assets.abmLauncherUp.copy()
        self.player.lastABML = abml.copy()

        abml = self.player.getABML()
        abmlRect = abml.get_rect()
        abmlRect.midright = (w, my)

        abmlText = abmlFont.render(self.player.getAnswer(), True, colors.white)
        abmlTextRect = abmlText.get_rect()
        abmlTextRect.center = abmlRect.center

        surf.blit(abml, abmlRect)
        surf.blit(abmlText, abmlTextRect)
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
                if event.button == 1 and game.player.canLaunch():
                    game.player.launch()
                    game.player.negative = False

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

    hp = 5
    totalhp = 5
    score = 0
    answer = ''
    negative = False
    game = None
    abms = []
    combo = 1
    
    lastMouseY = 0
    lastABML = None
    abmh = None

    def __init__(self, gameInstance):
        self.game = gameInstance
        self.lasers = [] # Prevent them from linking
        self.lastABML = assets.abmLauncherUp.copy()
        self.abmh = self.getABMHolder()
        self.abmh.start()

    def getABMHolder(self):
        return sprites.spriteAnimation(assets.abmHolder, 6)

    def getABML(self):
        s = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
        s.blit(self.lastABML, (0, 0))
        s.blit(self.abmh.getSurface(), (0, 0))
        return s

    def canLaunch(self):
        return self.abmh.isFinished() and self.getSelected() != None and self.answer != ''

    def launch(self):
        e = self.getSelected()
        if self.canLaunch():
            rect = e.getRect()
            x = self.game.enemy.getX(e)
            rect.topright = (x, e.y)
            self.abms.append(ABM(self, self.getAnswer(), e, rect.right))
            self.answer = ''
            self.isNegative = False
            self.abmh.start()
        else:
            raise Exception('Cannot launch')

    def getAnswer(self):
        neg = '-' if self.negative else ''
        if self.answer == '':
            return ''
        return neg + self.answer
            
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

        mx, my = pygame.mouse.get_pos()
        self.lastMouseY = my
        
        gui = pygame.Surface(self.game.resolution, pygame.SRCALPHA, 32)
        
        level = self.getLevel()
        
        hpBarRect = pygame.Rect(0, 0, 150, 12)
        hpBarRect.topright = (w - 30, 10)
        hpBar = pgrsBar(
            self.hp / self.totalhp,
            hpBarRect,
            colors.pink, colors.navy_blue
        )

        hpText = pgrsFont.render('{}/{} lives'.format(self.hp, self.totalhp), True, colors.white)
        hpTextRect = hpText.get_rect()
        hpTextRect.center = hpBarRect.center

        timerText = pgrsFont.render(secToMS(int(time.time() - self.game.start)), True, colors.white)
        timerRect = timerText.get_rect()
        timerRect.midright = hpBarRect.midleft

        scoreToNextRect = pygame.Rect(0, 0, 150, 12)
        scoreToNextRect.topright = w - 30, 10 + 12 + 5
        scoreToNextBar = pgrsBar(
            self.getPgrsToNext(),
            scoreToNextRect,
            colors.red, colors.orange
        )
        
        scoreText = pgrsFont.render('{} pts'.format(self.score), True, colors.orange)
        scoreRect = scoreText.get_rect()
        scoreRect.midright = scoreToNextRect.midleft

        levelText = pgrsFont.render('Level {}'.format(self.getLevel()), True, colors.black)
        levelRect = levelText.get_rect()
        levelRect.center = scoreToNextRect.center

        combo = 'x{}' if self.combo > 1 else ''
        comboText = pgrsFont.render(combo.format(self.combo), True, colors.white)
        comboRect = comboText.get_rect()
        comboRect.midleft = scoreToNextRect.midright
        
        gui.blit(hpBar, hpBarRect)
        gui.blit(hpText, hpTextRect)
        gui.blit(timerText, timerRect)
        gui.blit(scoreToNextBar, scoreToNextRect)
        gui.blit(scoreText, scoreRect)
        gui.blit(levelText, levelRect)
        gui.blit(comboText, comboRect)

        return gui.convert_alpha()

    def ptsToLevel(self, level):
        a = 75
        b = -75
        lvl = a*level**2 + b*level
        return lvl

    def ptsBetweenLevels(self, l1, l2):
        return abs(self.ptsToLevel(l1) - self.ptsToLevel(l2))
    
    def getLevel(self):
        a = 75
        b = -75
        lvl = ((5625 + 300*self.score)**0.5 + 75) / 150
        return int(lvl)

    def getScoreToNext(self):
        nextLevel = self.getLevel() + 1
        ptsToLast = self.ptsToLevel(self.getLevel())
        ptsAfterLast = self.score - ptsToLast
        total = self.ptsBetweenLevels(self.getLevel(), nextLevel)
        return total - ptsAfterLast

    def getPgrsToNext(self):
        nextLevel = self.getLevel() + 1
        ptsToLast = self.ptsToLevel(self.getLevel())
        ptsAfterLast = self.score - ptsToLast
        total = self.ptsBetweenLevels(self.getLevel(), nextLevel)
        return ptsAfterLast / total

class ABM():
        
    speed = 250
    player = None
    correct = False
    target = 0
    enemy = None
    y = 0
    start = 0
    ans = 0
    
    def __init__(self, player, ans, e, target):
        self.player = player
        self.ans = ans
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

    def getSurface(self):
        s = assets.abm.copy()
        srect = s.get_rect()
        t = abmlFont.render(str(self.ans), True, colors.gray(50))
        trect = t.get_rect()
        trect.center = srect.center
        s.blit(t, trect)
        return s

    def explode(self):
        explosion = None
        if self.correct:
            explosion = sprites.spriteAnimation(assets.explosionABMS, 30)
            s = []
            a = int(self.ans)
            for i in self.enemy.solution:
                if i != a:
                    s.append(i)
            self.enemy.solution = s
            self.player.abmh = self.player.getABMHolder()
            self.player.score += self.enemy.getValue() * self.player.combo
            lastcombo = self.player.combo
            self.player.combo += 1
            if self.player.combo % 10 == 0:
                self.player.hp += 1
        else:
            explosion = sprites.spriteAnimation(assets.explosionABMF, 30)
            self.player.combo = 1
        explosion.start()
        self.player.game.explosions.append((explosion, self.getPos()))
        self.player.abms.remove(self)
        
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

    def __iter__(self):
        for e in self.enemies:
            yield e

    def spawnchoices(self):
        chips = []
        for enemy in self.available:
            toAdd = enemy.getChance(self.game.player.getLevel())
            for chip in range(0, toAdd):
                chips.append(enemy)
        return chips

    def canSpawn(self):
        return time.time() > self.nextSpawn() or len(self.enemies) == 0
            
    def nextSpawn(self):
        return self.lastSpawn + self.game.player.getLevel() + 10

    def spawn(self):
        w, h = self.game.resolution
        ToSpawn = choice(self.spawnchoices())
        e = ToSpawn(self, randint(0, h - 64))
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

def pgrsBar(progress, rect, fgColor, bgColor):
    surf = pygame.Surface(rect.size)
    surf.fill(bgColor)
    if progress > 0:
        pgrs = pygame.Rect(1, 1, int(rect.w * progress) - 2, rect.h - 2)
    else:
        pgrs = pygame.Rect(0, 0, 0, 0)
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

    d = pygame.display.set_mode((640, 480))

    game = Game(d)

    while True:
        game.mainLoop()
        
if __name__ == '__main__':
    
    main()
