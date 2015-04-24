
import pygame


sprites = 17
length = 64
outname = 'abm-holder.png'

def main():
    size = (sprites * length, length)
    s = pygame.Surface(size)
    s.fill((123,123,123))
    print('Spritesembler: Surface size is %sx%s' % size)
    for i in range(0, sprites):
        filename = 'a%s.png' % (i + 1)
        img = pygame.image.load(filename)
        pos = (i * length, 0)
        s.blit(img, pos)
        print('Blitted %s at %s' % (filename, pos))
    pygame.image.save(s, outname)
    print('Outputted to %s' % outname)
            
if __name__ == '__main__':
    main()
