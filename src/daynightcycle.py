import math
import time

import pygame

CYCLESPEED = 1

def main():
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 12)
    display = pygame.display.set_mode((640, 480))
    while True:
        cycle = time.time() * CYCLESPEED * math.pi
        r = cap(0 + 255 * math.cos(cycle), 0, 255)
        g = cap(128 + 128 * math.sin(cycle + 2), None, 128)
        b = 128 + 128 * math.sin(cycle)
        print(int(r), int(g), int(b))
        display.fill((r, g, b))
        display.blit(font.render(str(b), True, (0, 0, 0)), (0, 0))
        pygame.display.update()

def cap(n, min=None, max=None):
    if min != None and n < min:
        return min
    elif max != None and n > max:
        return max
    return n

if __name__ == '__main__':
    main()
