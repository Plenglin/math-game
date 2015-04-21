import time

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

class Animation():

    frames = []
    starttime = 0
    fps = 0

    def __init__(self, frames, fps):
        self.frames = frames
        self.fps = fps

    def copy(self):
        return Animation(self.frames, self.fps)

    def start(self):
        self.starttime = time.time()

    def getFrames(self):
        return len(self.frames)

    def getFrame(self):
        timeElapsed = time.time() - self.starttime
        frame = int(timeElapsed * self.fps)
        return frame

    def getSurface(self):
        if not self.isFinished():
            return self.frames[self.getFrame()]
        else:
            return self.frames[self.getFrames() - 1]

    def isFinished(self):
        return self.getFrames() - 1 < self.getFrame()

    def getRect(self):
        return self.frames[0].get_rect()

def spriteAnimation(surf, fps):
    w, h = surf.get_size()
    sheet = Spritesheet(surf, (h, h))
    frames = []
    for x in range(0, int(w / h)):
        frames.append(sheet.get(x, 0))
    return Animation(frames, fps)

def main():
    import assets
    pygame.init()
    d = pygame.display.set_mode((640, 480))
    explosionAnimation = spriteAnimation(assets.explosion1, 24)
    explosionAnimation.start()
    while True:
        d.fill(colors.white)
        d.blit(explosionAnimation.getSurface(), (0, 0))
        pygame.display.update()
        

if __name__ == '__main__':
    main()
