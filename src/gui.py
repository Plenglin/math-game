import pygame


class GUI():

    '''
    Names is a dictionary of string: function returning something
    '''
    names = {}
    resolution = (0, 0)
    elements = []

    def __init__(self, names, resolution, *elements):
        self.names = names
        self.resolution = resolution
        self.elements = []
        for e in elements:
            e.link(self)
            self.elements.append(e)

    def add(self, element):
        element.link(self)
        self.elements.append(element)

class Element():

    pos = (0, 0)
    proportional = False # Should the positioning be relative to screen size?
    align = None

    def getSurface(self):
        pass

class Text(Element):

    text = ''
    names = {}
    font = None
    color = None
    gui = None

    def __init__(self, text, font, color, pos, names={}, proportional=False):
        self.pos = pos
        self.text = text
        self.font = font
        self.color = color
        # Prevent links
        if names == {}:
            self.names = {}
        else:
            self.names = names
        self.proportional = proportional

    def link(self, gui):
        self.gui = gui

    def getSurface(self):
        names = {k: f() for k, f in self.gui.names.items()}
        s = self.font.render(text.format(**names), True, color)
        return s

class ProgBar(Text):

    rect = None
    bgColor = None
    fgColor = None
    progress = 0

    def __init__(self, text, font, textColor, bgColor, fgColor, rect, proportional=False):
        super().__init__(self, text, font, textColor, pygame.Rect(rect).topleft, proportional)
        self.rect = pygame.Rect(rect)
        self.bgColor = bgColor
        self.fgColor = fgColor

    def setProgress(self, progress):
        self.progress = progress

    def getSurface(self):
        text = super().getSurface(self)
        totalRect = self.rect.copy()
        progRect = self.rect.copy()
        surf = pygame.Surface(totalRect.size)
        surf.fill(self.bgColor)
        pygame.draw.rect(surf, self.fgColor, progRect)
        surf.blit(text, (0, 0))
        return surf


def dictMerge(x, y):
    z = x.copy()
    z.update(y)
    return z

def main():
    pass

if __name__ == '__main__':
    main()
