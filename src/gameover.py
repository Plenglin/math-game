import json

import pygame

import colors


ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyz1234567890'
CHARLIMIT = 16
NOTIFICATION = ('You have made it into the high scores! Please enter your name' +
    'using alphanumeric characters (a-z, 0-9)')

def getHighScores():
    scores = {}
    with open('highscores.json', 'r') as file:
        scores = json.loads(file.read())
    return scores

def scoreBeatsRecord(score):
    scores = getHighScores()
    for k, v in scores.items():
        if score > v:
            diffs = {}
            for k, v in scores.items():
                d = score - v
                if d > 0:
                    diffs[d] = k
            leastDiff = min(diffs)
            print(leastDiff)
            return diffs[leastDiff]
    return None

def endscreen(display, score):
    displayrect = display.get_rect()
    recordBeat = scoreBeatsRecord(score)
    largeFont = pygame.font.Font('freesansbold.ttf', 64)
    textFont = pygame.font.Font('freesansbold.ttf', 20)
    if recordBeat != None:
        getInput = True
        name = ''
        note = largeFont.render(NOTIFICATION, True, colors.white)
        noteRect = note.get_rect()
        noteRect.midbottom = displayrect.center
        doBreak = False
        while True:
            display.fill(colors.black)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    k = pygame.key.name(event.key)
                    if k in ALPHANUMERIC and len(name) <= CHARLIMIT:
                        name += k
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[0:-1]
                    elif event.key == pygame.K_RETURN:
                        doBreak = True
            if doBreak:
                break
            nameSurf = textFont.render(name, True, colors.white)
            nameRect = nameSurf.get_rect()
            nameRect.midtop = noteRect.midbottom
            display.blit(note, noteRect)
            display.blit(nameSurf, nameRect)
            pygame.display.update()

def main():
    print(getHighScores())
    print(scoreBeatsRecord(600))

if __name__ == '__main__':
    main()
