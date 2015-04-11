import random

import pygame

pygame.font.init()

equationFont = pygame.font.Font('freesansbold.ttf', 20)

class Enemy():

    level = 0
    equation = ''
    solution = {0}

    def __init__(self, level):
        self.level = level
        self.solution, expressions = type(self).generate(level)
        random.shuffle(expressions)
        self.equation = ' = '.join(expressions)

    def __str__(self):
        return '{}; x = {}'.format(self.equation, self.solutions)

    '''
    Subclass and override

    Expected: {int} solution(s) and [str, str]
    expressions that equal each other
    NOTE: This is STATIC and should be called from
    the CLASS!
    '''
    @staticmethod
    def generate(level):
        raise ValueError('Subclass me')

    '''
    Subclass and override

    Expected: float representing the seconds
    needed to cross
    '''
    def getTime(self):
        raise ValueError('Override me')
    
    '''
    Subclass and override

    Expected: int representing the points
    recieved from solving
    '''
    def getValue(self):
        raise ValueError('Override me')

    '''
    Subclass and override

    Expected: int representing number of chips
    in the "pot" of selecting what number
    NOTE: This is STATIC and should be called
    from the CLASS!
    '''
    @staticmethod
    def getChance():
        raise ValueError('Override me')
    
class Level1(Enemy):
    '''
    A simple equation
    Example: x + 4 = 9
    Begins spawning at level 1
    '''
    
    @staticmethod
    def generate(level):
        
        x = random.randint(-50, 50)
        b = random.randint(-50, 50)
        y = x + b
        
        b = strAdd(b)

        exps = ['x {}'.format(b), str(y)]

        return {x}, exps

    def getTime(self):
        
        time = -2 * self.level + 15
        if level > 5:
            time = 5
        return time

    def getValue(self):
        return 50

    @staticmethod
    def getChance(level):
        
        chance = -10 * level + 100
        if level > 10:
            chance = 0
        return chance

class Level2(Enemy):
    '''
    A slightly more complex equation
    Example: 3x + 2 = 5
    Begins spawning at level 2
    '''

    @staticmethod
    def generate(level):
        
        m, x, b, y = genL2()
        
        m = strCoeff(m)
        b = strCoeff(b)
            
        exps = ['{}x {}'.format(m, b), str(y)]

        return {x}, exps

    def getTime(self):
        
        time = -(self.level - 1) + 25
        if time < 10:
            time = 10
        return time

    def getValue(self):

        return 100

    @staticmethod
    def getChance(level):
        
        if level < 2:
            return 0
        return 150

class Level3(Enemy):
    '''
    A 'two-step' equation
    Example: 3x + 4 = 4x + 3
    Begins spawning at level 6
    '''

    @staticmethod
    def generate(level):
        
        m1, x, b1, y = genL2()

        m2 = random.randint(-10, 10)
        b2 = y - m2 * x
        
        m1 = strCoeff(m1)
        m2 = strCoeff(m2)
        b1 = strAdd(b1)
        b2 = strAdd(b2)

        exps = ['{}x {}'.format(m1, b1), '{}x {}'.format(m2, b2)]

        return {x}, exps

    def getTime(self):

        time = -self.level + 30
        if time < 15:
            time = 15
        return time

    def getValue(self):

        return 200

    @staticmethod
    def getChance(level):

        if level < 6:
            return 0
        chance = 5 * (level - 5)
        if chance > 150:
            chance = 150
        return chance

class Level4(Enemy):
    '''
    A binomial factor pair
    Example: (3x + 2)(5x - 1) = 0
    Begins spawning at level 10
    '''

    @staticmethod
    def generate(level):
        
        m1, x1, b1, m2, x2, b2 = genL4()

        m1 = strCoeff(m1)
        m2 = strCoeff(m2)
        b1 = strAdd(b1)
        b2 = strAdd(b2)
        
        equation = '({}{})({}{})'.format(m1, b1, m2, b2)
        
        return {x1, x2}, [equation, '0']

    def getTime(self):

        return 30 * 0.95 ** (self.level - 15) + 10
    
    def getValue(self):

        return 500

    @staticmethod
    def getChance(level):

        if level < 10:
            return 0
        chance = 10 * 1.25 ** (level - 10)
        if chance > 200:
            chance = 200
        return chance

class Level5(Enemy):
    '''
    A trinomial
    Example: x^2 + 9x + 10 = -10
    Begins spawning at level 15
    '''

    @staticmethod
    def generate(level):

        b1 = random.randint(-10, 10)
        if b1 == 0:
            b1 = random.randint(1, 10)
        b2 = random.randint(-10, 10)
        if b2 == 0:
            b2 = random.randint(1, 10)

        b, c = b1 + b2, b1 * b2
        
        b = strCoeffAdd(b)
        c = strAdd(c)
        
        return {b1, b2}, ['x^2{}{}'.format(b, c), '0']
    
    def getTime(self):

        return 35 * 0.95 ** (self.level - 15) + 10
        
    def getValue(self):

        return 750

    @staticmethod
    def getChance(level):
        if level < 15:
            return 0
        chance = 25 * 1.10 ** (level - 15)
        if chance > 200:
            chance = 200
        return chance

def genL2():
    
    x = random.randint(-10, 10)
    
    m = random.randint(-10, 9)
    if m == 0:
        m = 10
        
    b = random.randint(-10, 9)
    if b == 0:
        b = 10
        
    y = m * x + b

    return m, x, b, y

def genL4():
    
    m1, x1, b1, y1 = genL2()
    m2, x2, b2, y2 = genL2()
    
    b1 = b1 - y1
    b2 = b2 - y2
    
    return m1, x1, b1, m2, x2, b2

def strCoeff(n):
    if n == -1:
        n = '-x'
    elif n == 0:
        n = ''
    elif n == 1:
        n = 'x'
    else:
        n = '{}x'.format(n)
    return n

def strCoeffAdd(n):
    if n == -1:
        n = '- x'
    elif n < 0:
        n = ' - {}x'.format(abs(n))
    elif n == 0:
        n = ''
    elif n == 1:
        n = ' + x'
    elif n > 1:
        n = ' + {}x'.format(n)
    return n

def strAdd(n):
    if n < 0:
        n = ' - {}'.format(abs(n))
    elif n == 0:
        n = ''
    elif n > 0:
        n = ' + {}'.format(n)
    return n

def factorsOf(n):
    for i in range(1, n):
        if n % i == 0:
            yield i
    yield n
        
def main():
    e = Level5(1)
    print(e.equation)
    input()
    print(e.solution)
    
if __name__ == '__main__':
    main()
