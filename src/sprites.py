import pygame

import colors

class Spritesheet():

    surface = None
    size = (0, 0)

    def __init__(self, surface, size):
        self.surface = surface
        self.size = size

    def get(self, x, y):
        surf = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        croparea = (x * self.size[0], y * self.size[1], self.size[0], self.size[1])
        surf.blit(self.surface, (0, 0), croparea)
        return surf.convert_alpha()


def main():
    pygame.init()
    rockets = pygame.image.load('assets/rockets.png')
    rsheet = Spritesheet(rockets, (64, 64))
    d = pygame.display.set_mode((640, 480))
    while True:
        d.fill(colors.white)
        d.blit(rsheet.get(0, 3), (0, 0))
        d.blit(rsheet.get(0, 2), (64, 0))
        pygame.display.update()
        

if __name__ == '__main__':
    main()
