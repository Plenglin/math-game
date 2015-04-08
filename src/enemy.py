import random
import re

import pygame

pygame.font.init()

equationFont = pygame.font.Font('freesansbold.ttf', 20)

class Enemy():

    level = 0
    equation = ''
    solutions = 0

    def __init__(self, level):
        self.level = level
        self.solutions, self.equation = self.generate()

    def __str__(self):
        return '{}; x = {}'.format(self.equation, self.solutions)

    '''
    Subclass and override

    Expected: {int} solution(s) and str equation
    '''
    def generate(self):
        raise ValueError('Subclass me')

    '''
    Subclass and override

    Expected: int representing number of chips
    in the "pot" of selecting what number
    '''
    def getChance(self):
        raise ValueError('Override me')

    '''
    Subclass and override

    Expected: float representing the seconds
    needed to cross
    '''
    def getSpeed(self):
        raise ValueError('Override me')
    
    '''
    Subclass and override

    Expected: int representing the points
    recieved from solving
    '''
    def getValue(self):
        raise ValueError('Override me')
    
class Level1(Enemy):
    '''
    A simple equation
    Example: x + 4 = 9
    Begins spawning at level 1
    '''

    def generate(self):
        
        x = random.randint(-20, 20)
        
        b = random.randint(-10, 10)
        y = x + b
        
        if b < 0:
            b = '- {}'.format(-b)
        else:
            b = '+ {}'.format(b)
            
        exps = ['x {}'.format(b), str(y)]
        random.shuffle(exps)

        return {x}, ' = '.join(exps)

    def getChance(self, level):
        
        chance = -10 * level + 100
        if level > 10:
            chance = 0
        return chance

    def getSpeed(self):
        
        time = -2 * self.level + 15
        if level > 5:
            time = 5
        return time

    def getValue(self):
        return 50

class Level2(Enemy):
    '''
    A slightly more complex equation
    Example: 3x + 2 = 5
    Begins spawning at level 2
    '''

    def generate(self):
        
        x = random.randint(-10, 10)
        
        m = random.randint(-9, 9)
        if m == 0:
            m = random.randint(1, 10)
        b = random.randint(-10, 10)
        y = m * x + b
        
        if m == 1:
            m = ''
        if b < 0:
            b = '- {}'.format(-b)
        else:
            b = '+ {}'.format(b)
            
        exps = ['{}x {}'.format(m, b), str(y)]
        random.shuffle(exps)

        return {x}, ' = '.join(exps)

    def getChance(self, level):
        
        if level < 2:
            return 0
        return 150

    def getSpeed(self):
        
        time = -(self.level - 1) + 25
        if time < 10:
            time = 10
        return time

    def getValue(self):

        return 100

class Level3(Enemy):
    '''
    A 'two-step' equation
    Example: 3x + 4 = 4x + 3
    Begins spawning at level 6
    '''

    def generate(self):
        
        x = random.randint(-10, 10)
        
        m1 = random.randint(-9, 9)
        m2 = random.randint(-9, 9)       
        if m1 == 0:
            m1 = random.randint(1, 9)
        if m2 == 0:
            m2 = random.randint(1, 9)
        if m1 == m2:
            return self.generate()
        b1 = random.randint(-9, 9)
        b2 = (m1 - m2) * x + b1
        
        if m1 == 1:
            m1 = ''
        elif m1 == -1:
            m1 = '-'
            
        if m2 == 1:
            m2 = ''
        elif m2 == -1:
            m2 = '-'
            
        if b1 < 0:
            b1 = '- {}'.format(-b1)
        else:
            b1 = '+ {}'.format(b1)
            
        if b2 < 0:
            b2 = '- {}'.format(-b2)
        else:
            b2 = '+ {}'.format(b2)

        exps = ['{}x {}'.format(m1, b1), '{}x {}'.format(m2, b2)]
        random.shuffle(exps)

        return {x}, ' = '.join(exps)

    def getChance(self, level):

        if level < 6:
            return 0
        chance = 5 * (level - 5)
        if chance > 50:
            chance = 50
        return chance

    def getSpeed(self):

        time = -self.level + 30
        if time < 15:
            time = 15
        return time

    def getValue(self):

        return 200

class Level4(Enemy):
    '''
    A binomial factor pair
    Example: (3x + 2)(5x - 1) = 0
    Begins spawning at level 10
    '''

    def generate(self):
        
        s1, b1 = Level2.generate(Level2(1))
        s2, b2 = Level2.generate(Level2(1))
        
        return {s1.pop(), s2.pop()}, b1

    def getChance(self, level):

        if level < 10:
            return 0
        chance = 10 * 1.25 ** (level - 10)
        if chance > 125:
            chance = 125
        return chance

    def getSpeed(self):

        pass
    
    def getValue(self):

        return 500

class Level5(Enemy):
    '''
    A trinomial
    Example: x^2 + 9x + 10 = -10
    Begins spawning at level 15
    '''

    def generate(self):

        pass
    
    def getChance(self, level):
        if level < 15:
            return 0
        chance = 25 * 1.10 ** (level - 15)
        # Yes, uncapped. Stop hogging the machine.
        return chance
    
    def getSpeed(self):

        pass
        
    def getValue(self):

        return 750
        
def main():
    foo = Level4(1)
    print(foo)
    
if __name__ == '__main__':
    main()
