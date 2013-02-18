import pygame
import config

kills = 0
shots = 0
damage = 0
life = 3
spawned = 0
level = {'level': 0,
         'spawned': 0}

bonus = {
         'speed': 1.0, # fighter speed
         'slowdown': 1.0, # slows down enemy
         'power': 1.0, # bullet power
         'bspeed': 1.0, # bullet speed
         'rspeed': 1.0 # reload speed
         }


pygame.font.init()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode(config.size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

def update():
    txt = 'Kills: %s\nShots: %s\nDamage: %s\nLife: %s' % (kills, shots, damage, life)
    text = font.render(txt, 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2)
    background.blit(text, textpos)
