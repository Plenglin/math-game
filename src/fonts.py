import pygame
from pygame.font import Font

from common import draw


pygame.font.init()

font = lambda size: Font('freesansbold.ttf', size)

s2  = Font('freesansbold.ttf', 12)
s3  = Font('freesansbold.ttf', 20)
s4  = Font('freesansbold.ttf', 36)
s5  = Font('freesansbold.ttf', 54)
s6  = Font('freesansbold.ttf', 75)
s7  = Font('freesansbold.ttf', 100)
s8  = Font('freesansbold.ttf', 200)

def pixelStrDim(string, font):
    """
    Get the dimensions of a specified string in a specified font
    """
    rect = font.render(string, True, (0, 0, 0)).get_rect()
    return rect.width, rect.height

def formatParagraph(string, AA, color, font, width):
    """
    Format the string with correct line breaks and everything
    """
    lines = []
    words = string.split()
    strLength, strHeight = pixelStrDim(string, font)
    bufferString = []
    for word in words:
        bufferString.append(word)
        strLen, _ = pixelStrDim(' '.join(bufferString), font)
        if strLen > width:
            bufferString = bufferString[:-1]
            lines.append(' '.join(bufferString))
            bufferString = [word]
    lines.append(' '.join(bufferString))
    surface = draw.alphaSurface((strLength, strHeight * len(lines)))
    for pair in enumerate(lines):
        line = pair[0]
        string = pair[1]
        surface.blit(font.render(string, AA, color), (0, strHeight * line))
    return surface        

if __name__ == '__main__':
    import sys
    from common import colors
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    while True:
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        x = 0
        for n, font in enumerate((s2, s3, s4, s5, s6, s7, s8)):
            display.blit(font.render(str(n), True, (255, 255, 255)), (x, 0))
            x += 50
        pygame.display.update()
