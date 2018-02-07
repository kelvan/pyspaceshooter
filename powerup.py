from __future__ import print_function, unicode_literals

from random import randint

import pygame

from utils import powerUpSound, load_image, load_sliced_sprites
import stats


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, images, player, speed=3, delay=250, image='powerup1.png'):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = speed
        self._last_update = 0
        self._frame = 0
        self._start = pygame.time.get_ticks()
        self._delay = delay
        self.powerUpSound = powerUpSound
        self.image, self.rect = load_image(image, -1)
        self.images = load_sliced_sprites(32, 32, images)
        self.player = player
        # powerup strength
        self.power = 0.1
        self.rect.top = 0
        self.rect.left = randint(0, self.area.right - 32)
        self.bonus = 0

    def update(self):
        self.fall_down()

    def fall_down(self):
        t = pygame.time.get_ticks()

        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self.images):
                self._frame = 0
            self.image = self.images[self._frame]
            self._last_update = t

        self.rect = self.rect.move((0, self.speed))

        self.check_collide()
        if self.rect.top > self.area.bottom:
            self.kill()

    def check_collide(self):
        if self.rect.colliderect(self.player):
            self.kill()
            self.powerUpSound.play()
            self.power_up()
            self.fade()

    def power_up(self):
        stats.bonus[self.bonus] += self.power

    def fade(self):
        print('got powerup')


class SpeedPowerUp(PowerUp):
    def __init__(self, player):
        PowerUp.__init__(self, 'powerup.png', player)
        self.bonus = 'speed'

    def fade(self):
        print('got speed powerup')


class BulletSpeedPowerUp(PowerUp):
    def __init__(self, player):
        PowerUp.__init__(self, 'powerup.png', player)
        self.bonus = 'bspeed'

    def fade(self):
        print('got bullet speed powerup')


class ReloadSpeedPowerUp(PowerUp):
    def __init__(self, player):
        PowerUp.__init__(self, 'powerup.png', player)
        self.bonus = 'rspeed'

    def fade(self):
        print('got reload powerup')


class PowerPowerUp(PowerUp):
    def __init__(self, player):
        PowerUp.__init__(self, 'powerup.png', player)
        self.bonus = 'power'

    def fade(self):
        print('got power powerup')


class SlowDownPowerUp(PowerUp):
    def __init__(self, player):
        PowerUp.__init__(self, 'powerup.png', player)
        self.bonus = 'slowdown'

    def fade(self):
        print('got slowdown powerup')
