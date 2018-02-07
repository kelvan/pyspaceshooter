import pygame

from utils import load_image, laserSound, rocketSound, explodeSound, \
    missleExplosion, scream, load_sliced_sprites, chickenSound
import stats


class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, image, enemies, power, speed, maxspeed=None):
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.image, self.rect = load_image(image, -1)
        self.area = screen.get_rect()
        self.rect.centerx = x
        self.enemies = enemies
        self.rect.bottom = y
        self.speed = speed
        if maxspeed:
            self.maxspeed = maxspeed
        else:
            self.maxspeed = speed / 2
        self.power = power
        p = min(stats.bonus['power'], 1.5)
        width = int(p * self.image.get_width())
        height = int(p * self.image.get_height())
        self.image = pygame.transform.scale(self.image, (width, height))

    def update(self):
        s = min(self.speed * stats.bonus['bspeed'], self.maxspeed)
        self.move(s)

    def move(self, dy):
        newpos = self.rect.move((0, self.speed * stats.bonus['bspeed']))
        if not self.area.contains(newpos):
            if self.rect.bottom < self.area.top:
                self.kill()
        self.check_collide()
        self.rect = newpos

    def check_collide(self):
        for c in pygame.sprite.spritecollide(self, self.enemies, False):
            self.kill()
            stats.damage += self.power * stats.bonus['power']
            c.hit(self.power * stats.bonus['power'])


class Rocket(Shot):
    def __init__(self, x, y, enemies, power=5, speed=-5):
        Shot.__init__(self, x, y, 'rocket.png', enemies, power, speed)


class Laser(Shot):
    def __init__(self, x, y, enemies, power=2, speed=-10):
        Shot.__init__(self, x, y, 'laser.png', enemies, power, speed)


class SuperChicken(Shot):
    def __init__(self, x, y, enemies, power=200, speed=-25):
        Shot.__init__(self, x, y, 'superchicken.png', enemies, power, speed)


class Fighter(pygame.sprite.Sprite):
    def __init__(self, enemies, speed=8, maxspeed=20):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('fighter.png', -1)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.speed = speed
        self.maxspeed = maxspeed
        self.dx = 0
        self.enemies = enemies
        self.shooting = False
        self.rect.bottom = self.area.bottom
        self.rect.centerx = self.area.centerx
        self.shots = pygame.sprite.Group()
        self._ticks = pygame.time.get_ticks()
        self._rocketDelay = 500
        self._last_update = 0
        self._start = pygame.time.get_ticks()
        self.shotType = None

    def update(self):
        if self.shooting:
            self.shotType()
        if self.dx:
            self.move_side(self.dx)
        self.shots.update()
        self.shots.draw(self.screen)

    def move_side(self, dx):
        dx *= stats.bonus['speed']
        if self.rect.left + dx <= self.area.left:
            self.rect.left = self.area.left
        elif self.rect.right + dx >= self.area.right:
            self.rect.right = self.area.right
        else:
            self.rect.centerx += dx

    def move(self, dx, dy):
        self.rect.midtop = (self.rect.x + dx, self.rect.y + dy)

    def shootRocket(self, delay=500, mindelay=200):
        d = min(delay / stats.bonus['rspeed'], mindelay)
        if pygame.time.get_ticks() - self._last_update > d:
            self._last_update = pygame.time.get_ticks()
            rocket = Rocket(self.rect.centerx, self.rect.top, self.enemies)
            self.shots.add(rocket)
            stats.shots += 1
            rocketSound.play()

    def shootLaser(self, delay=200, mindelay=100):
        d = min(delay / stats.bonus['rspeed'], mindelay)
        if pygame.time.get_ticks() - self._last_update > d:
            self._last_update = pygame.time.get_ticks()
            laser = Laser(self.rect.centerx, self.rect.top, self.enemies)
            self.shots.add(laser)
            stats.shots += 1
            laserSound.play()

    def shootSuperChicken(self, delay=1000, mindelay=750):
        d = min(delay / stats.bonus['rspeed'], mindelay)
        if pygame.time.get_ticks() - self._last_update > d:
            self._last_update = pygame.time.get_ticks()
            chicken = SuperChicken(self.rect.centerx, self.rect.top,
                                   self.enemies)
            self.shots.add(chicken)
            stats.shots += 1
            chickenSound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, life, speed, minspeed=None, bombdelay=None,
                 bomb=None, explodeimg='explode.png'):
        if not minspeed:
            self.minspeed = speed / 2
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = speed
        self.life = life
        self.exploding = False
        self._last_update = 0
        self._frame = 0
        self._start = pygame.time.get_ticks()
        self._delay = 100
        self.explodeSound = explodeSound
        self.explodeImages = load_sliced_sprites(128, 128, explodeimg)

    def update(self):
        if self.exploding:
            self.explode()
        else:
            self._move()

    def _move(self):
        if self.rect.left > self.area.right or \
           self.rect.right < self.area.left:
            if self.rect.bottom <= self.area.bottom - 128:
                self.rect.centery += 40
            else:
                self._breakthrough()
            self.speed *= -1.05

            if self.rect.left > self.area.right:
                self.rect.left = self.area.right
            else:
                self.rect.right = self.area.left

        else:
            if self.speed > 0:
                s = max(self.speed / stats.bonus['slowdown'], -self.minspeed)
            else:
                s = min(self.speed / stats.bonus['slowdown'], self.minspeed)
            self.rect = self.rect.move((s, 0))

    def _breakthrough(self):
        stats.life -= 1
        scream.play()
        self.kill()

    def hit(self, power):
        self.life -= power
        missleExplosion.play()
        if self.life <= 0:
            self.exploding = True
            self._start = pygame.time.get_ticks()

    def explode(self):
        t = pygame.time.get_ticks()

        if self._frame == 0:
            self.explodeSound.play()
            self.rect.centery -= 40

        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self.explodeImages):
                self._frame = 0
                self.kill()
                stats.kills += 1
            self.image = self.explodeImages[self._frame]
            self._last_update = t


class Ufo(Enemy):
    def __init__(self):
        Enemy.__init__(self, 'ufo.png', 25, 8)
        self.rect.topright = 0, 30
        stats.spawned += 1
