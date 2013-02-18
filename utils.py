import pygame
from pygame.locals import *
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is - 1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound


def load_sliced_sprites(w, h, filename):
    '''
    Specs :
        Master can be any height.
        Sprites frames width must be the same width
        Master width must be len(frames)*frame.width
    Assuming you ressources directory is named "data"
    '''
    images = []
    master_image = pygame.image.load(os.path.join('data', filename)).convert_alpha()

    master_width, master_height = master_image.get_size()
    for i in xrange(int(master_width / w)):
        images.append(master_image.subsurface((i * w, 0, w, h)))
    return images


pygame.mixer.init()
pygame.mixer.set_num_channels(21)
explodeSound = load_sound('explode.ogg')
rocketSound = load_sound('rocket.ogg')
laserSound = load_sound('laser.ogg')
chickenSound = load_sound('chicken.ogg')
missleExplosion = load_sound('missile_explosion.ogg')
bombExplosion = load_sound('bombexplosion.ogg')
bamf = load_sound('bamf.ogg')
scream = load_sound('scream.ogg')
powerUpSound = load_sound('powerup.ogg')
