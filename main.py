#!/usr/bin/env python

import os
import pygame
from pygame.locals import *
from objects import *
import stats
import config
from random import randint, choice


def main():
    if not pygame.font:
        print 'Warning, fonts disabled'
        return
    if not pygame.mixer:
        print 'Warning, sound disabled'

    pygame.font.init()
    music = pygame.mixer.music

    if config.music:
        try:
            music.load(os.path.join('data', 'music.ogg'))
        except:
            print "No music"
            config.music = False

    pygame.init()
    screen = pygame.display.set_mode(config.size)
    pygame.display.set_caption('SpaceFight')
    pygame.mouse.set_visible(0)

    background = pygame.image.load(os.path.join('data', \
                                                'background.png')).convert()

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    spawn = True
    lastCast = pygame.time.get_ticks()
    lastPowerUp = pygame.time.get_ticks()
    enemies = pygame.sprite.RenderPlain(Ufo())
    fighter = Fighter(enemies)
    fighterGroup = pygame.sprite.RenderPlain(fighter)
    powerups = pygame.sprite.RenderPlain(choice(config.powerups)(fighter))

    if config.music:
        music.set_volume(0.8)
        music.play(-1)

    while 1:
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    return
                #######################################################
                #                         DEBUG                       #
                #######################################################
                elif event.key == K_s:
                    enemies.add(Ufo())
                    lastCast = pygame.time.get_ticks()
                elif event.key == K_p:
                    powerups.add(choice(config.powerups)(fighter))
                    lastPowerUp = pygame.time.get_ticks()
                #######################################################
                elif event.key == K_SPACE:
                    fighter.shotType = fighter.shootRocket
                    fighter.shooting = True
                elif event.key == K_c:
                    fighter.shotType = fighter.shootSuperChicken
                    fighter.shooting = True
                elif event.key == K_UP or event.key == K_l:
                    fighter.shotType = fighter.shootLaser
                    fighter.shooting = True
                elif event.key == K_RIGHT:
                    fighter.dx = min(fighter.speed, fighter.maxspeed)
                elif event.key == K_LEFT:
                    fighter.dx = -min(fighter.speed, fighter.maxspeed)
                elif event.key == K_f:
                    pygame.display.toggle_fullscreen()
            elif event.type == KEYUP:
                if event.key == K_RIGHT and fighter.dx > 0:
                    fighter.dx = 0
                elif event.key == K_LEFT and fighter.dx < 0:
                    fighter.dx = 0
                elif event.key == K_SPACE and fighter.shotType == fighter.shootRocket:
                    fighter.shooting = False
                elif (event.key == K_UP  or event.key == K_l) and fighter.shotType == fighter.shootLaser:
                    fighter.shooting = False
                elif event.key == K_c and fighter.shotType == fighter.shootSuperChicken:
                    fighter.shooting = False


        if pygame.time.get_ticks() - lastCast >= config.levels[stats.level['level']]['spawnSpeed'] and stats.level['spawned'] < config.levels[stats.level['level']]['spawns']:
            enemies.add(Ufo())
            lastCast = pygame.time.get_ticks()
            stats.level['spawned'] += 1

        if pygame.time.get_ticks() - lastPowerUp >= config.levels[stats.level['level']]['powerUpSpeed']:
            powerups.add(choice(config.powerups)(fighter))
            lastPowerUp = pygame.time.get_ticks()

        if stats.level['spawned'] == config.levels[stats.level['level']]['spawns']:
            # spawn endboss
            pass


        screen.blit(background, (0, 0))
        stats.update()
        fighterGroup.update()
        fighterGroup.draw(screen)
        powerups.update()
        powerups.draw(screen)
        enemies.update()
        enemies.draw(screen)
        pygame.display.flip()

main()
