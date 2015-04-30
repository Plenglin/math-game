import json
import random

import pygame

import assets
import colors
import main as MAIN


ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyz1234567890'
CHARLIMIT = 16

def getHighScores():
    with open('highscores.json', 'r') as file:
        scores = json.loads(file.read())
    return scores

def scoreBeatsRecord(score):
    scores = getHighScores()
    for n, s in scores:
        if score > s:
            return True
    return False

def endscreen(display, player):

    score = player.score

    displayrect = display.get_rect()
    largeFont = pygame.font.Font('freesansbold.ttf', 30)
    textFont = pygame.font.Font('freesansbold.ttf', 20)
    name = ''
    scores = getHighScores()

    if scoreBeatsRecord(score):
        name = ''
        note = assets.recordBreak.copy()
        noteRect = note.get_rect()
        noteRect.midbottom = displayrect.center
        doBreak = False

        while True:
            display.fill(colors.black)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    k = pygame.key.name(event.key)
                    if k in ALPHANUMERIC and len(name) <= CHARLIMIT:
                        name += k.upper()
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[0:-1]
                    elif event.key == pygame.K_RETURN:
                        doBreak = True
            if not pygame.mixer.get_busy():
                assets.loop1.play()
            if doBreak:
                break
            nameSurf = textFont.render(name, True, colors.white)
            nameRect = nameSurf.get_rect()
            nameRect.midtop = noteRect.midbottom
            display.blit(note, noteRect)
            display.blit(nameSurf, nameRect)
            pygame.display.update()

        del scores[9]
        scores.append([name, score])
        scores.sort(key=lambda x: x[1], reverse=True)

    with open('highscores.json', 'w+') as file:
        file.write(json.dumps(scores, sort_keys=True, indent=4))

    try:
        acc = '{}% accuracy'.format(round(player.correct / player.total, 4) * 100)
    except ZeroDivisionError:
        acc = '0% accuracy'

    finalscore = largeFont.render('Your score: {}'.format(score), True, colors.white)
    finalscorerect = finalscore.get_rect()

    accuracy = largeFont.render(acc, True, colors.white)
    accuracyrect = accuracy.get_rect()

    correct = largeFont.render('{} correct'.format(player.correct), True, colors.white)
    correctrect = correct.get_rect()

    survived = largeFont.render('Survived {}'.format(player.survived), True, colors.white)
    survivedrect = survived.get_rect()

    presskey = textFont.render('Press any key to continue', True, colors.white)
    presskeyrect = presskey.get_rect()
    presskeyrect.midbottom = displayrect.midbottom

    correctrect.bottomleft = displayrect.center
    correctrect.left += 100
    finalscorerect.bottomleft = correctrect.topleft
    accuracyrect.topleft = correctrect.bottomleft
    survivedrect.topleft = accuracyrect.bottomleft

    highscores = pygame.Surface((350, 420), pygame.SRCALPHA, 32)
    highscoresrect = highscores.get_rect()
    highscoresrect.midright = displayrect.center
    c = colors.white
    n = 0
    for name, s in scores:
        highscores.blit(largeFont.render(str(n+1), True, c), (0, n*40))
        highscores.blit(textFont.render(name.upper(), True, c), (50, n*40))
        highscores.blit(textFont.render(str(s), True, c), (250, n*40))
        n += 1

    highscorestitle = largeFont.render('High Scores', True, colors.white)
    highscorestitlerect = highscorestitle.get_rect()
    highscorestitlerect.bottomleft = highscoresrect.topleft
    highscorestitlerect.top -= 5

    pun = textFont.render(random.choice(assets.jokes), True, colors.white)
    punrect = pun.get_rect()
    punrect.topright = displayrect.topright

    while True:
        display.fill(colors.black)
        display.blit(finalscore, finalscorerect)
        display.blit(accuracy, accuracyrect)
        display.blit(correct, correctrect)
        display.blit(survived, survivedrect)
        display.blit(highscorestitle, highscorestitlerect)
        display.blit(highscores, highscoresrect)
        display.blit(pun, punrect)
        display.blit(presskey, presskeyrect)
        if not pygame.mixer.get_busy():
            assets.loop1.play()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                raise MAIN.LevelFinished()
        pygame.display.update()

def main():
    scores = getHighScores()
    scores.sort(key=lambda x: x[1], reverse=True)
    print(scores)

if __name__ == '__main__':
    main()
